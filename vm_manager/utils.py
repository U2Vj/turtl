import hashlib
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
    def __init__(self, name: str, timeout_seconds: float | None = None):
        self.lock_id = _get_lock_id(name)
        self.timeout_seconds = timeout_seconds

    def __enter__(self):
        with connection.cursor() as cursor:
            # Attempt to aquire the lock (not blocking)
            if self.timeout_seconds == 0:
                cursor.execute("SELECT pg_try_advisory_lock(%s)", [self.lock_id])
                return cursor.fetchone()[0]

            # Wait for unlock until timeout
            if self.timeout_seconds is not None and self.timeout_seconds > 0:
                try:
                    cursor.execute("SET LOCAL lock_timeout = %s;", [f"{self.timeout_seconds}s"])
                    cursor.execute("SELECT pg_advisory_lock(%s);", [self.lock_id])
                    return True
                except utils.OperationalError as e:
                    # Timeout reached
                    return False
            else:
                # Wait indefinitely
                cursor.execute("SELECT pg_advisory_lock(%s);", [self.lock_id])
                return True
                    

    def __exit__(self, exc_type, exc_value, traceback):
        with connection.cursor() as cursor:
            # Release the lock
            cursor.execute("SELECT pg_advisory_unlock(%s);", [self.lock_id])
            