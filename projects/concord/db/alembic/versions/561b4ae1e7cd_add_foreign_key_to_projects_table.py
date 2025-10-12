"""add foreign key to projects table

Revision ID: 561b4ae1e7cd
Revises: f13d6347876c
Create Date: 2025-10-12 02:27:14.352592

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "561b4ae1e7cd"
down_revision: Union[str, Sequence[str], None] = "f13d6347876c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("projects", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "projects_users_fk",
        source_table="projects",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("projects_users_fk", table_name="projects")
    op.drop_column("posts", "owner_id")
    pass
