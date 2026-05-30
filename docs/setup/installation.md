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
| POSTGRES_HOST                  | optional for local dev outside docker |
| POSTGRES_PORT                  | optional for local dev outside docker |
| REDIS_HOST                     | optional for local dev outside docker |
| REDIS_PORT                     | optional for local dev outside docker |
| GRAFANA_ADMIN_USER             |  |
| GRAFANA_ADMIN_PASSWORD         |  |
| GRAFANA_DB_USER                |  |
| GRAFANA_DB_PASSWORD            |  |
| PROXMOX_HOST                   |  |
| PROXMOX_USER                   |  |
| PROXMOX_TOKEN_NAME             |  |
| PROXMOX_TOKEN_VALUE            |  |
| PROXMOX_VM_POOL                |  |
| PROXMOX_VM_STORAGE             |  |
| PROXMOX_VLAN_BRIDGE            |  |
| PROXMOX_VERIFY_SSL             |  |
| USER_THROTTLE_RATE             |  |
| ANON_THROTTLE_RATE             |  |
| VM_ACTIONS_THROTTLE_RATE       |  |
| LOGIN_IP_THROTTLE_RATE         |  |
| LOGIN_USER_THROTTLE_RATE       |  |
| THROTTLE_USER_ACTIVE_LAB_ENV   |  |
| VM_MANAGER_STOP_AFTER_MINUTES  |  |
| VM_MANAGER_CLEANUP_AFTER_MINUTES |  |
| NUMBER_OF_PROXIES              |  |
