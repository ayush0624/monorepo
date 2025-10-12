"""create posts table

Revision ID: 036e18fcc65b
Revises: 
Create Date: 2025-10-12 01:39:33.646728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '036e18fcc65b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), unique=True, nullable=False),
        sa.Column(
            "description", 
            sa.String(), 
            server_default=sa.text("'no description provided'"),
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.Enum(
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL",
                name = "project_priority",
                checkfirst=True
            ),
            nullable=False,
            server_default=sa.text("'MEDIUM'"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("'now'")
        )
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("projects")
    pass
