"""empty message

Revision ID: 2eeca843d976
Revises: 13e9fcf3fd01
Create Date: 2020-01-04 16:13:13.517225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2eeca843d976'
down_revision = '13e9fcf3fd01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('alarm_code', sa.String(length=16), nullable=False, server_default="1234"))
    op.alter_column('device', 'alarm_code', server_default=None)
    op.add_column('device', sa.Column('motd', sa.String(length=32), nullable=False, server_default="MOTD"))
    op.alter_column('device', 'motd', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'motd')
    op.drop_column('device', 'alarm_code')
    # ### end Alembic commands ###
