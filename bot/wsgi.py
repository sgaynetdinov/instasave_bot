import falcon

from .middleware import (CheckGroupMiddleware, JSONMiddleware,
                         SecretKeyMiddleware)
from .vk_bot import Bot

application = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
])

application.add_route('/', Bot())
