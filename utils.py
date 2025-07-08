from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
RESET_PASSWORD_SALT = os.getenv("RESET_PASSWORD_SALT")
API_BASE = os.getenv("API_BASE")
smtp_email = os.getenv("smtp_email")
smtp_passkey = os.getenv("smtp_passkey")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def generate_reset_token(user_data: str) -> str:
    
    """
    In the context of using itsdangerous.URLSafeTimedSerializer, a salt is an extra string used to namespace or distinguish different kinds of tokens.

    Think of it like a label that says what this token is for — so even if two parts of app generate tokens with the same secret key, the salt ensures they don’t get confused or misused.
    only tokens generated with "reset-password-salt" can be verified using that salt. It's an extra layer of security and prevents token collisions.
    """
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(
                            {"email": user_data.email, "username": user_data.username},
                            salt=RESET_PASSWORD_SALT
                        )

# Decoding the token
def verify_reset_token(token: str, expiration: int = 3600) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        decoded_data = serializer.loads(token, salt=RESET_PASSWORD_SALT, max_age=expiration)
        return decoded_data
    except Exception:
        return None