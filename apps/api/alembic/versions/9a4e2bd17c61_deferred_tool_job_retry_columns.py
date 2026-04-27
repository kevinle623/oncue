"""deferred tool job retry columns

Revision ID: 9a4e2bd17c61
Revises: 6c018ddca19d
Create Date: 2026-04-27 00:00:00.000000+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9a4e2bd17c61"
down_revision: str | None = "6c018ddca19d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "deferred_tool_jobs",
        sa.Column(
            "attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "deferred_tool_jobs",
        sa.Column(
            "max_attempts",
            sa.Integer(),
            nullable=False,
            server_default="3",
        ),
    )


def downgrade() -> None:
    op.drop_column("deferred_tool_jobs", "max_attempts")
    op.drop_column("deferred_tool_jobs", "attempts")
