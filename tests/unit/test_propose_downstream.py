# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

import pytest
from flexmock import flexmock

from packit.config import CommonPackageConfig, PackageConfig, JobConfig, JobType
from packit.config.job_config import JobConfigTriggerType
from packit_service.config import ServiceConfig
from packit_service.worker.helpers.sync_release.propose_downstream import (
    ProposeDownstreamJobHelper,
)


@pytest.mark.parametrize(
    "jobs,job_config_trigger_type,branches_override,branches,ff_branches, all_ff_branches",
    [
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={
                        "package": CommonPackageConfig(
                            dist_git_branches=["main", "f34"],
                        )
                    },
                ),
            ],
            JobConfigTriggerType.release,
            None,
            {"main", "f34"},
            {"main": set(), "f34": set()},
            set(),
        ),
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={
                        "package": CommonPackageConfig(
                            dist_git_branches=["f34", "main"],
                        )
                    },
                ),
            ],
            JobConfigTriggerType.release,
            {"main"},
            {"main"},
            {"main": set()},
            set(),
        ),
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={
                        "package": CommonPackageConfig(
                            dist_git_branches=["f35", "f34"],
                        )
                    },
                ),
            ],
            JobConfigTriggerType.release,
            {"f35"},
            {"f35"},
            {"f35": set()},
            set(),
        ),
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={"packages": CommonPackageConfig()},
                ),
            ],
            JobConfigTriggerType.release,
            None,
            {"main"},
            {"main": set()},
            set(),
        ),
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={
                        "package": CommonPackageConfig(
                            dist_git_branches={
                                "rawhide": {"open_pull_request_for": ["f33"]},
                                "f35": {},
                                "f34": {},
                            },
                        )
                    },
                ),
            ],
            JobConfigTriggerType.release,
            None,
            {"main", "f35", "f34"},
            {"main": {"f33"}, "f35": set(), "f34": set()},
            {"f33"},
        ),
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={
                        "package": CommonPackageConfig(
                            # no sense but possible!
                            dist_git_branches={
                                "fedora-branched": {
                                    "open_pull_request_for": ["fedora-stable"]
                                }
                            },
                        )
                    },
                ),
            ],
            JobConfigTriggerType.release,
            None,
            {"f39", "f40"},
            {"f39": {"f39", "f40"}, "f40": {"f39", "f40"}},
            {"f39", "f40"},
        ),
        pytest.param(
            [
                JobConfig(
                    type=JobType.propose_downstream,
                    trigger=JobConfigTriggerType.release,
                    packages={
                        "package": CommonPackageConfig(
                            # no sense but possible!
                            dist_git_branches={
                                "f41": {"open_pull_request_for": ["f40", "f39"]},
                                "f38": {"open_pull_request_for": ["f37"]},
                            },
                        )
                    },
                ),
            ],
            JobConfigTriggerType.release,
            {"f41", "f40"},
            {"f41"},
            {"f41": {"f40"}},
            {"f40"},
        ),
    ],
)
def test_branches(
    mock_get_f_aliases,
    jobs,
    job_config_trigger_type,
    branches_override,
    branches,
    ff_branches,
    all_ff_branches,
):
    project = flexmock(
        default_branch="main",
    )
    flexmock(ServiceConfig, get_project=lambda url: project)
    propose_downstream_helper = ProposeDownstreamJobHelper(
        service_config=ServiceConfig(),
        package_config=PackageConfig(
            jobs=jobs, packages={"package": CommonPackageConfig()}
        ),
        job_config=jobs[0],
        project=flexmock(),
        metadata=flexmock(pr_id=None),
        db_project_event=flexmock()
        .should_receive("get_project_event_object")
        .and_return(flexmock(job_config_trigger_type=job_config_trigger_type))
        .mock(),
        branches_override=branches_override,
    )
    assert propose_downstream_helper.branches == branches
    for source_branch in branches:
        assert (
            propose_downstream_helper.get_ff_branches_from(source_branch)
            == ff_branches[source_branch]
        )
        assert propose_downstream_helper.ff_branches == all_ff_branches
