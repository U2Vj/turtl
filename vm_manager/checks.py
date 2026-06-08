import os

from django.core.checks import Error, register
from django.conf import settings

REQUIRED_ENV_VARS = [
    'VM_MANAGER_LOG_LEVEL',
    'POSTGRES_DB',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'REDIS_PASSWORD',
    'PROXMOX_HOST',
    'PROXMOX_USER',
    'PROXMOX_TOKEN_NAME',
    'PROXMOX_TOKEN_VALUE',
    'PROXMOX_VM_POOL',
    'PROXMOX_VM_STORAGE',
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
        ca_path = os.environ.get('PROXMOX_CA_PATH') or os.path.join(settings.BASE_DIR, 'proxmox-ca.pem')
        if not os.path.isfile(ca_path):
            errors.append(Error(
                f"Proxmox CA cert not found: {ca_path}",
                hint="Place the Proxmox CA certificate in the project root or set PROXMOX_CA_PATH to the correct location.",
                id='vm_manager.E101',
            ))
    return errors
