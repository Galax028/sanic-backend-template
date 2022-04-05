from functools import wraps
from typing import Awaitable, Callable

from sanic.exceptions import Unauthorized
from sanic.request import Request


async def _decode_token(request: Request) -> bool:
    if not request.token:
        return False

    if request.token == "my very secure auth token":
        return True

    return False


def protected(wrapped: Callable[..., Awaitable]):
    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def decode_token(request: Request, *args, **kwargs):
            if await _decode_token(request):
                return await func(request, *args, **kwargs)

            raise Unauthorized("Invalid token!", 401)

        return decode_token

    return decorator(wrapped)
