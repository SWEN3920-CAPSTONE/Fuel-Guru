"""Add support for Review posts

Revision ID: 1bffd7ac8254
Revises: 004542971f12
Create Date: 2022-04-10 03:06:26.848330

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1bffd7ac8254'
down_revision = '004542971f12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('amenity_tags', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('comments', sa.Column('review_id', sa.Integer(), nullable=False))
    op.alter_column('comments', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('comments_post_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'reviews', ['review_id', 'post_id'], ['id', 'post_id'])
    op.drop_column('comments', 'last_edited')
    op.alter_column('gas_price_suggestions', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('promotions', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('ratings', sa.Column('review_id', sa.Integer(), nullable=False))
    op.alter_column('ratings', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('ratings_post_id_fkey', 'ratings', type_='foreignkey')
    op.create_foreign_key(None, 'ratings', 'reviews', ['review_id', 'post_id'], ['id', 'post_id'])
    op.drop_column('ratings', 'last_edited')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('last_edited', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.create_foreign_key('ratings_post_id_fkey', 'ratings', 'posts', ['post_id'], ['id'])
    op.alter_column('ratings', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('ratings', 'review_id')
    op.alter_column('promotions', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('gas_price_suggestions', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('comments', sa.Column('last_edited', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_post_id_fkey', 'comments', 'posts', ['post_id'], ['id'])
    op.alter_column('comments', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('comments', 'review_id')
    op.alter_column('amenity_tags', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###