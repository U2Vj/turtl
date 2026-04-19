# Setup Proxmox VE for usage in TURTL

## Requirements

First install and configure Proxmox VE.

Then add a .env File to the root of the Project with the following variables:

```
DJANGO_SECRET_KEY=<super-secret-key>
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=<ips-of-allowed-hosts>

VM_MANAGER_LOG_LEVEL=DEBUG

POSTGRES_DB=turtl_db
POSTGRES_USER=turtl_user
POSTGRES_PASSWORD=turtl_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_HOST=<ip-of-redis>
REDIS_PORT=6379

PROXMOX_HOST=proxmox-host:port
PROXMOX_USER=turtl@pve
PROXMOX_TOKEN_NAME=turtl-api
PROXMOX_TOKEN_VALUE=<api-token>

PROXMOX_VM_POOL=turtl-lab
PROXMOX_VLAN_BRIDGE=vmbr100
PROXMOX_VERIFY_SSL=true
PROXMOX_CA_PATH=/path/to/proxmox-ca.pem

```

If you enable TLS (`PROXMOX_VERIFY_SSL=true`), copy the **Proxmox CA certificate**  
(`/etc/pve/pve-root-ca.pem` on the Proxmox host) into your project and update the path accordingly.

The PostgreSQL Database is required for the **Advisory Locks**. You may change the user and password and start the db with docker-compose.



## Configure Virtual Machine Templates in Django Admin

To define lab environments, open the Django admin panel and configure:
1. **VMTemplate**  
   - Enter the Proxmox `template_id`  
   - Choose the `purpose` (e.g. `USER_SHELL`)  
   - Set required CPU cores and memory

2. **NetworkTemplate**  
   - Define a name  
   - Set a subnet (e.g. `10.10.0.0/24`)  
   - Enter a starting `vlan_id`

3. **TaskVMConfiguration**  
   - Select the corresponding Task  
   - Assign the previously created NetworkTemplate

4. **TaskVMTemplate**  
For each VM you want in the environment:  
     - Select the TaskVMConfiguration  
     - Select the VMTemplate  
     - Set the `planned_ip_address` (assigned via cloud-init)

