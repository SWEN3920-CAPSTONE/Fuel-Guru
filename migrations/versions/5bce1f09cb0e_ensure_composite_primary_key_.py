"""Try to ensure composite primary key autogenerates. If it doesnt work
just drop the tables and run the server again.

Revision ID: 5bce1f09cb0e
Revises: 8721555df3e7
Create Date: 2022-04-12 11:53:24.082126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bce1f09cb0e'
down_revision = '8721555df3e7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('gas_price_suggestions','id',autoincrement=True)
    op.alter_column('comment','id',autoincrement=True)
    op.alter_column('ratings','id',autoincrement=True)
    op.alter_column('reviews','id',autoincrement=True)
    op.alter_column('promotions','id',autoincrement=True)
    op.alter_column('amenity_tags','id',autoincrement=True)


def downgrade():
    op.alter_column('gas_price_suggestions','id',autoincrement=False)
    op.alter_column('comment','id',autoincrement=False)
    op.alter_column('ratings','id',autoincrement=False)
    op.alter_column('reviews','id',autoincrement=False)
    op.alter_column('promotions','id',autoincrement=False)
    op.alter_column('amenity_tags','id',autoincrement=False)
