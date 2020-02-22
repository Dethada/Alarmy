"""empty message

Revision ID: 9641337f2fed
Revises: 
Create Date: 2020-02-22 14:06:42.996600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9641337f2fed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('device_id', sa.String(length=32), nullable=False),
    sa.Column('alarm', sa.Boolean(), nullable=False),
    sa.Column('poll_interval', sa.Integer(), nullable=False),
    sa.Column('alert_interval', sa.Integer(), nullable=False),
    sa.Column('alarm_duration', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('vflip', sa.Boolean(), nullable=False),
    sa.Column('motd', sa.String(length=32), nullable=False),
    sa.Column('alarm_code', sa.String(length=16), nullable=False),
    sa.Column('detect_humans', sa.Boolean(), nullable=False),
    sa.Column('temp_threshold', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('device_id')
    )
    op.create_table('gas',
    sa.Column('ticker', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.String(length=32), nullable=False),
    sa.Column('lpg', sa.Float(), nullable=False),
    sa.Column('co', sa.Float(), nullable=False),
    sa.Column('smoke', sa.Float(), nullable=False),
    sa.Column('capture_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.device_id'], ),
    sa.PrimaryKeyConstraint('ticker'),
    sa.UniqueConstraint('capture_time')
    )
    op.create_table('person_alert',
    sa.Column('cid', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.String(length=32), nullable=False),
    sa.Column('alert_time', sa.DateTime(), nullable=False),
    sa.Column('image', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.device_id'], ),
    sa.PrimaryKeyConstraint('cid')
    )
    op.create_table('temperature',
    sa.Column('ticker', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.String(length=32), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('capture_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.device_id'], ),
    sa.PrimaryKeyConstraint('ticker'),
    sa.UniqueConstraint('capture_time')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('get_alerts', sa.Boolean(), nullable=False),
    sa.Column('device_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.device_id'], ),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('env_alert',
    sa.Column('cid', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.String(length=32), nullable=False),
    sa.Column('alert_time', sa.DateTime(), nullable=False),
    sa.Column('reason', sa.String(length=100), nullable=False),
    sa.Column('gas_ticker', sa.BigInteger(), nullable=False),
    sa.Column('temp_ticker', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.device_id'], ),
    sa.ForeignKeyConstraint(['gas_ticker'], ['gas.ticker'], ),
    sa.ForeignKeyConstraint(['temp_ticker'], ['temperature.ticker'], ),
    sa.PrimaryKeyConstraint('cid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('env_alert')
    op.drop_table('users')
    op.drop_table('temperature')
    op.drop_table('person_alert')
    op.drop_table('gas')
    op.drop_table('device')
    # ### end Alembic commands ###