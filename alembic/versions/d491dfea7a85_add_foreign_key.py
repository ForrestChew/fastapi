"""add foreign-key

Revision ID: d491dfea7a85
Revises: e9198d2b1bae
Create Date: 2022-09-22 14:04:30.627489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d491dfea7a85"
down_revision = "e9198d2b1bae"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
