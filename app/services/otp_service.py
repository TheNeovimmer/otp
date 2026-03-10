import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTP
from app.models.user import User
from app.utils.password import hash_password
from app.config import settings


def generate_otp() -> str:
    return "".join(random.choices(string.digits, k=settings.OTP_LENGTH))


def create_otp(db: Session, user_id: int) -> OTP:
    existing_otps = (
        db.query(OTP).filter(OTP.user_id == user_id, OTP.used == False).all()
    )
    for otp in existing_otps:
        otp.used = True

    code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

    new_otp = OTP(user_id=user_id, code=code, expires_at=expires_at, used=False)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return new_otp


def verify_otp(db: Session, email: str, code: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False

    otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user.id,
            OTP.code == code,
            OTP.used == False,
            OTP.expires_at > datetime.utcnow(),
        )
        .first()
    )

    if not otp:
        return False

    otp.used = True
    db.commit()
    return True


def reset_password(db: Session, email: str, new_password: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False

    user.password_hash = hash_password(new_password)
    db.commit()
    return True


def create_login_otp(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    return create_otp(db, user.id)
