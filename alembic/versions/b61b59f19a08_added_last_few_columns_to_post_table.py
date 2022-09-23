"""Added last few columns to post table

Revision ID: b61b59f19a08
Revises: d491dfea7a85
Create Date: 2022-09-22 14:10:51.518578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b61b59f19a08"
down_revision = "d491dfea7a85"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
