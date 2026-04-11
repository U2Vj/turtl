import time
import logging

logger = logging.getLogger(__name__)

LOCK_TIMEOUT = 120
POLL_INTERVAL = 2


def clone_vm(proxmox, node, template_id, new_id, new_name, linked_clone=True):
    """
    Clones a VM from a template_id as a linked clone
    """
    params = {
        'newid': new_id,
        'name' : new_name,
        'target': node,
        'full': 0 if linked_clone else 1
    }

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


def configure_vm(proxmox, node, vm_id, storage, ci_user, ci_password, bridge, ip_address, cpu_cores, memory_mb):
    """
    Configures the VM via Cloud-init
    """
    try:
        config_params = {
            'ide2': f"{storage}:cloudinit",
            'ciuser': ci_user,
            'net0': f"virtio,bridge={bridge}",
            'ipconfig0': f"ip={ip_address}",
            'cipassword': ci_password,
            'agent': 'enabled=1',
            'boot': 'order=scsi0',
            'cicustom': 'user=local:snippets/user-data.yaml',
            'sockets': 1,
            'cores': int(cpu_cores),
            'memory': int(memory_mb),
        }

        proxmox.nodes(node).qemu(vm_id).config.post(**config_params)
        logger.debug("VM options set successfully vmid=%s", vm_id)
    except Exception:
        logger.exception("Error configuring VM vmid=%s node=%s", vm_id, node)
        raise
