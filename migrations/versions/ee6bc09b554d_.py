"""empty message

Revision ID: ee6bc09b554d
Revises: 077cf53d6b50
Create Date: 2023-09-13 15:46:33.095013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee6bc09b554d'
down_revision = '077cf53d6b50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment_reaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_positive', sa.Boolean(), nullable=False),
    sa.Column('by_recommendation_author', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_reaction')
    # ### end Alembic commands ###
