"""Create posts table

Revision ID: 93b6ac1d0cc2
Revises: 
Create Date: 2022-09-22 13:44:03.714387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "93b6ac1d0cc2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
