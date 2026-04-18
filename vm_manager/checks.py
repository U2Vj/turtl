import os

from django.core.checks import Error, register

REQUIRED_ENV_VARS = [
    'PROXMOX_HOST',
    'PROXMOX_USER',
    'PROXMOX_TOKEN_NAME',
    'PROXMOX_TOKEN_VALUE',
    'PROXMOX_VM_POOL',
    'PROXMOX_VLAN_BRIDGE',
]


@register()
def check_proxmox_env(app_configs, **kwargs):
    errors = []
    for index, var in enumerate(REQUIRED_ENV_VARS, start=1):
        if not os.environ.get(var):
            errors.append(Error(
                f"Environment variable {var} is not set.",
                hint=f"Set {var} in .env or process environment.",
                id=f'vm_manager.E{index:03d}',
            ))
    return errors
