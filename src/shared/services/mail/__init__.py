from email.utils import formataddr
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback

from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from ..routers.api_models import Media
from ....constants.config import *


class _Mail(smtplib.SMTP_SSL if EMAIL_PROTOCOL_IS_SSL else smtplib.SMTP):
    def __init__(self) -> None:
        super().__init__(
            EMAIL_HOST,
            EMAIL_SMTP_SSL_PORT if EMAIL_PROTOCOL_IS_SSL else EMAIL_SMTP_TLS_PORT,
        )
        self.ehlo()
        if not EMAIL_PROTOCOL_IS_SSL:
            self.starttls()
            self.ehlo()

        self.login(FROM_EMAIL, EMAIL_PASSWORD)

        LOGGER.warning(f" Using Email Host: {EMAIL_HOST} sender: {FROM_EMAIL}")

    def send_mail(
        self,
        *,
        to_email: str | list[str],
        to_name: str,
        subject: str,
        body: str,
        cc_emails: list[str] = [],
        bcc_emails: list[str] = [],
        as_html: bool = False,
        attachments: list[Media] = [],
    ):
        LOGGER.warning(f" Using Email Host: {EMAIL_HOST} re: {to_email}")
        # Construct the MIMEMultipart message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = formataddr((FROM_NAME, FROM_EMAIL))
        # message["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        message["To"] = formataddr((to_name, to_email))
        # message["Cc"] = ", ".join(cc_emails)
        # message["Bcc"] = ", ".join(bcc_emails)

        message.attach(
            MIMEText(
                body,
                "html" if as_html else "plain",
            )
        )

        try:
            self.send_message(message)
        except Exception as e:
            traceback.print_exc()
            Mail.restart()
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error: retry again.",
            )
        finally:
            try:
                self.quit()
            except Exception:
                pass


class Mail:
    def __init__(self):
        self.mail = None
        self.mail = _Mail()

    def restart(self):
        try:
            self.mail = _Mail()
        except Exception as e:
            LOGGER.warning(e)

    def send_email(
        self,
        to_email: str | list[str],
        to_name: str,
        subject: str,
        body: str,
        cc_emails: list[str] = [],
        bcc_emails: list[str] = [],
        as_html: bool = False,
        attachments: list[Media] = [],
    ) -> tuple[str, str]:
        if self.mail:
            return self.mail.send_mail(
                to_email=to_email,
                to_name=to_name,
                subject=subject,
                body=body,
                cc_emails=cc_emails,
                bcc_emails=bcc_emails,
                as_html=as_html,
                attachments=attachments,
            )
        else:
            LOGGER.warning("No Email Service")

    def send_otp(
        self,
        to_email: str,
        to_name: str,
        otp: int,
    ):
        return self.send_email(
            to_email,
            to_name,
            "Account Verification OTP from DispatchXchange",
            f"<html><body>Your DispatchXchange Account Verification OTP is <h1>{otp}</h1>Valid for {OTP_TIMEOUT_MINUTES} minutes.</body></html>",
            [],
            [],
            True
        )

    def send_reset_otp(
        self,
        to_email: str,
        to_name: str,
        otp: int,
    ):
        return self.send_email(
            to_email,
            to_name,
            "Password Reset OTP from DispatchXchange",
            f"Your DispatchXchange Password Reset OTP is <h1>{otp}</h1>Valid for {OTP_TIMEOUT_MINUTES} minutes.",
            [],
            [],
            True
        )


Mail = Mail()
