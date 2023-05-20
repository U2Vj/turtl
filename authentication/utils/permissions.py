from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class AutoPermissionViewSetWithListMixin(AutoPermissionViewSetMixin):
    """
    This extends the default AutoPermissionViewSetMixin in Django Rules to also check read permissions when a request to
    a list endpoint is being done.
    """
    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "read"
    }
