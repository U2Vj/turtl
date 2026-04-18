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

    verify_env = os.environ.get('PROXMOX_VERIFY_SSL', 'true').strip().lower()
    if verify_env not in ('false', '0'):
        ca_path = os.environ.get('PROXMOX_CA_PATH')
        if not ca_path:
            errors.append(Error(
                "PROXMOX_VERIFY_SSL is enabled but PROXMOX_CA_PATH is not set.",
                hint="Set PROXMOX_CA_PATH to the Proxmox CA certificate",
                id='vm_manager.E100',
            ))
        elif not os.path.isfile(ca_path):
            errors.append(Error(
                f"PROXMOX_CA_PATH points to a file that does not exist: {ca_path}",
                hint="Check the path or copy the Proxmox CA certificate to that location.",
                id='vm_manager.E101',
            ))
    return errors
