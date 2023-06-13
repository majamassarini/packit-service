# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

from http import HTTPStatus
from logging import getLogger

from flask_restx import Namespace, Resource, fields

from packit_service.models import GitProjectModel
from packit_service.service.api.parsers import indices, pagination_arguments
from packit_service.service.api.utils import response_maker
from packit_service.service.urls import get_srpm_build_info_url

logger = getLogger("packit_service")

ns = Namespace(
    "projects", description="Repositories which have Packit Service enabled."
)

project_model = ns.model(
    "Project",
    {
        "namespace": fields.String(required=True, example="systemd"),
        "repo_name": fields.String(required=True, example="systemd"),
        "project_url": fields.String(
            required=True, example="https://github.com/systemd/systemd"
        ),
        "prs_handled": fields.Integer(required=True, example="100"),
        "branches_handled": fields.Integer(required=True, example="100"),
        "releases_handled": fields.Integer(required=True, example="0"),
        "issues_handled": fields.Integer(required=True, example="0"),
    },
)


@ns.route("")
class ProjectsList(Resource):
    @ns.marshal_list_with(project_model)
    @ns.expect(pagination_arguments)
    @ns.response(HTTPStatus.PARTIAL_CONTENT.value, "Projects list follows")
    @ns.response(HTTPStatus.OK.value, "OK")
    def get(self):
        """List all GitProjects"""

        result = []
        first, last = indices()

        for project in GitProjectModel.get_range(first, last):
            project_info = {
                "namespace": project.namespace,
                "repo_name": project.repo_name,
                "project_url": project.project_url,
                "prs_handled": len(project.pull_requests),
                "branches_handled": len(project.branches),
                "releases_handled": len(project.releases),
                "issues_handled": len(project.issues),
            }
            result.append(project_info)

        resp = response_maker(
            result,
            status=HTTPStatus.PARTIAL_CONTENT if result else HTTPStatus.OK,
            headers={"Content-Range": f"git-projects {first + 1}-{last}/*"},
        )
        return resp


@ns.route("/<forge>/<namespace>/<repo_name>")
@ns.param("forge", "Git Forge")
@ns.param("namespace", "Namespace")
@ns.param("repo_name", "Repo Name")
class ProjectInfo(Resource):
    @ns.marshal_with(project_model)
    @ns.response(HTTPStatus.OK.value, "Project details follow")
    def get(self, forge, namespace, repo_name):
        """Project Details"""
        project = GitProjectModel.get_project(forge, namespace, repo_name)
        if not project:
            return response_maker(
                {"error": "No info about project stored in DB"},
                status=HTTPStatus.NOT_FOUND,
            )
        project_info = {
            "namespace": project.namespace,
            "repo_name": project.repo_name,
            "project_url": project.project_url,
            "prs_handled": len(project.pull_requests),
            "branches_handled": len(project.branches),
            "releases_handled": len(project.releases),
            "issues_handled": len(project.issues),
        }
        return response_maker(project_info)


@ns.route("/<forge>")
@ns.param("forge", "Git Forge")
class ProjectsForge(Resource):
    @ns.marshal_list_with(project_model)
    @ns.expect(pagination_arguments)
    @ns.response(HTTPStatus.PARTIAL_CONTENT.value, "Projects list follows")
    @ns.response(HTTPStatus.OK.value, "OK")
    def get(self, forge):
        """List of projects of given forge. (e.g. github.com, gitlab.com)"""

        result = []
        first, last = indices()

        for project in GitProjectModel.get_by_forge(first, last, forge):
            project_info = {
                "namespace": project.namespace,
                "repo_name": project.repo_name,
                "project_url": project.project_url,
                "prs_handled": len(project.pull_requests),
                "branches_handled": len(project.branches),
                "releases_handled": len(project.releases),
                "issues_handled": len(project.issues),
            }
            result.append(project_info)

        resp = response_maker(
            result,
            status=HTTPStatus.PARTIAL_CONTENT if result else HTTPStatus.OK,
            headers={"Content-Range": f"git-projects {first + 1}-{last}/*"},
        )
        return resp


@ns.route("/<forge>/<namespace>")
@ns.param("forge", "Git Forge")
@ns.param("namespace", "Namespace")
class ProjectsNamespace(Resource):
    @ns.marshal_list_with(project_model)
    @ns.response(HTTPStatus.OK.value, "Projects details follow")
    def get(self, forge, namespace):
        """List of projects of given forge and namespace"""
        result = []
        for project in GitProjectModel.get_by_forge_namespace(forge, namespace):
            project_info = {
                "namespace": project.namespace,
                "repo_name": project.repo_name,
                "project_url": project.project_url,
                "prs_handled": len(project.pull_requests),
                "branches_handled": len(project.branches),
                "releases_handled": len(project.releases),
                "issues_handled": len(project.issues),
            }
            result.append(project_info)
        return response_maker(result)


build_info_model = ns.model(
    "BuildInfo",
    {
        "build_id": fields.Integer(example="1672735"),
        "chroot": fields.String(example="fedora-32-x86_64"),
        "status": fields.String(example="success"),
        "web_url": fields.String(
            example="https://copr.fedorainfracloud.org/coprs/build/1672735/"
        ),
    },
)

srpm_build_info_model = ns.model(
    "SRPMBuildInfo",
    {
        "srpm_build_id": fields.Integer(example="10095"),
        "status": fields.String(example="success"),
        "log_url": fields.String(
            example="https://dashboard.localhost/results/srpm-builds/10095"
        ),
    },
)

tests_info_model = ns.model(
    "TestsInfo",
    {
        "pipeline_id": fields.String(example="b995ba28-6659-467e-a9ff-35466fb4f525"),
        "chroot": fields.String(example="fedora-31-x86_64"),
        "status": fields.String(example="error"),
        "web_url": fields.String(
            example=(
                "https://console-testing-farm.apps.ci.centos.org/"
                "pipeline/b995ba28-6659-467e-a9ff-35466fb4f525"
            )
        ),
    },
)

project_pr_model = ns.model(
    "ProjectPullRequest",
    {
        "pr_id": fields.Integer(required=True, example="1872"),
        "builds": fields.Nested(build_info_model, required=True),
        "koji_builds": fields.Nested(
            build_info_model, required=True
        ),  # TODO: no good example, never populated?
        "srpm_builds": fields.Nested(srpm_build_info_model, required=True),
        "tests": fields.Nested(tests_info_model, required=True),
    },
)


@ns.route("/<forge>/<namespace>/<repo_name>/prs")
@ns.param("forge", "Git Forge")
@ns.param("namespace", "Namespace")
@ns.param("repo_name", "Repo Name")
class ProjectsPRs(Resource):
    @ns.marshal_list_with(project_pr_model)
    @ns.expect(pagination_arguments)
    @ns.response(
        HTTPStatus.PARTIAL_CONTENT.value, "Project PRs handled by Packit Service follow"
    )
    @ns.response(HTTPStatus.OK.value, "OK")
    def get(self, forge, namespace, repo_name):
        """List PRs"""

        result = []
        first, last = indices()

        for pr in GitProjectModel.get_project_prs(
            first, last, forge, namespace, repo_name
        ):
            pr_info = {
                "pr_id": pr.pr_id,
                "builds": [],
                "koji_builds": [],
                "srpm_builds": [],
                "tests": [],
            }

            for build in pr.get_copr_builds():
                build_info = {
                    "build_id": build.build_id,
                    "chroot": build.target,
                    "status": build.status,
                    "web_url": build.web_url,
                }
                pr_info["builds"].append(build_info)

            for build in pr.get_koji_builds():
                build_info = {
                    "build_id": build.build_id,
                    "chroot": build.target,
                    "status": build.status,
                    "web_url": build.web_url,
                }
                pr_info["koji_builds"].append(build_info)

            for build in pr.get_srpm_builds():
                build_info = {
                    "srpm_build_id": build.id,
                    "status": build.status,
                    "log_url": get_srpm_build_info_url(build.id),
                }
                pr_info["srpm_builds"].append(build_info)

            for test_run in pr.get_test_runs():
                test_info = {
                    "pipeline_id": test_run.pipeline_id,
                    "chroot": test_run.target,
                    "status": str(test_run.status),
                    "web_url": test_run.web_url,
                }
                pr_info["tests"].append(test_info)

            result.append(pr_info)

        resp = response_maker(
            result,
            status=HTTPStatus.PARTIAL_CONTENT if result else HTTPStatus.OK,
            headers={"Content-Range": f"git-project-prs {first + 1}-{last}/*"},
        )

        return resp


@ns.route("/<forge>/<namespace>/<repo_name>/issues")
@ns.param("forge", "Git Forge")
@ns.param("namespace", "Namespace")
@ns.param("repo_name", "Repo Name")
class ProjectIssues(Resource):
    # TODO: docs OK but is not marshalling correctly
    # @ns.marshal_with(fields.List(fields.Integer(example="432344")))
    @ns.response(
        HTTPStatus.OK.value, "OK, project issues handled by Packit Service follow"
    )
    def get(self, forge, namespace, repo_name):
        """Project issues"""
        return response_maker(
            [
                issue.issue_id
                for issue in GitProjectModel.get_project_issues(
                    forge, namespace, repo_name
                )
            ]
        )


project_release_model = ns.model(
    "ProjectRelease",
    {
        "tag_name": fields.String(required=True, example="0.15.0"),
        "commit_hash": fields.String(
            required=True, example="b86243ea30c7809f507abe2e59359cf9cadf11a5"
        ),
    },
)


@ns.route("/<forge>/<namespace>/<repo_name>/releases")
@ns.param("forge", "Git Forge")
@ns.param("namespace", "Namespace")
@ns.param("repo_name", "Repo Name")
class ProjectReleases(Resource):
    @ns.marshal_list_with(project_release_model)
    @ns.response(
        HTTPStatus.OK.value, "OK, project releases handled by Packit Service follow"
    )
    def get(self, forge, namespace, repo_name):
        """Project releases"""
        result = []
        for release in GitProjectModel.get_project_releases(
            forge, namespace, repo_name
        ):
            release_info = {
                "tag_name": release.tag_name,
                "commit_hash": release.commit_hash,
            }
            result.append(release_info)
        return response_maker(result)


project_branch_model = ns.model(
    "ProjectBranch",
    {
        "branch": fields.String(required=True, example="main"),
        "builds": fields.Nested(build_info_model, required=True),
        "koji_builds": fields.Nested(
            build_info_model, required=True
        ),  # TODO: no good example, never populated?
        "srpm_builds": fields.Nested(srpm_build_info_model, required=True),
        "tests": fields.Nested(tests_info_model, required=True),
    },
)


@ns.route("/<forge>/<namespace>/<repo_name>/branches")
@ns.param("forge", "Git Forge")
@ns.param("namespace", "Namespace")
@ns.param("repo_name", "Repo Name")
class ProjectBranches(Resource):
    @ns.marshal_list_with(project_branch_model)
    @ns.response(
        HTTPStatus.OK.value, "OK, project branches handled by Packit Service follow"
    )
    def get(self, forge, namespace, repo_name):
        """Project branches"""
        result = []
        for branch in GitProjectModel.get_project_branches(forge, namespace, repo_name):
            branch_info = {
                "branch": branch.name,
                "builds": [],
                "koji_builds": [],
                "srpm_builds": [],
                "tests": [],
            }

            for build in branch.get_copr_builds():
                build_info = {
                    "build_id": build.build_id,
                    "chroot": build.target,
                    "status": build.status,
                    "web_url": build.web_url,
                }
                branch_info["builds"].append(build_info)

            for build in branch.get_koji_builds():
                build_info = {
                    "build_id": build.build_id,
                    "chroot": build.target,
                    "status": build.status,
                    "web_url": build.web_url,
                }
                branch_info["koji_builds"].append(build_info)

            for build in branch.get_srpm_builds():
                build_info = {
                    "srpm_build_id": build.id,
                    "status": build.status,
                    "log_url": get_srpm_build_info_url(build.id),
                }
                branch_info["srpm_builds"].append(build_info)

            for test_run in branch.get_test_runs():
                test_info = {
                    "pipeline_id": test_run.pipeline_id,
                    "chroot": test_run.target,
                    "status": test_run.status,
                    "web_url": test_run.web_url,
                }
                branch_info["tests"].append(test_info)
            result.append(branch_info)

        return response_maker(result)
