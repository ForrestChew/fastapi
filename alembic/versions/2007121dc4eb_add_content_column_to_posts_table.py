"""Add content column to posts table

Revision ID: 2007121dc4eb
Revises: b9b4d726f652
Create Date: 2022-09-22 13:51:16.758891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2007121dc4eb"
down_revision = "b9b4d726f652"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
