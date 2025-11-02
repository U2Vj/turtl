"""
WebSocket JWT Authentication Middleware
"""
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from authentication.models import User


@database_sync_to_async
def get_user(validated_token):
    """
    Get user from validated JWT token
    """
    try:
        user_id = validated_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return AnonymousUser()


class JwtAuthMiddleware:
    """
    Custom middleware to authenticate WebSocket connections using JWT tokens
    """
    
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            token = None

            # Get Token from Websocket subprotocols
            for proto in (scope.get('subprotocols', []) or []):
                if isinstance(proto, str) and proto.startswith('jwt.'):
                    token = proto[4:]
                    break
            
            # If we have a token, validate it
            if token:
                try:
                    # Validate and read payload using SimpleJWT
                    access = AccessToken(token)
                    scope['user'] = await get_user(access.payload)
                    print(f"JWT Auth: Authenticated user {scope['user']} from token")
                except (InvalidToken, TokenError, Exception) as e:
                    print(f"JWT Auth: Invalid token: {e}")
                    scope['user'] = AnonymousUser()
            else:
                print("JWT Auth: No token found, using AnonymousUser")
                scope['user'] = AnonymousUser()
                
        except Exception as e:
            print(f"JWT Auth: Exception during authentication: {e}")
            scope['user'] = AnonymousUser()
        
        return await self.inner(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    """
    Create JWT authentication middleware stack
    """
    # Ensure JWT sets the user last to avoid being overwritten
    return AuthMiddlewareStack(JwtAuthMiddleware(inner))
