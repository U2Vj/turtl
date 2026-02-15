"""
WebSocket JWT Authentication Middleware
"""
import logging

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from authentication.models import User

logger = logging.getLogger("vm_manager.auth")


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
                    logger.info("JWT Auth: Authenticated user_id=%s", getattr(scope["user"], "id", None))
                except (InvalidToken, TokenError):
                    logger.warning("JWT Auth: Invalid token provided")
                    scope['user'] = AnonymousUser()
                except Exception:
                    logger.exception("JWT Auth: Unexpected error while validating token")
                    scope['user'] = AnonymousUser()
            else:
                logger.debug("JWT Auth: No token found, using AnonymousUser")
                scope['user'] = AnonymousUser()
                
        except Exception:
            logger.exception("JWT Auth: Exception during authentication middleware execution")
            scope['user'] = AnonymousUser()
        
        return await self.inner(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    """
    Create JWT authentication middleware stack
    """
    # Ensure JWT sets the user last to avoid being overwritten
    return AuthMiddlewareStack(JwtAuthMiddleware(inner))
