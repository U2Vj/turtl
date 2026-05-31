# Limitations

This page documents the current limitations and possible improvements of TURTL.

## No internet access for lab VMs

Cloned lab VMs run on an isolated, VLAN-aware Linux bridge without a gateway. Therefore all lab VMs do not have internet access.

Any software needed for a task needs to be installed in the template beforehand. During the creation of the template VM you can temporarily attach a second network device to allow for internet access. This must be removed again before converting the VM to a template.

## Single-node only

While Proxmox can be run in a cluster, TURTL currently only picks the first available node in a cluster and creates all VMs there. There is no load balancing of VMs across multiple nodes.

Every template must be available on the node that gets selected.

## Custom Cloud-Init scripts

Proxmox allows for using custom Cloud-Init scripts via the cicustom option. ([Proxmox documentation](https://pve.proxmox.com/wiki/Cloud-Init_Support))

This is not currently supported by TURTL, however a placeholder has been set for this feature in [vm_ops](../../vm_manager/proxmox/vm_ops.py). 

To implement the feature there needs to be code that uploads and manages the custom Cloud-Init scripts on the snippets storage of Proxmox.

## IPv4 only

IPv6 is currently not supported for planned VM IP addresses.

## Maximum number of networks

VLAN tags count from 2 to 4094, allowing for a maximum of 4093 active networks in TURTL.
