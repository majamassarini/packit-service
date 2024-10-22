"""Add Koji build scratch attribute

Revision ID: 46b37040cb19
Revises: 855bc0b691c2
Create Date: 2022-03-21 09:34:53.526691

"""

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from alembic import op
from packit_service.models import ProjectAndEventsConnector

# revision identifiers, used by Alembic.
revision = "46b37040cb19"
down_revision = "855bc0b691c2"
branch_labels = None
depends_on = None


if TYPE_CHECKING:  # noqa: SIM108
    Base = object
else:
    Base = declarative_base()


class PipelineModel(Base):
    __tablename__ = "pipelines"
    id = Column(Integer, primary_key=True)  # our database PK
    datetime = Column(DateTime, default=datetime.utcnow)

    koji_build_id = Column(Integer, ForeignKey("koji_build_targets.id"), index=True)
    koji_build = relationship("KojiBuildTargetModel", back_populates="runs")


class KojiBuildTargetModel(ProjectAndEventsConnector, Base):
    __tablename__ = "koji_build_targets"
    id = Column(Integer, primary_key=True)
    build_id = Column(String, index=True)  # koji build id

    # commit sha of the PR (or a branch, release) we used for a build
    commit_sha = Column(String)
    # what's the build status?
    status = Column(String)
    # chroot, but we use the word target in our docs
    target = Column(String)
    # URL to koji web ui for the particular build
    web_url = Column(String)
    # url to koji build logs
    build_logs_url = Column(String)
    # datetime.utcnow instead of datetime.utcnow() because its an argument to the function
    # so it will run when the koji build is initiated, not when the table is made
    build_submitted_time = Column(DateTime, default=datetime.utcnow)
    build_start_time = Column(DateTime)
    build_finished_time = Column(DateTime)

    # metadata for the build which didn't make it to schema yet
    # metadata is reserved to sqlalch
    data = Column(JSON)

    # it is a scratch build?
    scratch = Column(Boolean)

    runs = relationship("PipelineModel", back_populates="koji_build")


def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "koji_build_targets",
        sa.Column("scratch", sa.Boolean(), nullable=True),
    )
    # ### end Alembic commands ###

    for koji_build in session.query(KojiBuildTargetModel).all():
        koji_build.scratch = True

    session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("koji_build_targets", "scratch")
    # ### end Alembic commands ###
