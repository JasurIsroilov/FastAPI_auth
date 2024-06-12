import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from datetime import datetime, timedelta

from config import Settings
from .errors import UserErrors
from .schemas import UserSchema


http_bearer = HTTPBearer()


class TokenManager:

    __algorithm: str = Settings.JWT_ALGORITHM
    __token_type_field: str = "type"
    __access_token_type: str = "access"
    __refresh_token_type: str = "refresh"

    @classmethod
    def __create_jwt_token(cls, token_type: str, payload: dict, expire_minutes: int):
        jwt_payload = {cls.__token_type_field: token_type}
        jwt_payload.update(payload)
        return cls.jwt_encode(jwt_payload, expire_minutes)

    @classmethod
    def create_refresh_token(cls, user: UserSchema) -> str:
        jwt_payload = {
            "sub": user.id
        }
        return cls.__create_jwt_token(cls.__refresh_token_type, jwt_payload, Settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    @classmethod
    def create_access_token(cls, user: UserSchema) -> str:
        jwt_payload = {
            "sub": user.id,
            "username": user.username
        }
        return cls.__create_jwt_token(cls.__access_token_type, jwt_payload, Settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @classmethod
    def jwt_encode(cls, payload: dict, expire_minutes: int):
        to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        return jwt.encode(to_encode, Settings.PRIVATE_KEY_PATH.read_text(), algorithm=cls.__algorithm)

    @classmethod
    def jwt_decode(cls, token: str | bytes):
        return jwt.decode(token, Settings.PUBLIC_KEY_PATH.read_text(), algorithms=[cls.__algorithm])

    @classmethod
    def validate_access_token(cls, payload: dict):
        if payload.get(cls.__token_type_field) != cls.__access_token_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UserErrors.not_access_token)
        return

    @classmethod
    def validate_refresh_token(cls, payload: dict):
        if payload.get(cls.__token_type_field) != cls.__refresh_token_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UserErrors.not_refresh_token)
        return


async def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    try:
        payload = TokenManager.jwt_decode(credentials.credentials)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UserErrors.invalid_token + f" {e}")
    return payload
