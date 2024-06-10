from uuid import uuid4, UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel


class UserModel(BaseModel):

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
