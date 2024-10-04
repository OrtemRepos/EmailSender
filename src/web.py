from aiosmtplib import SMTP

from litestar import get, post, Response, status_codes, Router
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from faststream.asyncapi import get_asyncapi_html
from faststream.asyncapi.schema import Schema
from src.service import email_sender
from src.schema import UserEmail
from json import load


@post("/reset-password")
async def reset_password(email: UserEmail) -> Response:
    async with SMTP(
        hostname=email_sender.host, port=int(email_sender.port), use_tls=True
    ) as session:
        await email_sender.send_email(
            email.email, email.token, "Reset Password", "reset_password.html", session
        )
    return Response(content=None, status_code=status_codes.HTTP_204_NO_CONTENT)


@post("/confirm-email")
async def confirm_email(email: UserEmail) -> Response:
    async with SMTP(
        hostname=email_sender.host, port=int(email_sender.port), use_tls=True
    ) as session:
        await email_sender.send_email(
            email.email, email.token, "Confirm Email", "confirm_email.html", session
        )
    return Response(content=None, status_code=status_codes.HTTP_204_NO_CONTENT)


@post("/batch-reset-password")
async def batch_reset_password(emails: list[UserEmail]) -> Response:
    await email_sender.send_email_batch(emails, "Reset Password", "reset_password.html")
    return Response(content=None, status_code=status_codes.HTTP_204_NO_CONTENT)


@post("/batch-confirm-email")
async def batch_confirm_email(emails: list[UserEmail]) -> Response:
    await email_sender.send_email_batch(emails, "Confirm Email", "confirm_email.html")
    return Response(content=None, status_code=status_codes.HTTP_204_NO_CONTENT)


with open("./asyncapi.json", "r") as f:
    schema = load(f)


@get("/asyncapi")
async def asyncapi() -> Response:
    return Response(content=get_asyncapi_html(Schema(**schema)), media_type="text/html")


api = Router(
    "/api",
    route_handlers=[
        confirm_email,
        reset_password,
        batch_confirm_email,
        batch_reset_password,
    ],
)

docs = Router("/docs", route_handlers=[asyncapi])

openapi_config = OpenAPIConfig(
    title="EmailSedner REST API",
    version="0.1.0",
    description="Send emails to users",
    path="/docs",
    render_plugins=[ScalarRenderPlugin()],
)
