import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *  # noqa: F401, F403

sentry_sdk.init(
    dsn=config("SENTRY_DSN"),  # noqa: F405
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=0,
)
