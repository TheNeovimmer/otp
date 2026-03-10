from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.otp import OTPRequest, OTPVerify
from app.services.otp_service import create_otp, verify_otp, reset_password
from app.services.email_service import send_otp_email
from app.config import settings

router = APIRouter(prefix="/otp", tags=["otp"])


@router.post("/request")
def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found",
        )

    otp = create_otp(db, user.id)
    email_sent = send_otp_email(request.email, otp.code)

    if settings.DEBUG and not email_sent:
        return {"message": f"OTP (dev mode): {otp.code}"}

    return {"message": "OTP sent to your email"}


@router.post("/verify")
def verify_otp_and_reset_password(request: OTPVerify, db: Session = Depends(get_db)):
    if not verify_otp(db, request.email, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP"
        )

    if not reset_password(db, request.email, request.new_password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password",
        )

    return {"message": "Password reset successfully"}
