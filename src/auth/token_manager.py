import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from datetime import datetime, timedelta

from config import Settings
from .errors import UserErrors


http_bearer = HTTPBearer()


class TokenManager:

    __algorithm: str = Settings.JWT_ALGORITHM

    @classmethod
    def jwt_encode(cls, payload: dict):
        to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        return jwt.encode(to_encode, Settings.PRIVATE_KEY_PATH.read_text(), algorithm=cls.__algorithm)

    @classmethod
    def jwt_decode(cls, token: str | bytes):
        return jwt.decode(token, Settings.PUBLIC_KEY_PATH.read_text(), algorithms=[cls.__algorithm])


async def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    try:
        payload = TokenManager.jwt_decode(credentials.credentials)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UserErrors.invalid_token + f" {e}")
    return payload
