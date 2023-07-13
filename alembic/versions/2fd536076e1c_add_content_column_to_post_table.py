"""add content column to post table

Revision ID: 2fd536076e1c
Revises: 5101ab30916e
Create Date: 2023-07-12 16:29:40.045012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fd536076e1c'
down_revision = '5101ab30916e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column(
        'content', sa.String(),nullable=False))
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('post','content')
    op.drop_column('post','published')
    op.drop_column('post','created_at')
    pass
