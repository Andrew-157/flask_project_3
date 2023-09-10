from ..models import FictionType, Tag
from .. import db
from sqlalchemy import select


def get_fiction_type_by_name(name: str) -> FictionType | None:
    stmt = select(FictionType).where(FictionType.name == name)
    return db.session.scalars(stmt).unique().one_or_none()


def get_tag_by_name(name: str) -> Tag | None:
    stmt = select(Tag).where(Tag.name == name)
    return db.session.scalars(stmt).unique().one_or_none()
