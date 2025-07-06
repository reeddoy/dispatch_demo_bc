from email.utils import formataddr
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback

from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from ..routers.api_models import Media
from ....constants.config import *



# _Mail class is no longer needed for per-email connection, so we remove it.



class Mail:

    def restart(self):
        # No persistent mail object needed anymore
        pass

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
    ) -> None:
        import threading
        def send():
            try:
                smtp_cls = smtplib.SMTP_SSL if EMAIL_PROTOCOL_IS_SSL else smtplib.SMTP
                with smtp_cls(
                    EMAIL_HOST,
                    EMAIL_SMTP_SSL_PORT if EMAIL_PROTOCOL_IS_SSL else EMAIL_SMTP_TLS_PORT,
                ) as smtp:
                    smtp.ehlo()
                    if not EMAIL_PROTOCOL_IS_SSL:
                        smtp.starttls()
                        smtp.ehlo()
                    smtp.login(FROM_EMAIL, EMAIL_PASSWORD)

                    LOGGER.warning(f" Using Email Host: {EMAIL_HOST} sender: {FROM_EMAIL}")
                    message = MIMEMultipart("alternative")
                    message["Subject"] = subject
                    message["From"] = formataddr((FROM_NAME, FROM_EMAIL))
                    message["To"] = formataddr((to_name, to_email))
                    message.attach(
                        MIMEText(
                            body,
                            "html" if as_html else "plain",
                        )
                    )
                    smtp.send_message(message)
            except Exception as e:
                traceback.print_exc()
                LOGGER.warning(f"Failed to send email: {e}")
        threading.Thread(target=send, daemon=True).start()

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
