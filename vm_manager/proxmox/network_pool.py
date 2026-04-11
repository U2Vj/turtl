import logging
from django.db import transaction
from ..utils import AdvisoryLock, slugify
from ..models import BridgePoolEntry, Network

logger = logging.getLogger(__name__)

LOCK_ACQUIRE_TIMEOUT = 30


class NoBridgeAvailableError(Exception):
    pass


def provision_network(user, task, task_config):
    """
    Assigns a bridge from the pool to a new network for the given user and task.
    The subnet is taken from the NetworkTemplate (used for cloud-init IP assignment).
    The bridges must already exist in Proxmox – no Proxmox API calls are made here.
    """
    network_template = task_config.network_template
    if not network_template:
        raise ValueError(f"No network template defined for task: {task.title}")

    lock_name = "proxmox_bridge_allocation"

    with AdvisoryLock(lock_name, timeout_seconds=LOCK_ACQUIRE_TIMEOUT) as acquired:
        if not acquired:
            raise TimeoutError("Could not acquire lock for bridge allocation")

        with transaction.atomic():
            # 1. Find next available bridge from pool
            bridge_entry = BridgePoolEntry.objects.select_for_update().filter(allocated_to__isnull=True).first()

            if not bridge_entry:
                raise NoBridgeAvailableError("No bridge available in pool. Please add more bridges via Django admin.")

            bridge_name = bridge_entry.bridge_name
            network_name = f"{slugify(task.title)}-{slugify(user.username)}-net"

            # Extract numeric ID from bridge name (e.g. "vmbr100" -> 100) for vlan_id field
            try:
                vlan_id = int(bridge_name.replace("vmbr", ""))
            except ValueError:
                raise ValueError(f"Bridge name '{bridge_name}' does not follow expected format 'vmbrNNN'")

            # 2. Create network in database (subnet from NetworkTemplate for cloud-init)
            network = Network.objects.create(
                name=network_name,
                subnet=network_template.subnet,
                vlan_id=vlan_id,
                template=network_template,
                user=user,
                task=task
            )

            # 3. Mark bridge as allocated
            bridge_entry.allocated_to = network
            bridge_entry.save()

            logger.info(
                "Bridge assigned from pool bridge=%s user_id=%s task_id=%s",
                bridge_name,
                user.id,
                task.id,
            )
            return network


def release_network(network):
    """
    Returns the bridge assigned to the given network back to the pool and deletes the network record.
    No Proxmox API calls are made – the bridge remains in Proxmox unchanged.
    """
    try:
        bridge_entry = network.bridge_pool_entry
        bridge_entry.allocated_to = None
        bridge_entry.save()
        logger.info("Bridge returned to pool bridge=%s network_id=%s", bridge_entry.bridge_name, network.id)
    except BridgePoolEntry.DoesNotExist:
        logger.warning("No pool entry found for network_id=%s, skipping release", network.id)

    network.delete()
