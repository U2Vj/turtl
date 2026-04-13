import time
import logging

logger = logging.getLogger(__name__)

LOCK_TIMEOUT = 120
POLL_INTERVAL = 2


def clone_vm(proxmox, node, template_id, new_id, new_name, linked_clone=True, pool=None):
    """
    Clones a VM from a template_id as a linked clone
    """
    params = {
        'newid': new_id,
        'name' : new_name,
        'target': node,
        'full': 0 if linked_clone else 1
    }

    if pool:
        params['pool'] = pool

    try:
        proxmox.nodes(node).qemu(template_id).clone.post(**params)
        logger.debug("Clone command sent for vmid=%s from template_id=%s", new_id, template_id)
    except Exception:
        logger.exception(
            "Error cloning template template_id=%s new_id=%s node=%s",
            template_id,
            new_id,
            node,
        )
        raise

    logger.debug("Waiting for lock removal on vmid=%s", new_id)
    wait_for_unlock(proxmox, node, new_id)
    logger.debug("Lock removed from vmid=%s", new_id)


def wait_for_unlock(proxmox, node, vm_id, timeout=None, interval=None):
    """
    Waits until the VM Lock is removed by Proxmox
    """
    if timeout is None:
        timeout = LOCK_TIMEOUT
    if interval is None:
        interval = POLL_INTERVAL

    start = time.time()
    while True:
        locks = proxmox.nodes(node).qemu(vm_id).status.current.get().get('lock')
        if not locks:
            return
        if time.time() - start > timeout:
            raise TimeoutError(f"Timeout waiting for unlock of VM {vm_id}")
        time.sleep(interval)


def wait_for_vm_stopped(proxmox, node, vm_id, timeout=None, interval=None):
    """
    Waits until the VM status is 'stopped'
    """
    if timeout is None:
        timeout = LOCK_TIMEOUT
    if interval is None:
        interval = POLL_INTERVAL

    start = time.time()
    while True:
        vm_status = proxmox.nodes(node).qemu(vm_id).status.current.get().get('status')
        if vm_status == 'stopped':
            return
        if time.time() - start > timeout:
            raise TimeoutError(f"Timeout waiting for VM {vm_id} to stop")
        time.sleep(interval)


def _detect_boot_disk_from_config(config):
    """
    Detects the boot disk from a VM config dict by looking for the first
    existing disk in common bus types (scsi, sata, ide, virtio).
    """
    for bus in ('scsi', 'sata', 'ide', 'virtio'):
        key = f'{bus}0'
        if key in config:
            return key
    return 'scsi0'


def configure_vm(proxmox, node, vm_id, storage, cpu_cores, memory_mb, bridge=None, vlan_tag=None, ip_address=None, cloud_init=True):
    """
    Configures the VM. When cloud_init is True, a cloud-init drive is
    attached and ipconfig0 is set if an IP address is provided.
    When bridge is provided, a network interface is configured with an optional VLAN tag.
    """
    try:
        vm_config = proxmox.nodes(node).qemu(vm_id).config.get()
        boot_disk = _detect_boot_disk_from_config(vm_config)
        config_params = {
            'agent': 'enabled=1',
            'boot': f'order={boot_disk}',
            'sockets': 1,
            'cores': int(cpu_cores),
            'memory': int(memory_mb),
        }

        if bridge:
            # Preserve existing NIC model and MAC, only update bridge and VLAN tag
            existing_net0 = vm_config.get('net0', '')
            if existing_net0:
                # Parse existing config into key=value parts, keeping model=MAC as-is
                parts = existing_net0.split(',')
                new_parts = []
                for part in parts:
                    key = part.split('=')[0] if '=' in part else ''
                    if key in ('bridge', 'tag'):
                        continue  # drop old bridge/tag
                    new_parts.append(part)
                new_parts.append(f"bridge={bridge}")
                if vlan_tag is not None:
                    new_parts.append(f"tag={vlan_tag}")
                net0 = ','.join(new_parts)
            else:
                net0 = f"virtio,bridge={bridge}"
                if vlan_tag is not None:
                    net0 += f",tag={vlan_tag}"
            config_params['net0'] = net0
        else:
            config_params['delete'] = 'net0'

        if cloud_init:
            config_params['ide2'] = f"{storage}:cloudinit"
            if ip_address:
                config_params['ipconfig0'] = f"ip={ip_address}"
            # TODO: cicustom can be re-enabled to support custom cloud-init snippets
            # config_params['cicustom'] = 'user=local:snippets/user-data.yaml'

        proxmox.nodes(node).qemu(vm_id).config.post(**config_params)
        logger.debug("VM options set successfully vmid=%s cloud_init=%s", vm_id, cloud_init)
    except Exception:
        logger.exception("Error configuring VM vmid=%s node=%s", vm_id, node)
        raise
