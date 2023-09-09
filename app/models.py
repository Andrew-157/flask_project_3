from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from . import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=255), unique=True)
    email: Mapped[str] = mapped_column(String(length=255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=300))

    def __repr__(self) -> str:
        return self.username
