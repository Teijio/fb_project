"""Initial structure

Revision ID: 01
Revises: 
Create Date: 2024-04-13 13:12:03.371945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '01'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activitylog',
    sa.PrimaryKeyConstraint('id'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', postgresql.INET(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('pixel', sa.String(length=1000), nullable=False),
    sa.Column('token', sa.String(length=1000), nullable=False),
    sa.Column('fbclid', sa.String(length=1000), nullable=False),
    sa.Column('fbc', sa.String(length=1000), nullable=False),
    sa.Column('fbp', sa.String(length=1000), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_activitylog_ip_address'), 'activitylog', ['ip_address'], unique=True)
    op.create_table('pixeltoken',
    sa.PrimaryKeyConstraint('id'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pixel', sa.String(length=1000), nullable=False),
    sa.Column('token', sa.String(length=1000), nullable=False),
    )
    op.create_index(op.f('ix_pixeltoken_pixel'), 'pixeltoken', ['pixel'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pixeltoken_pixel'), table_name='pixeltoken')
    op.drop_table('pixeltoken')
    op.drop_index(op.f('ix_activitylog_ip_address'), table_name='activitylog')
    op.drop_table('activitylog')
    # ### end Alembic commands ###
