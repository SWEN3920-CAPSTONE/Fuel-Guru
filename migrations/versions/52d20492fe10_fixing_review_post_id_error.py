"""fixing review post id error

Revision ID: 52d20492fe10
Revises: 47ca68e2f1b4
Create Date: 2022-06-05 17:33:49.426270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52d20492fe10'
down_revision = '47ca68e2f1b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('reviews_post_id_key', 'reviews', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('reviews_post_id_key', 'reviews', ['post_id'])
    # ### end Alembic commands ###