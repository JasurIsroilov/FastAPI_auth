import bcrypt

from config import Settings
from .schemas import RegisterSchema


class PasswordManager:

    __encoding: str = "utf-8"

    @classmethod
    def hash(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode(cls.__encoding),
                             bcrypt.gensalt()).decode(cls.__encoding)

    @classmethod
    def check(cls, user: RegisterSchema, password: str) -> bool:
        return bcrypt.checkpw(user.password.encode(cls.__encoding), password.encode(cls.__encoding))
