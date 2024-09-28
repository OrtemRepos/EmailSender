import time
from faststream import FastStream
from faststream.asgi import make_ping_asgi
from faststream.kafka import KafkaBroker

from src.schema import UserEmail
from src.logging_config import logger
from src.service import email_sender


broker = KafkaBroker(
    "localhost:9092",
    logger=logger,
)


app = FastStream(
    broker,
    logger=logger,
    title="EmailSender",
    description="EmailSender API",
    version="0.1.0",
    ).as_asgi(
    asgi_routes=[
        ("/health", make_ping_asgi(broker, timeout=5.0)),
    ],
    asyncapi_path="/docs",
)

@broker.subscriber("email_confirm", batch=True, group_id="email_confirm", description="Send email to confirm email")
async def confirmation_email(emails: list[UserEmail]) -> None:
    try:
        await email_sender.send_email_batch(emails, "Confirm Email", "confirm_email.html")
    except Exception as e:
        logger.exception('Failed to send emails', exc_info=e)
        logger.warning("Failed to send emails")
    logger.info("Emails seccsfully sent")
@broker.subscriber("forgot_password", batch=True, group_id="forgot_password", description="Send email to reset password")
async def forgot_password(emails: list[UserEmail]) -> None:
    try:
        await email_sender.send_email_batch(emails, "Forgot Password", "reset_password.html")
    except Exception as e:
        logger.exception('Failed to send emails', exc_info=e)
        logger.warning("Failed to send emails")
    logger.info("Emails seccsfully sent")

    