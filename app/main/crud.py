from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from .. import db
from ..models import FictionType, Tag, Recommendation, Reaction


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


def get_reaction_by_user_id_and_recommendation_id(user_id: int, recommendation_id: int) -> Reaction | None:
    stmt = select(Reaction).where(
        and_(Reaction.user_id == user_id,
             Reaction.recommendation_id == recommendation_id))
    return db.session.scalar(stmt)


def count_positive_reactions_for_recommendation(recommendation_id: int) -> int:
    stmt = select(Reaction).where(
        and_(Reaction.recommendation_id == recommendation_id,
             Reaction.is_positive == True))
    return len(db.session.scalars(stmt).all())


def count_negative_reactions_for_recommendation(recommendation_id: int) -> int:
    stmt = select(Reaction).where(
        and_(Reaction.recommendation_id == recommendation_id,
             Reaction.is_positive == False)
    )
    return len(db.session.scalars(stmt).all())
