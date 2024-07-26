# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

import logging
from typing import Optional, List, Set, Union, Dict

from ogr.abstract import GitProject

from packit.config import JobType, PackageConfig, JobConfig, JobConfigTriggerType
from packit.config.aliases import get_branches
from packit.constants import OPEN_PULL_REQUEST_FOR_KEY
from packit_service.config import ServiceConfig
from packit_service.models import ProjectEventModel
from packit_service.trigger_mapping import are_job_types_same
from packit_service.worker.events import EventData
from packit_service.worker.helpers.job_helper import BaseJobHelper

logger = logging.getLogger(__name__)


class SyncReleaseHelper(BaseJobHelper):
    job_type: JobType
    status_name: str

    def __init__(
        self,
        service_config: ServiceConfig,
        package_config: PackageConfig,
        project: GitProject,
        metadata: EventData,
        db_project_event: ProjectEventModel,
        job_config: JobConfig,
        branches_override: Optional[Set[str]] = None,
    ):
        super().__init__(
            service_config=service_config,
            package_config=package_config,
            project=project,
            metadata=metadata,
            db_project_event=db_project_event,
            job_config=job_config,
        )
        self.branches_override = branches_override
        self._check_names: Optional[List[str]] = None
        self._default_dg_branch: Optional[str] = None
        self._job: Optional[JobConfig] = None

    @property
    def default_dg_branch(self) -> str:
        """
        Get the default branch of the distgit project.
        """
        raise NotImplementedError("Use subclass.")

    def _get_branches(self, aliases: Union[List, Dict, Set]) -> Set[str]:
        """
        Return all valid branches from given aliases strs.
        """
        branches = get_branches(
            *aliases,
            default_dg_branch=self.default_dg_branch,
            default=self.default_dg_branch,
        )
        if self.branches_override:
            logger.debug(f"Branches override: {self.branches_override}")
            branches = branches & self.branches_override

        return branches

    @property
    def branches(self) -> Set[str]:
        """
        Return all valid branches from config.
        """
        return self._get_branches(self.job.dist_git_branches)

    def get_fast_forward_branches_from(self, source_branch: str) -> Set[str]:
        """
        Returns a list of target branches that can be fast forwarded merging
        the specified source_branch
        The keys can be aliases, expand them into a temporary structure
        to be sure that source_branch can be found in the first dictionary.
        In the inner loop of the downstream sync the expanded aliases are used.

        @WARNING If a key alias will be expanded in more than a key, a branch
        and a PR will be created for every each of them. The user sould choose
        which one to close or merge.

        The branches should be specified as in the following example
            {"rawhide": {"open_pull_request_for": ["f40", "f39"]},
             "epel9": {}
            }

        source_branch: source branch with commits to be merged
        """
        if not isinstance(self.job.dist_git_branches, dict):
            return set()

        expanded_dist_git_branches = {}
        for key, value in self.job.dist_git_branches.items():
            expanded_keys = self._get_branches([key])
            expanded_dist_git_branches.update(
                {expanded_key: value for expanded_key in expanded_keys}
            )

        if source_branch not in expanded_dist_git_branches:
            return set()

        if (
            source_branch_dict := expanded_dist_git_branches[source_branch]
        ) and isinstance(source_branch_dict[OPEN_PULL_REQUEST_FOR_KEY], list):
            return self._get_branches(source_branch_dict[OPEN_PULL_REQUEST_FOR_KEY])

        return set()

    @property
    def job(self) -> Optional[JobConfig]:
        """
        Check if there is JobConfig for propose downstream defined
        :return: JobConfig or None
        """
        if not self._job:
            for job in [self.job_config] + self.package_config.jobs:
                if are_job_types_same(job.type, self.job_type) and (
                    self._db_project_object
                    and (
                        self._db_project_object.job_config_trigger_type == job.trigger
                        # pull-from-upstream can be retriggered by a dist-git PR comment,
                        # in which case the trigger types don't match
                        or job.type == JobType.pull_from_upstream
                        and self._db_project_object.job_config_trigger_type
                        == JobConfigTriggerType.pull_request
                        and job.trigger == JobConfigTriggerType.release
                    )
                ):
                    self._job = job
                    break
        return self._job

    def report_status_for_branch(self, branch, description, state, url):
        raise NotImplementedError("Use subclass")

    def report_status_to_all(
        self,
        description,
        state,
        url="",
        markdown_content=None,
    ):
        raise NotImplementedError("Use subclass")
