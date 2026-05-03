"""multiple profiles per account

Revision ID: 0002_multiple_profiles
Revises: 0001_initial_schema
Create Date: 2026-05-02
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_multiple_profiles"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profiles",
        sa.Column(
            "name",
            sa.String(length=255),
            server_default="Default Profile",
            nullable=False,
        ),
    )
    op.add_column(
        "profiles",
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("false"), nullable=False),
    )
    op.execute(
        """
        UPDATE profiles
        SET name = COALESCE(NULLIF(target_role, ''), 'Default Profile')
        """
    )
    op.execute(
        """
        UPDATE profiles
        SET is_active = true
        WHERE id IN (
            SELECT MIN(id)
            FROM profiles
            GROUP BY user_id
        )
        """
    )
    op.create_index(op.f("ix_profiles_user_id"), "profiles", ["user_id"], unique=False)
    op.drop_constraint("profiles_user_id_key", "profiles", type_="unique")
    op.alter_column("profiles", "name", server_default=None)
    op.alter_column("profiles", "is_active", server_default=None)


def downgrade() -> None:
    op.create_unique_constraint("profiles_user_id_key", "profiles", ["user_id"])
    op.drop_index(op.f("ix_profiles_user_id"), table_name="profiles")
    op.drop_column("profiles", "is_active")
    op.drop_column("profiles", "name")
