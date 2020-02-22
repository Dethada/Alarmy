"""empty message

Revision ID: acf6d6cc504d
Revises: 9641337f2fed
Create Date: 2020-02-22 16:31:26.128480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acf6d6cc504d'
down_revision = '9641337f2fed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('email', sa.VARCHAR(length=320), autoincrement=False, nullable=False))
    # ### end Alembic commands ###