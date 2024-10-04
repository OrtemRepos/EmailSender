from faststream.kafka import KafkaBroker
from litestar import Litestar

from src.schema import UserEmail
from src.logging_config import logger
from src.service import email_sender
from src.web import api, docs, openapi_config

broker = KafkaBroker("localhost:9094", logger=logger, asyncapi_url="/asyncapi")

app = Litestar(
    route_handlers=[api, docs],
    openapi_config=openapi_config,
    on_startup=[broker.start],
    on_shutdown=[broker.close],
)


@broker.subscriber(
    "email_confirm", batch=True, description="Send email to confirm email"
)
async def confirmation_email(emails: list[UserEmail]) -> None:
    try:
        await email_sender.send_email_batch(
            emails, "Confirm Email", "confirm_email.html"
        )
    except Exception as e:
        logger.exception("Failed to send emails", exc_info=e)
        logger.warning("Failed to send emails")
    logger.info("Emails seccsfully sent")


@broker.subscriber(
    "forgot_password", batch=True, description="Send email to reset password"
)
async def forgot_password(emails: list[UserEmail]) -> None:
    try:
        await email_sender.send_email_batch(
            emails, "Forgot Password", "reset_password.html"
        )
    except Exception as e:
        logger.exception("Failed to send emails", exc_info=e)
        logger.warning("Failed to send emails")
    logger.info("Emails seccsfully sent")
