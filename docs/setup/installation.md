# Installation Guide

## Prerequisites
TURTL requires a recent version of [Python](https://www.python.org/) (Python 3.12 or later), [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/install/linux/) and the latest LTS version of [NodeJS](https://nodejs.org/en).
For the virtualization features TURTL requires an Instance of [Proxmox VE](https://www.proxmox.com/en/products/proxmox-virtual-environment/overview) connected to a network that the machine running TURTL has access to.

## Getting started

### Clone repository

```bash
git clone <insert final gitlab url here>
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
| PUBLIC_HOSTNAME                | Domain or IP at which the app will be hosted at |
| POSTGRES_DB                    | Name of PostgreSQL db |
| POSTGRES_USER                  | PostgreSQL username |
| POSTGRES_PASSWORD              | PostgreSQL password |
| POSTGRES_HOST                  | Optional for local dev outside docker |
| POSTGRES_PORT                  | Optional for local dev outside docker |
| REDIS_HOST                     | Optional for local dev outside docker |
| REDIS_PORT                     | Optional for local dev outside docker |
| REDIS_PASSWORD                 | Set secure password for redis |
| GRAFANA_ADMIN_USER             | Grafana admin username |
| GRAFANA_ADMIN_PASSWORD         | Strong admin password |
| GRAFANA_DB_USER                | Create a seperate read only user for Grafana (recommended) |
| GRAFANA_DB_PASSWORD            | Password for Grafana user |
| PROXMOX_HOST                   | IP or hostname of Proxmox VE Host + Port e.g. 10.0.0.1:8006 |
| PROXMOX_USER                   | Username of Proxmox User |
| PROXMOX_TOKEN_NAME             | Name of API key |
| PROXMOX_TOKEN_VALUE            | Value of API key |
| PROXMOX_VM_POOL                | Name of the pool where VMs for lab environments get created e.g. turtl-lab |
| PROXMOX_VM_STORAGE             | Disk storage for the cloned vms e.g. local-zfs-turtl |
| PROXMOX_VLAN_BRIDGE            | VLAN-Bridge used for networking for the lab environments  |
| PROXMOX_VERIFY_SSL             | if true, verifies Proxmox SSL certificate (requires proxmox-ca.pem in project root) |
| USER_THROTTLE_RATE             | Limit how many requests a logged in user can make e.g. 200/minute |
| ANON_THROTTLE_RATE             | Limit how many request anonymous users can make e.g. 100/minute |
| VM_ACTIONS_THROTTLE_RATE       | Limit how many lab environment actions a user can make (create/start/stop/delete) e.g. 4/minute |
| LOGIN_IP_THROTTLE_RATE         | Limit how many login requests can come from one ip address e.g. 100/minute |
| LOGIN_USER_THROTTLE_RATE       | Limit how many login requests can be made for a specific user e.g. 10/minute |
| THROTTLE_USER_ACTIVE_LAB_ENV   | Limit how many active lab environments a user can have in parallel (users need to stop/delete existing lab envs to create new ones) |
| VM_MANAGER_STOP_AFTER_MINUTES  | Set the time after which the cleanup system stops a lab environment (time starts once user disconnects from lab environment) |
| VM_MANAGER_CLEANUP_AFTER_MINUTES | Set the time after which the cleanup system deletes a lab environment (time starts after lab environment has been stopped)  |
| NUMBER_OF_PROXIES              | Set the number of proxies the application is running behind. Default: 1 (nginx) |
