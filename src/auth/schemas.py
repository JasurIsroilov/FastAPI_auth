from pydantic import BaseModel


class RegisterSchema(BaseModel):

    username: str
    password: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    id: str
    username: str
