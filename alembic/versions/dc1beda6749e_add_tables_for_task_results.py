"""Add tables for task results

Revision ID: dc1beda6749e
Revises: 4292b00185bf
Create Date: 2020-03-26 14:18:34.908120

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "dc1beda6749e"
down_revision = "4292b00185bf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "task_results",
        sa.Column("task_id", sa.String(), nullable=False),
        sa.Column("jobs", sa.PickleType(), nullable=True),
        sa.Column("event", sa.PickleType(), nullable=True),
        sa.PrimaryKeyConstraint("task_id"),
    )
    op.drop_column("copr_builds", "logs")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "copr_builds",
        sa.Column("logs", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.drop_table("task_results")
    # ### end Alembic commands ###
