"""Remove comments and ratings, reviews only

Revision ID: 47ca68e2f1b4
Revises: 1c841e5a584d
Create Date: 2022-06-05 15:56:18.230436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '47ca68e2f1b4'
down_revision = '1c841e5a584d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ratings')
    op.drop_table('comments')
    op.add_column('reviews', sa.Column('rating_val', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('body', sa.String(length=500), nullable=True))
    op.execute("UPDATE reviews SET rating_val = 1")
    op.alter_column('reviews', 'rating_val', nullable=False)
    op.execute("UPDATE reviews SET body = 'filler'")
    op.alter_column('reviews', 'body', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'body')
    op.drop_column('reviews', 'rating_val')
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('last_edited', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('review_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['review_id', 'post_id'], ['reviews.id', 'reviews.post_id'], name='comments_review_id_post_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'review_id', 'post_id', name='comments_pkey'),
    sa.UniqueConstraint('id', name='comments_id_key')
    )
    op.create_table('ratings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('rating_val', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('last_edited', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('review_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['review_id', 'post_id'], ['reviews.id', 'reviews.post_id'], name='ratings_review_id_post_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'review_id', 'post_id', name='ratings_pkey'),
    sa.UniqueConstraint('id', name='ratings_id_key')
    )
    # ### end Alembic commands ###
