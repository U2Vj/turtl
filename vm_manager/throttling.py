from rest_framework.throttling import UserRateThrottle


class VMActionThrottle(UserRateThrottle):
    scope = 'vm_actions'
