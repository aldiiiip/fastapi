"""create table

Revision ID: 5101ab30916e
Revises: 
Create Date: 2023-07-12 16:18:17.197531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5101ab30916e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('post',sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                            sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('post')
    pass
