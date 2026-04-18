import os

from django.core.checks import Error, register

REQUIRED_ENV_VARS = [
    'PROXMOX_HOST',
    'PROXMOX_USER',
    'PROXMOX_TOKEN_NAME',
    'PROXMOX_TOKEN_VALUE',
    'PROXMOX_VM_POOL',
    'PROXMOX_VLAN_BRIDGE',
    'PROXMOX_VERIFY_SSL',
]


@register()
def check_proxmox_env(app_configs, **kwargs):
    # If PROXMOX_HOST is not set, assume proxmox is not being used and skip checks
    if not bool(os.environ.get('PROXMOX_HOST')):
        return []
    errors = []
    for index, var in enumerate(REQUIRED_ENV_VARS, start=1):
        if not os.environ.get(var):
            errors.append(Error(
                f"Environment variable {var} is not set.",
                hint=f"Set {var} in .env or process environment.",
                id=f'vm_manager.E{index:03d}',
            ))
    return errors
