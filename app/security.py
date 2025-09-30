
from passlib.context import CryptContext
from datetime import datetime, timedelta
import hmac, hashlib, base64
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Token HMAC simple (demo). En producción usa JWT/OAuth2.
def create_token(username: str, minutes: int = 120) -> str:
    exp = int((datetime.utcnow() + timedelta(minutes=minutes)).timestamp())
    msg = f"{username}:{exp}".encode()
    sig = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(msg + b"." + sig).decode()
    return token

def validate_token(token: str) -> str | None:
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        msg, sig = raw.split(b".")
        expected = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected):
            return None
        user, exp = msg.decode().split(":")
        if int(exp) < int(datetime.utcnow().timestamp()):
            return None
        return user
    except Exception:
        return None
