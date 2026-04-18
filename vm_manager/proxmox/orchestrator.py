import os
import logging
from django.db import transaction
from django.utils import timezone
from ..utils import AdvisoryLock, slugify, format_ip
from ..models import LabEnvironment, Network, TaskVMConfiguration, VirtualMachine
from .client import ProxmoxClient
from .vm_ops import clone_vm, configure_vm, wait_for_unlock, wait_for_vm_stopped
from .network_pool import provision_network, release_network, NoVlanAvailableError

logger = logging.getLogger(__name__)


class ProxmoxManager(ProxmoxClient):

    def _get_lab_env_lock_name(self, lab_env_id):
        return f"lab_env_operation_{lab_env_id}"

    def create_lab_environment(self, user, task):
        """
        Create a new lab environment for a user and task.
        1. Create network
        2. Create VMs from the task configuration
        """

        # create lock on user-task to prevent attempted creation of duplicate environments
        lock_name = f"lab_env_{user.id}_{task.id}"

        with AdvisoryLock(lock_name, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for lab environment creation (user: {user.id}, task: {task.id})")

            try:
                #Check if environment already exists
                existing_env = LabEnvironment.objects.filter(user=user, task=task).first()
                if existing_env:
                    logger.info(
                        "Lab environment already exists for user_id=%s task_id=%s",
                        user.id,
                        task.id,
                    )
                    return existing_env

                task_config = TaskVMConfiguration.objects.filter(task=task).first()
                if not task_config:
                    raise ValueError(f"No VM configuration found for task: {task.title}")

                with transaction.atomic():
                    # 1. Assign network from bridge pool if network template is set
                    network = None
                    if task_config.network_template:
                        network = provision_network(user, task, task_config)

                    # 2. Create the lab environment record
                    lab_env = LabEnvironment.objects.create(
                        user=user,
                        task=task,
                        network=network
                    )

                    # 3. Create all VMs for env
                    for vm_template_config in task_config.vm_templates.all():
                        self.provision_vm(lab_env, vm_template_config, network, user, task)

                    # 4. Update lab_env status
                    lab_env.status = 'active'
                    lab_env.last_seen_at = timezone.now()
                    lab_env.stopped_at = None
                    lab_env.save()

                    return lab_env

            except Exception:
                logger.exception(
                    "Error creating lab environment for task_id=%s user_id=%s",
                    task.id,
                    user.id,
                )
                self.cleanup_orphans()
                raise

    def provision_vm(self, lab_env, vm_template_config, network, user, task):
        """
        Create VM in Proxmox and configure it for network
        """

        vm_creation_lock = "proxmox_vm_creation"

        try:
            template = vm_template_config.template
            node = self.get_node()
            vm_name = f"vm-{slugify(template.name)}"

            # Network config
            bridge_name = None
            vlan_tag = None
            ip_address = None
            if network:
                ip_address = format_ip(vm_template_config.planned_ip_address, network)
                bridge_name = os.environ.get('PROXMOX_VLAN_BRIDGE')
                vlan_tag = network.vlan_id

            with AdvisoryLock(vm_creation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
                if not acquired:
                    raise TimeoutError("Could not acquire lock for VM creation")

                vmid = self.proxmox.cluster.nextid.get()

                logger.debug(
                    "Cloning VM from template template_id=%s vm_name=%s vmid=%s",
                    template.template_id,
                    vm_name,
                    vmid,
                )
                pool = os.environ.get('PROXMOX_VM_POOL')

                clone_vm(
                    proxmox=self.proxmox,
                    node=node,
                    template_id=template.template_id,
                    new_id=vmid,
                    new_name=vm_name,
                    pool=pool,
                )

                logger.debug(
                    "Configuring VM vmid=%s bridge=%s vlan_tag=%s ip=%s cloud_init=%s",
                    vmid, bridge_name, vlan_tag, ip_address, vm_template_config.cloud_init,
                )
                storage = 'local-lvm'

                configure_vm(
                    proxmox=self.proxmox,
                    node=node,
                    vm_id=vmid,
                    storage=storage,
                    cpu_cores=template.cpu_cores,
                    memory_mb=template.memory_mb,
                    bridge=bridge_name,
                    vlan_tag=vlan_tag,
                    ip_address=ip_address,
                    cloud_init=vm_template_config.cloud_init,
                )

                # Wait for Proxmox
                wait_for_unlock(self.proxmox, node, vmid)

                #Add VM to database
                with transaction.atomic():
                    vm = VirtualMachine.objects.create(
                        vmid=vmid,
                        lab_environment=lab_env,
                        template=template,
                        name=vm_name,
                        status='creating',
                        network=network,
                        assigned_ip_address=ip_address.split('/')[0] if ip_address else None
                    )

                # Start the VM
                logger.debug("Starting VM vmid=%s", vmid)
                self.proxmox.nodes(node).qemu(vmid).status.start.post()

                # Update status
                vm.status = 'running'
                vm.save()

            return vm
        except Exception:
            logger.exception(
                "Error provisioning VM for task_id=%s user_id=%s env_id=%s",
                task.id,
                user.id,
                lab_env.id,
            )
            raise

    def start_environment(self, lab_env):
        """
        Starts all VMs inside a lab environment
        """
        env_operation_lock = self._get_lab_env_lock_name(lab_env.id)
        with AdvisoryLock(env_operation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for starting environment {lab_env.id}")

            try:
                lab_env.status = 'starting'
                lab_env.save()
                with transaction.atomic():
                    for vm in lab_env.virtual_machines.select_for_update().all():
                        if vm.status != 'running':
                            # Start the VM
                            node = self.get_vm_node(vm.vmid)
                            self.proxmox.nodes(node).qemu(vm.vmid).status.start.post()
                            vm.status = 'running'
                            vm.save()
                    # Update lab environment status
                    if lab_env.status != 'active':
                        lab_env.status = 'active'
                        lab_env.stopped_at = None
                        lab_env.last_seen_at = timezone.now()
                        lab_env.save()
                return True
            except Exception:
                logger.exception("Error starting lab environment env_id=%s", lab_env.id)
                return False

    def stop_environment(self, lab_env):
        """
        Stops all VMs inside a lab environment
        """
        env_operation_lock = self._get_lab_env_lock_name(lab_env.id)
        with AdvisoryLock(env_operation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for stopping environment {lab_env.id}")

            try:
                lab_env.status = 'stopping'
                lab_env.save()

                with transaction.atomic():
                    for vm in lab_env.virtual_machines.select_for_update().all():
                        if vm.status == 'running':
                            # Stop the VM
                            node = self.get_vm_node(vm.vmid)
                            self.proxmox.nodes(node).qemu(vm.vmid).status.stop.post()
                            # Update VM status
                            vm.status = 'stopped'
                            vm.save()

                    current_time = timezone.now()
                    update_fields = []

                    if lab_env.status != 'stopped':
                        lab_env.status = 'stopped'
                        update_fields.append('status')

                    if lab_env.stopped_at is None:
                        lab_env.stopped_at = current_time
                        lab_env.last_seen_at = current_time
                        update_fields.extend(['stopped_at', 'last_seen_at'])

                    if update_fields:
                        lab_env.save(update_fields=update_fields)
                return True
            except Exception:
                logger.exception("Error stopping lab environment env_id=%s", lab_env.id)
                if lab_env.status == 'stopping':
                    lab_env.status = 'degraded'
                    lab_env.save(update_fields=['status'])
                raise

    def cleanup_environment(self, user, task):
        """
        Deletes all VMs and the network of a lab environment for a given user and task. Then deletes the lab environment.
        """
        existing_env = LabEnvironment.objects.filter(user=user, task=task).only('id').first()
        if not existing_env:
            logger.info(
                "No lab environment found for cleanup user_id=%s task_id=%s",
                user.id,
                task.id,
            )
            return "not_found"

        env_operation_lock = self._get_lab_env_lock_name(existing_env.id)
        with AdvisoryLock(env_operation_lock, timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                logger.warning(
                    "Could not acquire lock for cleanup user_id=%s task_id=%s",
                    user.id,
                    task.id,
                )
                return "locked"

            try:
                # Get the lab environment
                lab_env = LabEnvironment.objects.filter(user=user, task=task).first()
                if not lab_env:
                    logger.info(
                        "No lab environment found for cleanup user_id=%s task_id=%s",
                        user.id,
                        task.id,
                    )
                    return "not_found"
                # Mark environment as being cleaned up
                if lab_env.status != 'cleanup':
                    lab_env.status = 'cleanup'
                    lab_env.save()
                # Delete all VMs
                for vm in lab_env.virtual_machines.all():
                    try:
                        node = self.get_vm_node(vm.vmid)
                        # Stop the VM and wait for it to stop
                        try:
                            self.proxmox.nodes(node).qemu(vm.vmid).status.stop.post()
                            wait_for_vm_stopped(self.proxmox, node, vm.vmid)
                        except Exception:
                            logger.warning(
                                "Could not stop VM during cleanup vmid=%s env_id=%s",
                                vm.vmid,
                                lab_env.id,
                                exc_info=True,
                            )
                        self.proxmox.nodes(node).qemu(vm.vmid).delete()
                        # Delete VM from database
                        vm.delete()
                    except Exception:
                        logger.warning(
                            "Could not delete VM during cleanup vmid=%s env_id=%s",
                            vm.vmid,
                            lab_env.id,
                            exc_info=True,
                        )

                # Release the network bridge back to the pool
                if lab_env.network:
                    try:
                        release_network(lab_env.network)
                    except Exception:
                        logger.warning(
                            "Error releasing network during cleanup env_id=%s",
                            lab_env.id,
                            exc_info=True,
                        )

                # Delete lab environment
                lab_env.delete()
                return "deleted"

            except Exception:
                logger.exception(
                    "Error during cleanup for user_id=%s task_id=%s",
                    user.id,
                    task.id,
                )
                try:
                    lab_env = LabEnvironment.objects.filter(user=user, task=task).first()
                    if lab_env and lab_env.status == 'cleanup':
                        lab_env.status = 'stopped'
                        if lab_env.stopped_at is None:
                            lab_env.stopped_at = timezone.now()
                        lab_env.save(update_fields=['status', 'stopped_at'])
                finally:
                    self.cleanup_orphans()
                return "failed"

    def cleanup_orphans(self):
        """
        Searches for orphan VMs in Proxmox that have no matching database record and deletes them.
        Bridge cleanup is omitted – pool bridges are never deleted by TURTL.
        """
        with AdvisoryLock("proxmox-cleanup", timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as acquired:
            if not acquired:
                return

            # check if vm creation is ongoing, if yes do not cleanup
            with AdvisoryLock("proxmox_vm_creation", timeout_seconds=self.LOCK_ACQUIRE_TIMEOUT) as vm_lock_acquired:

                if not vm_lock_acquired:
                    return

                pool = os.environ.get('PROXMOX_VM_POOL')

                if not pool:
                    logger.warning("PROXMOX_VM_POOL not set, skipping orphan cleanup")
                    return

                try:
                    pool_data = self.proxmox.pools(pool).get()
                    resources = [m for m in pool_data.get('members', []) if m.get('type') == 'qemu']
                except Exception:
                    logger.exception("Could not fetch pool '%s', skipping orphan cleanup", pool)
                    return

                for r in resources:
                    name = r.get('name', '')
                    vmid = int(r.get('vmid'))

                    if not VirtualMachine.objects.filter(vmid=vmid).exists():
                        logger.info("Found orphan VM in pool=%s vmid=%s name=%s, deleting", pool, vmid, name)
                        try:
                            node = r.get('node') or self.get_vm_node(vmid)
                            self.proxmox.nodes(node).qemu(vmid).status.stop.post()
                            wait_for_vm_stopped(self.proxmox, node, vmid)
                            self.proxmox.nodes(node).qemu(vmid).delete()
                        except Exception:
                            logger.warning("Could not delete orphan VM vmid=%s", vmid, exc_info=True)

                # Clean up orphan networks (without lab environment)
                orphan_networks = Network.objects.filter(lab_environments=None)
                for network in orphan_networks:
                    logger.info("Deleting orphan network id=%s name=%s", network.id, network.name)
                    network.delete()

    def sync_vm_status(self, lab_env):
        """
        Synchronizes VM status with Proxmox for a lab environment
        """
        env_operation_lock = self._get_lab_env_lock_name(lab_env.id)
        with AdvisoryLock(env_operation_lock, timeout_seconds=0) as acquired:
            if not acquired:
                logger.debug("Skipping VM status sync because environment is busy env_id=%s", lab_env.id)
                return

            try:
                any_vm = False
                all_running = True
                all_stopped = True

                for vm in lab_env.virtual_machines.all():
                    any_vm = True
                    try:
                        node = self.get_vm_node(vm.vmid)
                        vm_status = self.proxmox.nodes(node).qemu(vm.vmid).status.current.get().get('status')

                        if vm.status != vm_status:
                            vm.status = vm_status
                            vm.save()

                        if vm_status != 'running':
                            all_running = False
                        if vm_status != 'stopped':
                            all_stopped = False
                    except Exception:
                        logger.warning(
                            "Could not sync status for VM vmid=%s env_id=%s",
                            vm.vmid,
                            lab_env.id,
                            exc_info=True,
                        )
                        all_running = False
                        all_stopped = False

                if any_vm:
                    if all_running:
                        if lab_env.status != 'active' or lab_env.stopped_at is not None:
                            lab_env.status = 'active'
                            lab_env.stopped_at = None
                            lab_env.last_seen_at = timezone.now()
                            lab_env.save(update_fields=['status', 'stopped_at', 'last_seen_at'])
                        return

                    if not all_stopped:
                        update_fields = []
                        if lab_env.status != 'degraded':
                            lab_env.status = 'degraded'
                            update_fields.append('status')
                        if lab_env.stopped_at is not None:
                            lab_env.stopped_at = None
                            update_fields.append('stopped_at')
                        if update_fields:
                            lab_env.save(update_fields=update_fields)
                        logger.info(
                            "Degraded or unclear VM state detected during sync env_id=%s all_running=%s all_stopped=%s",
                            lab_env.id,
                            all_running,
                            all_stopped,
                        )
                        return

                    update_fields = []
                    if lab_env.status != 'stopped':
                        lab_env.status = 'stopped'
                        update_fields.append('status')
                    if lab_env.stopped_at is None:
                        lab_env.stopped_at = timezone.now()
                        update_fields.append('stopped_at')
                    if update_fields:
                        lab_env.save(update_fields=update_fields)

            except Exception:
                logger.exception("Error syncing VM status env_id=%s", lab_env.id)
                raise
