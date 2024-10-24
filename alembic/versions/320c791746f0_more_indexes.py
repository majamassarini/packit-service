"""More indexes

Revision ID: 320c791746f0
Revises: 469bdb9ca350
Create Date: 2022-08-30 18:17:28.607677

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "320c791746f0"
down_revision = "469bdb9ca350"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_copr_build_targets_commit_sha"),
        "copr_build_targets",
        ["commit_sha"],
        unique=False,
    )
    op.create_index(
        op.f("ix_git_branches_project_id"),
        "git_branches",
        ["project_id"],
        unique=False,
    )
    op.drop_column("git_projects", "https_url")
    op.create_index(
        op.f("ix_job_triggers_trigger_id"),
        "job_triggers",
        ["trigger_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_copr_build_id"),
        "pipelines",
        ["copr_build_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_koji_build_id"),
        "pipelines",
        ["koji_build_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_propose_downstream_run_id"),
        "pipelines",
        ["propose_downstream_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_srpm_build_id"),
        "pipelines",
        ["srpm_build_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pipelines_test_run_id"),
        "pipelines",
        ["test_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_issues_project_id"),
        "project_issues",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_releases_project_id"),
        "project_releases",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pull_requests_project_id"),
        "pull_requests",
        ["project_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_pull_requests_project_id"), table_name="pull_requests")
    op.drop_index(op.f("ix_project_releases_project_id"), table_name="project_releases")
    op.drop_index(op.f("ix_project_issues_project_id"), table_name="project_issues")
    op.drop_index(op.f("ix_pipelines_test_run_id"), table_name="pipelines")
    op.drop_index(op.f("ix_pipelines_srpm_build_id"), table_name="pipelines")
    op.drop_index(
        op.f("ix_pipelines_propose_downstream_run_id"),
        table_name="pipelines",
    )
    op.drop_index(op.f("ix_pipelines_koji_build_id"), table_name="pipelines")
    op.drop_index(op.f("ix_pipelines_copr_build_id"), table_name="pipelines")
    op.drop_index(op.f("ix_job_triggers_trigger_id"), table_name="job_triggers")
    op.add_column(
        "git_projects",
        sa.Column("https_url", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_index(op.f("ix_git_branches_project_id"), table_name="git_branches")
    op.drop_index(
        op.f("ix_copr_build_targets_commit_sha"),
        table_name="copr_build_targets",
    )
    # ### end Alembic commands ###
