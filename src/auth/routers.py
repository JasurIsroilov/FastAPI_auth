from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .schemas import RegisterSchema, TokenSchema, UserSchema
from .user_manager import UserManager, get_current_user
from .token_manager import TokenManager, get_current_token_payload


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: RegisterSchema, session: AsyncSession = Depends(get_async_session)):
    await UserManager.create_user(user, session)
    return {"msg": "Success"}


@router.post("/login", response_model=TokenSchema)
async def login(user: RegisterSchema, session: AsyncSession = Depends(get_async_session)):
    user_schema = await UserManager.login_user(user, session)
    jwt_payload = {
        "sub": user_schema.id,
        "username": user.username
    }
    token = TokenManager.jwt_encode(jwt_payload)
    return TokenSchema(access_token=token, token_type="Bearer")


@router.get("/me")
async def me(payload: dict = Depends(get_current_token_payload), user: UserSchema = Depends(get_current_user)):
    response = user.dict()
    response.update(logged_in_at=payload.get("iat"))
    return response
