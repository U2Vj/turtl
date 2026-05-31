# Setup Proxmox VE for usage in TURTL

This guide describes how to prepare a Proxmox VE instance to use for TURTLs virtualization features

## Installing Proxmox
Install [Proxmox VE 9.0](https://www.proxmox.com/en/products/proxmox-virtual-environment/get-started) or higher on a dedicated machine.
The machine needs to be reachable from the TURTL host.

## Configuring Proxmox
The following commands need to be executed in the shell of the proxmox host to setup the roles and access tokens needed for TURTL.

### 1. Add resource pools

```bash
pveum pool add turtl-lab
pveum pool add turtl-templates 
```

### 2. Create roles

```bash
pveum role add TurtlApp -privs "VM.Allocate,VM.Clone,VM.Config.Disk,VM.Config.CPU,VM.Config.Memory,VM.Config.Network,VM.Config.Options,VM.Config.Cloudinit,VM.Config.CDROM,VM.Config.HWType,VM.PowerMgmt,VM.Console,VM.Monitor,VM.Audit,Datastore.AllocateSpace,Datastore.Audit,Pool.Audit,Pool.Allocate,SDN.Use"
```

and for the user:

```bash
pveum role add TurtlUser -privs "VM.Allocate,VM.Clone,VM.Config.Disk,VM.Config.CPU,VM.Config.Memory,VM.Config.Network,VM.Config.Options,VM.Config.Cloudinit,VM.Config.CDROM,VM.Config.HWType,VM.PowerMgmt,VM.Console,VM.Monitor,VM.Audit,Datastore.AllocateSpace,Datastore.Audit,Datastore.Allocate,Datastore.AllocateTemplate,Pool.Audit,Pool.Allocate,SDN.Use"
```

### 3. Create user and API token

The TURTL application needs an API token for authentication to Proxmox. Additionally a user is needed to access the Proxmox webinterface to prepare the VM templates.

```bash
pveum user add turtl@pve
pveum passwd turtl@pve
pveum user token add turtl@pve turtl-api --privsep 1
```

### 4. Create vlan aware Linux Bridge

TURTL uses a vlan aware linux bridge to provide an isolated network for every lab environment.

```bash
pvesh create /nodes/<nodename>/network \
  --iface vmbr100 \
  --type bridge \
  --bridge_vlan_aware 1 \
  --autostart 1
```

Apply the network settings:

```bash
pvesh set /nodes/<nodename>/network
```

### 5. Set ACLs

```bash
pveum aclmod /pool/turtl-lab -user turtl@pve -role TurtlUser
pveum aclmod /pool/turtl-templates -user turtl@pve -role TurtlUser
pveum aclmod /storage/local-lvm -user turtl@pve -role TurtlUser
pveum aclmod /storage/local -user turtl@pve -role TurtlUser
pveum aclmod /sdn/zones/localnetwork/vmbr100 -user turtl@pve -role PVESDNUser
```

and for the token:

```bash
pveum aclmod /pool/turtl-lab -token 'turtl@pve!turtl-api' -role TurtlApp
pveum aclmod /pool/turtl-templates -token 'turtl@pve!turtl-api' -role TurtlApp
pveum aclmod /storage/local-lvm -token 'turtl@pve!turtl-api' -role TurtlApp
pveum aclmod /sdn/zones/localnetwork/vmbr100 -token 'turtl@pve!turtl-api' -role PVESDNUser
```


## Creating Virtual Machine Templates in Proxmox

TURTL uses VM templates to clone individual virtual machines for every task and student. To create a template you can either import a virtual machine from a disk or create an entirely new VM from scratch inside proxmox.

### Example import from disk:

```bash
qm create 9000 --name "EternalBlue" --memory 2048 --cores 2 --ostype win7

qm disk import 9000 /tmp/EternalBlue-disk001.vmdk local-lvm

qm set 9000 --sata0 local-lvm:vm-9000-disk-0
qm set 9000 --boot order=sata0
qm set 9000 --net0 e1000,bridge=vmbr100

pvesh set /pools/turtl-templates --vms 9000
```

### Create a new VM in Proxmox:

The simplest way to do this is to use the Proxmox webinterface. Login to the webinterface and expand the node. Click on 'local' and select 'ISO Images' on the side bar. There you can upload an ISO file from a Windows or Linux operating system of your choice.
If you right click on the node in the sidebar you can now create a new VM using the uploaded ISO file.

When creating Linux VMs make sure to set the checkmark for 'Qemu Agent' and install the guest agent in the VM:

```bash
sudo apt-get install qemu-guest-agent
```

Be aware that it is currently not possible to provide internet access to the VMs when cloned using TURTL. Make sure to read the [limitations](../info/limitations.md) documentation to learn more.

You can set a higher CPU and RAM for installing the VM faster. The resources allocated to the lab VMs can be set later inside of TURTL.

If the VM should be used in a lab environment configuration with other VMs you need to manually set the IP address inside the virtual machine.

The alternative is to use **Cloud-Init** to set the ip address in the vm when it is cloned. This has the advantage that you can reuse the same template for multiple tasks with different ip addresses.
For this to work, cloud-init must be installed and running on the VM.


### Convert to template

If you are done configuring the VM you need to convert it into a template for TURTL to be able to clone the VMs.
Beware that the state of the VM cannot be changed after the conversion.
You can either right click the VM in the Proxmox webinterface and select 'Convert to template' or run the following command inside of the Proxmox shell:

```bash
qm template <vmid>
```

## Configure Virtual Machine Templates in Django Admin

To define lab environments, open the Django admin panel on /django-admin and configure:
1. **VMTemplate**  
   - Enter the Proxmox `template_id`  
   - Choose the `purpose` (e.g. `USER_SHELL`)  
   - Set required CPU cores and memory

2. **NetworkTemplate**
   
   If the VM is part of a lab environment consisting of multiple VMs you need to create a **NetworkTemplate**
   - Define a name  
   - Set a subnet (e.g. `10.10.0.0/24`)

3. **TaskVMConfiguration**  
   - Select the corresponding Task  
   - Assign a NetworkTemplate (optional, for multiple connected VMs)

4. **TaskVMTemplate**  
For each VM you want in the environment:  
     - Select the TaskVMConfiguration  
     - Select the VMTemplate
     - Set the IP address for the VM (if Cloud-Init is installed on the template)

