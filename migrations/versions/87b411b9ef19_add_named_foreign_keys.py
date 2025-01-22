"""Add named foreign keys

Revision ID: 87b411b9ef19
Revises: 
Create Date: 2025-01-15 23:55:17.735934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87b411b9ef19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Recreate the user_stats table with named foreign keys
    op.drop_table('user_stats')
    op.create_table(
        'user_stats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE', name='fk_user_stats_user_id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('tdee', sa.Float(), nullable=False),
        sa.Column('bmi', sa.Float(), nullable=False),
        sa.Column('bfp', sa.Float(), nullable=False),
        sa.Column('bmr', sa.Float(), nullable=False),
        sa.Column('ibw', sa.Float(), nullable=False),
        sa.Column('hydration', sa.Float(), nullable=False)
    )

    # Recreate the user_interactions table with named foreign keys
    op.drop_table('user_interactions')
    op.create_table(
        'user_interactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE', name='fk_user_interactions_user_id'), nullable=False),
        sa.Column('query', sa.String(500), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('goal', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('rating', sa.Integer(), nullable=True)
    )


def downgrade():
    # Drop the tables and recreate them without named constraints
    op.drop_table('user_stats')
    op.create_table(
        'user_stats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('tdee', sa.Float(), nullable=False),
        sa.Column('bmi', sa.Float(), nullable=False),
        sa.Column('bfp', sa.Float(), nullable=False),
        sa.Column('bmr', sa.Float(), nullable=False),
        sa.Column('ibw', sa.Float(), nullable=False),
        sa.Column('hydration', sa.Float(), nullable=False)
    )

    op.drop_table('user_interactions')
    op.create_table(
        'user_interactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('query', sa.String(500), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('goal', sa.Boolean(), nullable=True, server_default=sa.false()),
        sa.Column('rating', sa.Integer(), nullable=True)
    )
