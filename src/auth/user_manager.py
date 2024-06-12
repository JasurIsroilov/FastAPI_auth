from fastapi import HTTPException, Depends, status

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import get_async_session
from .models import UserModel
from .schemas import RegisterSchema, UserSchema
from .password_manager import PasswordManager
from .token_manager import get_current_token_payload, TokenManager
from .errors import UserErrors


class UserManager:

    @classmethod
    async def __on_register(cls):
        ...

    @classmethod
    async def __on_login(cls):
        ...

    @classmethod
    async def create_user(cls, user: RegisterSchema, session: AsyncSession):
        user.password = PasswordManager.hash(user.password)
        stmt = insert(UserModel).values(**user.dict())
        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=UserErrors.username_unique)
        return

    @classmethod
    async def login_user(cls, user: RegisterSchema, session: AsyncSession) -> UserSchema:
        stmt = select(UserModel).where(UserModel.username == user.username)
        res = await session.execute(stmt)
        res = res.first()
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserErrors.unknown_user)
        if not PasswordManager.check(user, res[0].password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserErrors.incorrect_password)
        return UserSchema(id=str(res[0].id), username=res[0].username)


async def get_current_user(payload: dict = Depends(get_current_token_payload),
                           session: AsyncSession = Depends(get_async_session)) -> UserSchema:
    TokenManager.validate_access_token(payload)
    user_id: str = payload.get("sub")
    stmt = select(UserModel).where(UserModel.id == user_id)
    res = await session.execute(stmt)
    res = res.first()
    if res is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UserErrors.invalid_token)
    return UserSchema(id=str(res[0].id), username=res[0].username)


async def get_current_user_for_refresh(payload: dict = Depends(get_current_token_payload),
                                       session: AsyncSession = Depends(get_async_session)) -> UserSchema:
    TokenManager.validate_refresh_token(payload)
    user_id: str = payload.get("sub")
    stmt = select(UserModel).where(UserModel.id == user_id)
    res = await session.execute(stmt)
    res = res.first()
    if res is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UserErrors.invalid_token)
    return UserSchema(id=str(res[0].id), username=res[0].username)
