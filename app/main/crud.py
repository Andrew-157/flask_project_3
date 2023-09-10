from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .. import db
from ..models import FictionType, Tag, Recommendation


def get_fiction_type_by_name(name: str) -> FictionType | None:
    stmt = select(FictionType).where(FictionType.name == name)
    return db.session.scalar(stmt)


def get_tag_by_name(name: str) -> Tag | None:
    stmt = select(Tag).where(Tag.name == name)
    return db.session.scalar(stmt)


def get_recommendation_by_id(id: int) -> Recommendation | None:
    stmt = select(Recommendation).\
        where(Recommendation.id == id).\
        options(joinedload(Recommendation.tags),
                joinedload(Recommendation.user),
                joinedload(Recommendation.fiction_type))
    return db.session.scalar(stmt)
