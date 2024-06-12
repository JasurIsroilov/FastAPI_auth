from pydantic import BaseModel


class RegisterSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserSchema(BaseModel):
    id: str
    username: str
