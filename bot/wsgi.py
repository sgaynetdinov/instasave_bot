import falcon

from opbeat import Client
from opbeat.middleware import Opbeat

from . import vk_bot, config
from .middleware import JSONMiddleware, SecretKeyMiddleware, CheckGroupMiddleware, ConfirmationMiddleware, OpbeatAPMMiddleware


client = Client(
    organization_id=config.OPBEAT_ORGANIZATION_ID,
    app_id=config.OPBEAT_APP_ID,
    secret_token=config.OPBEAT_SECRET_TOKEN,
    DEBUG=False,
    TIMEOUT=5
)


application = start = falcon.API(middleware=[
    OpbeatAPMMiddleware(client),
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
    ConfirmationMiddleware()
])

application.add_route('/', vk_bot.Bot())

application = Opbeat(application, client)
