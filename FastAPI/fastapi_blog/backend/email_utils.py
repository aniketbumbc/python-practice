from email.message import EmailMessage
import aiosmtplib
from config import settings
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


async def send_email(to_email: str, subject: str, plain_text: str, html_content: str | None = None) -> None:
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(plain_text)

    if html_content:
        message.add_alternative(html_content, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.mail_server,
        port=settings.mail_port,
        username=settings.mail_username or None,
        password=settings.mail_password.get_secret_value() or None,
        start_tls=settings.mail_use_tls,
    )


async def send_password_reset_email(to_email: str, username: str, token: str) -> None:
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"
    expire_minutes = settings.reset_token_expire_minutes

    plain_text = (
        f"Hi {username},\n\n"
        f"We received a request to reset your password.\n\n"
        f"Reset your password here:\n{reset_url}\n\n"
        f"This link expires in {expire_minutes} minutes.\n\n"
        f"If you did not request this, please ignore this email."
    )

    html_content = templates.get_template("email.html").render(
        subject="Password Reset Request",
        username=username,
        reset_url=reset_url,
        expire_minutes=expire_minutes,
    )

    await send_email(
        to_email=to_email,
        subject="Password Reset Request",
        plain_text=plain_text,
        html_content=html_content,
    )