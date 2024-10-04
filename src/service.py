from aiosmtplib import SMTP
from src.util import generate_email
from src.config import settings
from src.schema import UserEmail


class SenderEmail:
    def __init__(self) -> None:
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.user = settings.smtp_user
        self.password = settings.smtp_password
        self.url = f"{self.host}"

    async def send_email(
        self, email: str, token: str, subject: str, content_path: str, session: SMTP
    ) -> None:
        email_message = generate_email(token, content_path, subject)
        await session.send_message(
            email_message, sender=self.user, recipients=email, mail_options=[]
        )

    async def send_email_batch(
        self, email_list: list[UserEmail], subject: str, content_path: str
    ) -> None:
        async with SMTP(
            hostname=self.url, port=int(self.port), use_tls=True
        ) as session:
            await session.login(self.user, self.password)
            for email in email_list:
                await self.send_email(
                    email.email, email.token, subject, content_path, session
                )


email_sender = SenderEmail()
