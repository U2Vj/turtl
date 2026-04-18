import logging
from django.db import transaction
from ..utils import AdvisoryLock, slugify
from ..models import Network

logger = logging.getLogger(__name__)

LOCK_ACQUIRE_TIMEOUT = 30
VLAN_TAG_MIN = 2
VLAN_TAG_MAX = 4094


class NoVlanAvailableError(Exception):
    pass


def _next_free_vlan_id():
    """
    Returns the lowest VLAN tag in the configured range that is not
    currently used by any Network record.
    """
    used = set(Network.objects.values_list('vlan_id', flat=True))
    for tag in range(VLAN_TAG_MIN, VLAN_TAG_MAX + 1):
        if tag not in used:
            return tag
    return None


def provision_network(user, task, task_config):
    """
    Creates a network for the given user and task by assigning the next
    available VLAN tag. No Proxmox API calls are made — the VLAN-aware
    bridge must already exist on the Proxmox host.
    """
    network_template = task_config.network_template
    if not network_template:
        raise ValueError(f"No network template defined for task: {task.title}")

    lock_name = "proxmox_vlan_allocation"

    with AdvisoryLock(lock_name, timeout_seconds=LOCK_ACQUIRE_TIMEOUT) as acquired:
        if not acquired:
            raise TimeoutError("Could not acquire lock for VLAN allocation")

        with transaction.atomic():
            vlan_id = _next_free_vlan_id()
            if vlan_id is None:
                raise NoVlanAvailableError("No VLAN tags available in configured range.")

            network_name = f"{slugify(task.title)}-{slugify(user.username)}-net"

            network = Network.objects.create(
                name=network_name,
                subnet=network_template.subnet,
                vlan_id=vlan_id,
                template=network_template,
                user=user,
                task=task
            )

            logger.info(
                "VLAN tag assigned vlan_id=%s user_id=%s task_id=%s",
                vlan_id,
                user.id,
                task.id,
            )
            return network


def release_network(network):
    """
    Deletes the network record, freeing its VLAN tag for reuse.
    """
    vlan_id = network.vlan_id
    network_id = network.id
    network.delete()
    logger.info("Network released vlan_id=%s network_id=%s", vlan_id, network_id)
