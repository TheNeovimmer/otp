import os
import resend
from app.config import settings

resend.api_key = settings.RESEND_API_KEY


def send_otp_email(email: str, otp_code: str) -> bool:
    try:
        params = {
            "from": f"{settings.EMAIL_FROM_NAME} <onboarding@resend.dev>",
            "to": email,
            "subject": "Password Reset OTP",
            "html": f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Password Reset Request</h2>
                <p>Your OTP for password reset is:</p>
                <h1 style="background: #f0f0f0; padding: 10px; text-align: center; letter-spacing: 5px;">{otp_code}</h1>
                <p>This OTP will expire in {settings.OTP_EXPIRE_MINUTES} minutes.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </body>
            </html>
            """,
        }

        response = resend.Emails.send(params)
        print(f"Resend response: {response}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
