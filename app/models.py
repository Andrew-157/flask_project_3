from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=255), unique=True)
    email: Mapped[str] = mapped_column(String(length=255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=300))

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    reactions: Mapped[list["Reaction"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return self.username


class FictionType(Base):
    __tablename__ = 'fiction_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), unique=True)
    slug: Mapped[str] = mapped_column(String(length=300), unique=True)

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates='fiction_type', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return self.name


tagged_recommendations = Table(
    'tagged_recommendations',
    Base.metadata,
    Column('recommendation_id',
           ForeignKey('recommendation.id',
                      ondelete='CASCADE',
                      onupdate='CASCADE'), primary_key=True),
    Column('tag_id',
           ForeignKey('tag.id',
                      ondelete='CASCADE',
                      onupdate='CASCADE'), primary_key=True)
)


class Recommendation(Base):
    __tablename__ = 'recommendation'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255))
    short_description: Mapped[str] = mapped_column(String())
    opinion: Mapped[str] = mapped_column(String())
    published: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow())
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',
                                                    ondelete='CASCADE',
                                                    onupdate='CASCADE'))
    fiction_type_id: Mapped[int] = mapped_column(ForeignKey('fiction_type.id',
                                                            ondelete='CASCADE',
                                                            onupdate='CASCADE'))

    user: Mapped[User] = relationship(
        back_populates='recommendations')

    fiction_type: Mapped[FictionType] = relationship(
        back_populates='recommendations')

    tags: Mapped[list["Tag"]] = relationship(
        secondary=tagged_recommendations
    )

    reactions: Mapped[list["Reaction"]] = relationship(
        back_populates='recommendation', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return self.title


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=300))

    def __repr__(self) -> str:
        return self.name


class Reaction(Base):
    __tablename__ = 'reaction'

    id: Mapped[int] = mapped_column(primary_key=True)
    is_positive: Mapped[bool] = mapped_column(Boolean(), default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',
                                                    ondelete='CASCADE',
                                                    onupdate='CASCADE'))
    recommendation_id: Mapped[int] = mapped_column(ForeignKey('recommendation.id',
                                                              ondelete='CASCADE',
                                                              onupdate='CASCADE'))

    user: Mapped[User] = relationship(
        back_populates='reactions')

    recommendation: Mapped[Recommendation] = relationship(
        back_populates='reactions')

    __table_args__ = (UniqueConstraint('user_id', 'recommendation_id',
                                       name='user_recommendation_uc'),)
