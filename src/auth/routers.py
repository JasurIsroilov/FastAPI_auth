from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .schemas import RegisterSchema, TokenSchema, UserSchema
from .user_manager import UserManager, get_current_user, get_current_user_for_refresh
from .token_manager import TokenManager, get_current_token_payload


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: RegisterSchema, session: AsyncSession = Depends(get_async_session)):
    await UserManager.create_user(user, session)
    return {"msg": "Success"}


@router.post("/login", response_model=TokenSchema)
async def login(user: RegisterSchema, session: AsyncSession = Depends(get_async_session)):
    user_schema = await UserManager.login_user(user, session)
    access_token = TokenManager.create_access_token(user=user_schema)
    refresh_token = TokenManager.create_refresh_token(user=user_schema)
    return TokenSchema(access_token=access_token,
                       refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenSchema, response_model_exclude_none=True)
async def refresh(user: UserSchema = Depends(get_current_user_for_refresh)):
    access_token = TokenManager.create_access_token(user=user)
    return TokenSchema(access_token=access_token)


@router.get("/me")
async def me(payload: dict = Depends(get_current_token_payload), user: UserSchema = Depends(get_current_user)):
    response = user.dict()
    response.update(logged_in_at=payload.get("iat"))
    return response
