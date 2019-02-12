import falcon

from .vk_bot import Bot
from .middleware import JSONMiddleware, SecretKeyMiddleware, CheckGroupMiddleware


application = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
])

application.add_route('/', Bot())
