import aiosmtplib
from email.message import EmailMessage
from typing import Optional
import os
from pydantic import EmailStr
import ssl

# aiosmtplib을 사용한 비동기 이메일 전송
# EmailStr 사용


class EmailProcessor:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.receiver_email = ""

    async def send_email(
        self,
        subject: str,
        content: str,
        sender_email: EmailStr,
        sender_password: str,
        html_content: Optional[str] = None,
    ) -> bool:
        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured, cannot send email.")
            return False

        if not sender_email or not sender_password:
            print(
                "Warning: Email credentials (SENDER_EMAIL, SENDER_PASSWORD) "
                "are not configured in environment variables."
            )
            return False

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = self.receiver_email
        message.set_content(content)

        # HTML 내용이 있는 경우, 대체 콘텐츠로 추가
        if html_content:
            message.add_alternative(html_content, subtype="html")

        try:
            # 포트 465는 SMTPS (implicit TLS)를 사용하고, 포트 587은 STARTTLS를 사용합니다.
            use_tls = self.smtp_port == 465
            context = ssl.create_default_context() if use_tls else None

            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=sender_email,
                password=sender_password,
                use_tls=use_tls,
                ssl_context=context,
                timeout=10,
            )

            print(f"Email sent successfully to {self.receiver_email}")
            return True

        except aiosmtplib.SMTPException as e:
            print(f"SMTP error occurred while sending to {self.receiver_email}: {e}")
            return False
        except Exception as e:
            print(
                f"An unexpected error occurred while sending email to {self.receiver_email}: {e}"
            )
            return False
