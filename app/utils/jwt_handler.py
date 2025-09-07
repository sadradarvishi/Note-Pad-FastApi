from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.settings import settings


def create_access_token(data: dict, minutes: int | None = None) -> str:
    now = datetime.now(UTC)
    exp = now + timedelta(minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {**data, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
