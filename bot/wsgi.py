import falcon

from .vk_bot import Bot
from .middleware import JSONMiddleware, SecretKeyMiddleware, CheckGroupMiddleware, ConfirmationMiddleware


application = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
    ConfirmationMiddleware()
])

application.add_route('/', Bot())
