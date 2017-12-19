import falcon

from . import vk_bot
from .middleware import JSONMiddleware, SecretKeyMiddleware, CheckGroupMiddleware, ConfirmationMiddleware

application = start = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
    ConfirmationMiddleware()
])

application.add_route('/', vk_bot.Bot())
