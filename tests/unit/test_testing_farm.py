# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

import pytest
from flexmock import flexmock
from ogr.abstract import CommitStatus
from packit.config import JobConfig, JobType, JobConfigTriggerType
from packit.local_project import LocalProject

from packit_service.config import PackageConfigGetter
from packit_service.models import TFTTestRunModel

# These names are definitely not nice, still they help with making classes
# whose names start with Testing* or Test* to become invisible for pytest,
# and so stop the test discovery warnings.
from packit_service.service.events import (
    TestingFarmResultsEvent as TFResultsEvent,
    TestingFarmResult as TFResult,
    TestResult as TResult,
    EventData,
)
from packit_service.worker.handlers import TestingFarmResultsHandler as TFResultsHandler
from packit_service.worker.reporting import StatusReporter
from packit_service.worker.testing_farm import (
    TestingFarmJobHelper as TFJobHelper,
)


@pytest.mark.parametrize(
    "tests_result,tests_message,tests_tests,status_status,status_message,status_url",
    [
        pytest.param(
            TFResult.passed,
            "some message",
            [
                TResult(
                    name="/something/different",
                    result=TFResult.passed,
                    log_url="some specific url",
                )
            ],
            CommitStatus.success,
            "some message",
            "some url",
            id="only_installation_not_provided_passed",
        ),
        pytest.param(
            TFResult.failed,
            "some message",
            [
                TResult(
                    name="/something/different",
                    result=TFResult.failed,
                    log_url="some specific url",
                )
            ],
            CommitStatus.failure,
            "some message",
            "some url",
            id="only_installation_not_provided_failed",
        ),
        pytest.param(
            TFResult.passed,
            "some message",
            [
                TResult(
                    name="/install/copr-build",
                    result=TFResult.passed,
                    log_url="some specific url",
                ),
                TResult(
                    name="/different/test",
                    result=TFResult.passed,
                    log_url="some specific url",
                ),
            ],
            CommitStatus.success,
            "some message",
            "some url",
            id="only_installation_multiple_results_passed",
        ),
        pytest.param(
            TFResult.failed,
            "some message",
            [
                TResult(
                    name="/install/copr-build",
                    result=TFResult.failed,
                    log_url="some specific url",
                ),
                TResult(
                    name="/different/test",
                    result=TFResult.passed,
                    log_url="some specific url",
                ),
            ],
            CommitStatus.failure,
            "some message",
            "some url",
            id="only_installation_multiple_results_failed",
        ),
        pytest.param(
            TFResult.failed,
            "some message",
            [
                TResult(
                    name="/install/copr-build",
                    result=TFResult.passed,
                    log_url="some specific url",
                ),
                TResult(
                    name="/different/test",
                    result=TFResult.failed,
                    log_url="some specific url",
                ),
            ],
            CommitStatus.failure,
            "some message",
            "some url",
            id="only_installation_multiple_results_failed_different",
        ),
    ],
)
def test_testing_farm_response(
    tests_result,
    tests_message,
    tests_tests,
    status_status,
    status_message,
    status_url,
):
    flexmock(PackageConfigGetter).should_receive(
        "get_package_config_from_repo"
    ).and_return(
        flexmock(
            jobs=[
                JobConfig(
                    type=JobType.copr_build,
                    trigger=JobConfigTriggerType.pull_request,
                )
            ],
        )
    )
    config = flexmock(command_handler_work_dir=flexmock())
    flexmock(TFResultsHandler).should_receive("service_config").and_return(config)
    flexmock(TFResultsEvent).should_receive("db_trigger").and_return(None)
    config.should_receive("get_project").with_args(
        url="https://github.com/packit/ogr"
    ).and_return()
    event_dict = TFResultsEvent(
        pipeline_id="id",
        result=tests_result,
        compose=flexmock(),
        summary=tests_message,
        log_url="some url",
        copr_build_id=flexmock(),
        copr_chroot="fedora-rawhide-x86_64",
        tests=tests_tests,
        commit_sha=flexmock(),
        project_url="https://github.com/packit/ogr",
    ).get_dict()
    test_farm_handler = TFResultsHandler(
        package_config=flexmock(),
        job_config=flexmock(),
        data=EventData.from_event_dict(event_dict),
        tests=tests_tests,
        result=tests_result,
        pipeline_id="id",
        log_url="some url",
        copr_chroot="fedora-rawhide-x86_64",
        summary=tests_message,
    )
    flexmock(StatusReporter).should_receive("report").with_args(
        state=status_status,
        description=status_message,
        url=status_url,
        check_names="packit-stg/testing-farm-fedora-rawhide-x86_64",
    )

    tft_test_run_model = flexmock()
    tft_test_run_model.should_receive("set_status").with_args(
        tests_result
    ).and_return().once()
    tft_test_run_model.should_receive("set_web_url").with_args(
        "some url"
    ).and_return().once()

    flexmock(TFTTestRunModel).should_receive("get_by_pipeline_id").and_return(
        tft_test_run_model
    )

    flexmock(LocalProject).should_receive("refresh_the_arguments").and_return(None)

    test_farm_handler.run()


@pytest.mark.parametrize(
    "chroot,compose,arch",
    [
        ("fedora-33-x86_64", "Fedora-33", "x86_64"),
        ("centos-stream-x86_64", "Centos-Stream", "x86_64"),
    ],
)
def test_get_compose_arch(chroot, compose, arch):
    job_helper = TFJobHelper(
        service_config=flexmock(
            testing_farm_api_url="xyz",
        ),
        package_config=flexmock(jobs=[]),
        project=flexmock(),
        metadata=flexmock(),
        db_trigger=flexmock(),
        job_config=JobConfig(
            type=JobType.tests, trigger=JobConfigTriggerType.pull_request
        ),
    )
    job_helper = flexmock(job_helper)

    response = flexmock(
        status_code=200, json=lambda: {"composes": [{"name": "Fedora-33"}]}
    )
    job_helper.should_receive("send_testing_farm_request").and_return(response)

    compose_, arch_ = job_helper.get_compose_arch(chroot)
    assert compose_ == compose
    assert arch_ == arch


@pytest.mark.parametrize(
    (
        "tf_api,"
        "tf_token,"
        "ps_deployment,"
        "repo,"
        "namespace,"
        "commit_sha,"
        "project_url,"
        "git_ref,"
        "copr_owner,"
        "copr_project,"
        "build_id,"
        "chroot,"
        "compose,"
        "arch"
    ),
    [
        (
            "https://api.dev.testing-farm.io/v0.1/",
            "very-secret",
            "test",
            "packit",
            "packit-service",
            "feb41e5",
            "https://github.com/packit/packit",
            "master",
            "me",
            "cool-project",
            "123456",
            "centos-stream-x86_64",
            "Fedora-Rawhide",
            "x86_64",
        ),
    ],
)
def test_payload(
    tf_api,
    tf_token,
    ps_deployment,
    repo,
    namespace,
    commit_sha,
    project_url,
    git_ref,
    copr_owner,
    copr_project,
    build_id,
    chroot,
    compose,
    arch,
):
    # Soo many things are happening in a single constructor!!!!
    config = flexmock(
        testing_farm_api_url=tf_api,
        testing_farm_secret=tf_token,
        deployment=ps_deployment,
        command_handler_work_dir="/tmp",
    )
    package_config = flexmock(jobs=[])
    project = flexmock(
        repo=repo,
        namespace=namespace,
        service="GitHub",
        get_git_urls=lambda: {"git": f"{project_url}.git"},
    )
    metadata = flexmock(
        trigger=flexmock(),
        commit_sha=commit_sha,
        git_ref=git_ref,
        project_url=project_url,
    )
    db_trigger = flexmock()

    job_helper = TFJobHelper(
        service_config=config,
        package_config=package_config,
        project=project,
        metadata=metadata,
        db_trigger=db_trigger,
        job_config=JobConfig(
            type=JobType.tests, trigger=JobConfigTriggerType.pull_request
        ),
    )
    job_helper = flexmock(job_helper)

    job_helper.should_receive("job_owner").and_return(copr_owner)
    job_helper.should_receive("job_project").and_return(copr_project)
    job_helper.should_receive("get_compose_arch").and_return(compose, arch)
    payload = job_helper._payload(build_id, chroot)

    assert payload["api_key"] == tf_token
    assert payload["test"]["fmf"] == {
        "url": project_url,
        "ref": commit_sha,
    }
    assert payload["environments"] == [
        {
            "arch": arch,
            "os": {"compose": compose},
            "artifacts": [{"id": f"{build_id}:{chroot}", "type": "fedora-copr-build"}],
        }
    ]
    assert payload["notification"]["webhook"]["url"].endswith("/testing-farm/results")


def test_get_request_details():
    request_id = "123abc"
    request = {
        "id": request_id,
        "environments_requested": [
            {"arch": "x86_64", "os": {"compose": "Fedora-Rawhide"}}
        ],
        "result": {"overall": "passed", "summary": "all ok"},
    }
    request_response = flexmock(status_code=200)
    request_response.should_receive("json").and_return(request)
    flexmock(
        TFJobHelper,
        send_testing_farm_request=request_response,
        job_build=None,
    )
    details = TFJobHelper.get_request_details(request_id)
    assert details == request
