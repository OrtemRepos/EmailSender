from aiosmtplib import SMTP

from litestar import get, post, Router, Response
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.openapi.spec.tag import Tag

from faststream.asyncapi.schema import Schema
from faststream.asyncapi import get_asyncapi_html
from src.service import email_sender
from src.schema import UserEmail
from json import load


tags = [
    Tag("Confirm-Email", description="Send email to confirm email"),
    Tag("Reset-Password", description="Send email to reset password"),
    Tag("Docs", description="AsyncAPI docs"),
    Tag("Server", description="Server utils"),
]


@post("/reset-password", status_code=204, description="Send email to reset password", tags=["Reset-Password"])
async def reset_password(email: UserEmail) -> None:
    async with SMTP(
        hostname=email_sender.host, port=int(email_sender.port), use_tls=True
    ) as session:
        await email_sender.send_email(
            email.email, email.token, "Reset Password", "reset_password.html", session
        )


@post("/confirm-email", status_code=204, description="Send email to confirm email", tags=["Confirm-Email"])
async def confirm_email(email: UserEmail) -> None:
    async with SMTP(
        hostname=email_sender.host, port=int(email_sender.port), use_tls=True
    ) as session:
        await email_sender.send_email(
            email.email, email.token, "Confirm Email", "confirm_email.html", session
        )


@post(
    "/batch-reset-password",
    status_code=204,
    description="Send batch email to reset password",
    tags=["Reset-Password"],
)
async def batch_reset_password(emails: list[UserEmail]) -> None:
    await email_sender.send_email_batch(emails, "Reset Password", "reset_password.html")


@post("/batch-confirm-email", description="Send batch email to confirm email", status_code=204, tags=["Confirm-Email"])
async def batch_confirm_email(
    emails: list[UserEmail]
) -> None:
    await email_sender.send_email_batch(emails, "Confirm Email", "confirm_email.html")


with open("./asyncapi.json", "r") as f:
    schema = load(f)


@get(
    "/asyncapi",
    description="Get AsyncAPI schema",
)
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

docs = Router("/docs", route_handlers=[asyncapi],
              tags=["Docs"])

openapi_config = OpenAPIConfig(
    title="EmailSedner REST API",
    version="0.1.0",
    description="Send emails to users",
    path="/docs",
    render_plugins=[ScalarRenderPlugin()],
    tags=tags,
)
