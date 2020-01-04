"""empty message

Revision ID: e38b5872e93f
Revises: fd75cc9ca20f
Create Date: 2020-01-05 01:00:39.043427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e38b5872e93f'
down_revision = 'fd75cc9ca20f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('temp_threshold', sa.Integer(), nullable=False, server_default="50"))
    op.alter_column('device', 'temp_threshold', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'temp_threshold')
    # ### end Alembic commands ###