# Installation Guide
This guide explains how to setup TURTL in Production. 
For a guide on how to setup local development see [Development](development.md) 

## Prerequisites
TURTL requires a recent version of [Python](https://www.python.org/) (Python 3.12 or later), [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/install/linux/) and the latest LTS version of [NodeJS](https://nodejs.org/en).
For the virtualization features TURTL requires an Instance of [Proxmox VE](https://www.proxmox.com/en/products/proxmox-virtual-environment/overview) connected to a network that the machine running TURTL has access to.

### Requirements
Proxmox VE configured as described in [Proxmox](proxmox.md)

### Clone repository

```bash
git clone https://github.com/U2Vj/turtl.git
cd turtl
```

### Setup environment variables

```bash
cp .env.example .env
```
Then fill out the following variables

| Variable | Value |
| -------- | ------- |
| DJANGO_SECRET_KEY              | Insert a secure random string  |
| DJANGO_DEBUG                   | Toggle for debug mode, set to false in production |
| VM_MANAGER_LOG_LEVEL           | DEBUG, INFO, WARN, ERROR |
| DJANGO_ALLOWED_HOSTS           | Comma separated list of hostnames Django accepts requests from. MUST inlude localhost for backend healthcheck to work |
| CSRF_TRUSTED_ORIGINS           | List of trusted origins for Django CSRF |
| FRONTEND_URL                   | Base URL of the frontend |
| POSTGRES_DB                    | Name of PostgreSQL db |
| POSTGRES_USER                  | PostgreSQL username |
| POSTGRES_PASSWORD              | PostgreSQL password |
| POSTGRES_HOST                  | Optional for local dev outside docker |
| POSTGRES_PORT                  | Optional for local dev outside docker |
| REDIS_HOST                     | Optional for local dev outside docker |
| REDIS_PORT                     | Optional for local dev outside docker |
| REDIS_PASSWORD                 | Set secure password for redis |
| GRAFANA_DB_USER                | Create a separate read only user for Grafana (recommended) |
| GRAFANA_DB_PASSWORD            | Password for Grafana user |
| PROXMOX_HOST                   | IP or hostname of Proxmox VE Host + Port e.g. 10.0.0.1:8006 |
| PROXMOX_USER                   | Username of Proxmox User |
| PROXMOX_TOKEN_NAME             | Name of API key |
| PROXMOX_TOKEN_VALUE            | Value of API key |
| PROXMOX_VM_POOL                | Name of the pool where VMs for lab environments get created e.g. turtl-lab |
| PROXMOX_VM_STORAGE             | Disk storage for the cloned vms e.g. local-zfs-turtl |
| PROXMOX_VLAN_BRIDGE            | VLAN-Bridge used for networking for the lab environments  |
| PROXMOX_VERIFY_SSL             | if true, verifies Proxmox SSL certificate (requires proxmox-ca.pem in /deploy/certs). The certificates hostname or ip must match the configured PROXMOX_HOST |
| USER_THROTTLE_RATE             | Limit how many requests a logged in user can make e.g. 200/minute |
| ANON_THROTTLE_RATE             | Limit how many request anonymous users can make e.g. 100/minute |
| VM_ACTIONS_THROTTLE_RATE       | Limit how many lab environment actions a user can make (create/start/stop/delete) e.g. 4/minute |
| LOGIN_IP_THROTTLE_RATE         | Limit how many login requests can come from one ip address e.g. 100/minute |
| LOGIN_USER_THROTTLE_RATE       | Limit how many login requests can be made for a specific user e.g. 10/minute |
| THROTTLE_USER_ACTIVE_LAB_ENV   | Limit how many active lab environments a user can have in parallel (users need to stop/delete existing lab envs to create new ones) |
| VM_MANAGER_STOP_AFTER_MINUTES  | Set the time after which the cleanup system stops a lab environment (time starts once user disconnects from lab environment) |
| VM_MANAGER_CLEANUP_AFTER_MINUTES | Set the time after which the cleanup system deletes a lab environment (time starts after lab environment has been stopped)  |
| WS_MAX_PARALLEL_PER_USER       | Limits how many websockets and therefore noVNC shells a user can have open in parallel |
| NUMBER_OF_PROXIES              | Set the number of proxies the application is running behind. Default: 1 (nginx) |

### Setup certificates

```bash
mkdir -p deploy/certs
cd deploy/certs
```

#### IP based:

```bash
openssl req -x509 -nodes -newkey rsa:4096 -keyout turtl.key -out turtl.crt -days 365 -subj "/CN=<ip>" -addext "subjectAltName=IP:<ip>"
```
or:

#### Domain based:

```bash
openssl req -x509 -nodes -newkey rsa:4096 -keyout turtl.key -out turtl.crt -days 365 -subj "/CN=<domain>" -addext "subjectAltName=DNS:<domain>"
```

### Configure nginx
Copy the example nginx configuration:
```bash
cp deploy/frontend/nginx.conf.example deploy/frontend/nginx.conf
```
Insert the hostname or ip where the application is hosted (must match the certificates):
```
server_name <insert hostname or ip where application is hosted>;
```
and:
```
proxy_set_header Host <insert url or ip where application is hosted>;
```

### Start application

```bash
cd deploy
sudo docker compose up --build
```

#### Create admin user:

```bash
sudo docker compose exec backend python manage.py createsuperuser
```

#### Create student accounts:

The seeder app provides a script to mass create student accounts in the database and generate a printable html file. The following example generates 100 Student accounts enrolled for classroom id 1:

```bash
sudo docker compose exec backend python manage.py generate_students 100 --classroom_id 1 --domain "turtl" --password-length 10 --output users.html

sudo docker compose cp backend:/app/users.html ./users.html
```

#### Delete student accounts:

To delete all student accounts use the following command:

```bash
sudo docker compose exec backend python manage.py cleanup_students
```

#### Django Admin panel:
The admin panel can be reached at:
```bash
https://your-deployment-url/django-admin
```

### Configure Grafana
Grafana can be used to monitor the number of active and running lab environments with data coming from the analytics table. This feature is very rudimentary but can be expanded by more data sources and views in the future. Data sources and dashboards are imported using Grafana provisioning: https://grafana.com/docs/grafana/latest/administration/provisioning/

Grafana connects to the PostgreSQL Database with the credentials from GRAFANA_DB_USER and GRAFANA_DB_PASSWORD.
You could set the same user for both grafana and django, but it is recommended to create a separate readonly user in the grafana

Grafana binds to the localhost of the machine running the turtl application. If you want to access it you can setup ssh port forwarding like this:
```bash
ssh -L 3001:localhost:3000 username@server
```
then you can reach grafana on your local device in a webbrowser by going to: http://localhost:3001

The initial login is admin:admin, but it is recommended to change it to something more secure.
