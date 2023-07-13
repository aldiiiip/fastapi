"""add foreign key to post table

Revision ID: b6cf9cb2b7c6
Revises: e952a44dc06c
Create Date: 2023-07-12 17:25:44.358102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6cf9cb2b7c6'
down_revision = 'e952a44dc06c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk',source_table="post",referent_table="user", 
                          local_cols=['owner_id'], remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='owner_id')
    op.drop_column('post','owner_id')
    pass
