from rest_framework.throttling import SimpleRateThrottle

class LoginIPThrottle(SimpleRateThrottle):
    scope = 'login_ip'

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {'scope': self.scope, 'ident': ident}
    
class LoginUsernameThrottle(SimpleRateThrottle):
    scope = 'login_user'

    def get_cache_key(self, request, view):
        email = (request.data.get('email') or '').strip().lower()
        if not email:
            return None
        return self.cache_format % {'scope': self.scope, 'ident': email}
