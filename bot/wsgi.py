import falcon

from .bot import Bot
from .middleware import JSONMiddleware, SecretKeyMiddleware, CheckGroupMiddleware, ConfirmationMiddleware

application = start = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
    ConfirmationMiddleware()
])

application.add_route('/', Bot())
