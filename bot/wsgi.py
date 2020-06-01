import os

import falcon
import sentry_sdk
from sentry_sdk.integrations.falcon import FalconIntegration

from .middleware import (CheckGroupMiddleware, JSONMiddleware,
                         SecretKeyMiddleware)
from .vk_bot import Bot


sentry_dsn = os.environ.get('SENTRY_DSN')
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FalconIntegration()]
    )

application = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
])

application.add_route('/', Bot())
