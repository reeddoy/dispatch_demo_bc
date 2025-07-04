import logging, os, stripe


OTP_TIMEOUT_MINUTES = 30
OTP_TIMEOUT = 60 * OTP_TIMEOUT_MINUTES
SESSION_TIMEOUT = 24 * 60 * 60
# SESSION_TIMEOUT = 10 * 60
REFRESH_SESSION_TIMEOUT = 3

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9obl9kb2UiLCJleHAiOjE3MDM4MjY2Mjl9.joFEjOmttG-j9jIq5il9fnDD4sBYnJtWOZl-lHGnEss"


MONGODB = os.environ.get("MONGODB")

FROM_NAME = "XDispatch"

EMAIL_PROTOCOL_IS_SSL = os.environ.get("EMAIL_PROTOCOL_IS_SSL") == "True"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_SMTP_TLS_PORT = os.environ.get("EMAIL_SMTP_TLS_PORT")
EMAIL_SMTP_SSL_PORT = os.environ.get("EMAIL_SMTP_SSL_PORT")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

REWARDFUL = os.environ.get("REWARDFUL")

stripe.api_key = os.environ.get("stripe_secret_key")

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("   ")
# LOGGER = logging.getLogger(FROM_NAME)
