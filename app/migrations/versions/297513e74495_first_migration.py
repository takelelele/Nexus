"""First migration

Revision ID: 297513e74495
Revises: 
Create Date: 2025-03-20 18:50:50.733913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '297513e74495'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['Activities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Buildings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('latitude', sa.DECIMAL(precision=9, scale=6), nullable=False),
    sa.Column('longitude', sa.DECIMAL(precision=9, scale=6), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('building_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['building_fk'], ['Buildings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Organizations_Activities',
    sa.Column('organization_fk', sa.Integer(), nullable=False),
    sa.Column('activity_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_fk'], ['Activities.id'], ),
    sa.ForeignKeyConstraint(['organization_fk'], ['Organizations.id'], ),
    sa.PrimaryKeyConstraint('organization_fk', 'activity_fk')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Organizations_Activities')
    op.drop_table('Organizations')
    op.drop_table('Buildings')
    op.drop_table('Activities')
    # ### end Alembic commands ###
