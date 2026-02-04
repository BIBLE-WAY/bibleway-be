from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

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
