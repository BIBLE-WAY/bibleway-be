from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
import os

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_string):
    try:
        UntypedToken(token_string)
        access_token = AccessToken(token_string)
        user_id = access_token.get('user_id')
        if not user_id:
            return None
        try:
            return User.objects.get(user_id=user_id, is_active=True)
        except User.DoesNotExist:
            return None
    except (TokenError, InvalidToken, Exception):
        return None


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get origin from headers
        headers = dict(scope.get('headers', []))
        origin = headers.get(b'origin', b'').decode()

        # Get allowed origins from CORS settings
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])

        # For development, also allow localhost
        if settings.DEBUG:
            allowed_origins = list(allowed_origins) + ['http://localhost:5173', 'http://127.0.0.1:5173']

        # Validate origin (allow if no origin or if in allowed list)
        if origin and origin not in allowed_origins:
            print(f"WebSocket connection rejected - Origin {origin} not in allowed origins: {allowed_origins}")
            await send({
                'type': 'websocket.close',
                'code': 4403,
            })
            return

        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = None

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)
