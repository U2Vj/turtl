import hashlib
import re
import unicodedata
import time
from django.db import connection, utils

def _get_lock_id(name: str) -> int:
    """
    Generate a lock ID based on a string that can be used by postgres
    """
    return int(hashlib.sha256(name.encode()).hexdigest(), 16) % (2**63)

class AdvisoryLock:
    """
    Context manager for advisory locks with timeouts in PostgreSQL
    """
    def __init__(self, name: str, timeout_seconds: float | None = None, poll_interval: float = 0.2):
        self.lock_id = _get_lock_id(name)
        self.timeout_seconds = timeout_seconds
        self.poll_interval = max(0.05, float(poll_interval))
        self.acquired = False

    def __enter__(self):
        with connection.cursor() as cursor:
            if self.timeout_seconds == 0:
                cursor.execute("SELECT pg_try_advisory_lock(%s)", [self.lock_id])
                self.acquired = bool(cursor.fetchone()[0])
                return self.acquired

            if self.timeout_seconds is not None and self.timeout_seconds > 0:
                deadline = time.monotonic() + float(self.timeout_seconds)
                while time.monotonic() < deadline:
                    cursor.execute("SELECT pg_try_advisory_lock(%s)", [self.lock_id])
                    if cursor.fetchone()[0]:
                        self.acquired = True
                        return True
                    time.sleep(self.poll_interval)
                self.acquired = False
                return False

            cursor.execute("SELECT pg_advisory_lock(%s)", [self.lock_id])
            self.acquired = True
            return True

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.acquired:
            return False
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_unlock(%s);", [self.lock_id])
        self.acquired = False
        return False
            
def slugify(value, max_length=40):
    """
    Cleans string so it is valid to use in proxmox names
    """
    value = str(value)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")

    # ensure starts with letter
    if value and not value[0].isalpha():
        value = "n" + value
    
    # Truncate and ensure valid ending
    if max_length and len(value) > max_length:
        value = value[:max_length].rstrip("-")
        if not value or len(value) < 2:
            return "default"
        
    return value


def format_ip(ip_address, network):
    """
    Ensure an IP address string includes CIDR suffix.
    - If ip_address already contains '/', return it unchanged.
    - Otherwise, derive CIDR from network.subnet or default to /24.
    """
    ip_str = str(ip_address) if ip_address is not None else ""
    if "/" in ip_str:
        return ip_str

    subnet = getattr(network, 'subnet', None) or ""
    if "/" in subnet:
        cidr = subnet.split("/")[1]
        return f"{ip_str}/{cidr}"
    else:
        return f"{ip_str}/24"
