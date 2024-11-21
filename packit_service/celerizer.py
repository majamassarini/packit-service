# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

from os import getenv

from celery import Celery
from lazy_object_proxy import Proxy

from packit_service.sentry_integration import configure_sentry

# flake8: noqa


class Celerizer:
    def __init__(self):
        self._celery_app = None

    @property
    def celery_app(self):
        if self._celery_app is None:
            host = getenv("REDIS_SERVICE_HOST", "redis")
            password = getenv("REDIS_PASSWORD", "")
            port = getenv("REDIS_SERVICE_PORT", "6379")
            db = getenv("REDIS_SERVICE_DB", "0")
            celery_beckend = getenv("REDIS_CELERY_BECKEND", "1")
            broker_url = f"redis://:{password}@{host}:{port}/{db}"
            backend_url = f"redis://:{password}@{host}:{port}/{celery_beckend}"

            # http://docs.celeryq.dev/en/stable/reference/celery.html#celery.Celery
            self._celery_app = Celery(backend=backend_url, broker=broker_url)

            # https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#configuration
            self._celery_app.config_from_object("packit_service.celery_config")

        return self._celery_app


def get_celery_application():
    celerizer = Celerizer()
    app = celerizer.celery_app
    configure_sentry(
        runner_type="packit-worker",
        celery_integration=True,
        sqlalchemy_integration=True,
    )
    return app


# Let a remote debugger (Visual Studio Code client)
# access this running instance.
import debugpy

# Allow other computers to attach to debugpy at this IP address and port.
try:
    debugpy.listen(("0.0.0.0", 5678))

    # Uncomment the following lines if you want to
    # pause the program until a remote debugger is attached

    # print("Waiting for debugger attach")
    debugpy.wait_for_client()

except RuntimeError:
    pass


# @todo: rerun docker-compose build --force-rm for every change!

import json

# this event creates more builds than needed:
# - rpm-build:fedora-41-x86_64:latest
# - rpm-build:fedora-41-x86_64:rawhide
# - rpm-build:fedora-rawhide-x86_64:latest
# - rpm-build:fedora-rawhide-x86_64:rawhide
#
# hello-world packit.yaml:
# - job: copr_build
#   trigger: pull_request
#   identifier: latest
#   targets:
#   - fedora-latest-x86_64
#
# - job: copr_build
#   trigger: pull_request
#   identifier: rawhide
#   targets:
#   - fedora-rawhide-x86_64
#
# I would have expected only two builds to be created:
# - rpm-build:fedora-41-x86_64:latest
# - rpm-build:fedora-rawhide-x86_64:rawhide

pull_request_synchronize = """
{
  "action": "synchronize",
  "number": 2119,
  "pull_request": {
    "url": "https://api.github.com/repos/packit/hello-world/pulls/2119",
    "id": 1768063546,
    "node_id": "PR_kwDOCwFO9M5pYoI6",
    "html_url": "https://github.com/packit/hello-world/pull/2119",
    "diff_url": "https://github.com/packit/hello-world/pull/2119.diff",
    "patch_url": "https://github.com/packit/hello-world/pull/2119.patch",
    "issue_url": "https://api.github.com/repos/packit/hello-world/issues/2119",
    "number": 2119,
    "state": "open",
    "locked": false,
    "title": "Create a setup with two different tests",
    "user": {
      "login": "majamassarini",
      "id": 2678400,
      "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
      "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/majamassarini",
      "html_url": "https://github.com/majamassarini",
      "followers_url": "https://api.github.com/users/majamassarini/followers",
      "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
      "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
      "organizations_url": "https://api.github.com/users/majamassarini/orgs",
      "repos_url": "https://api.github.com/users/majamassarini/repos",
      "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
      "received_events_url": "https://api.github.com/users/majamassarini/received_events",
      "type": "User",
      "user_view_type": "public",
      "site_admin": false
    },
    "body": null,
    "created_at": "2024-03-12T14:24:41Z",
    "updated_at": "2024-11-21T08:15:45Z",
    "closed_at": null,
    "merged_at": null,
    "merge_commit_sha": "f95b9a71ab9ca9a7d93c224a8fd6e28922d0dae0",
    "assignee": null,
    "assignees": [

    ],
    "requested_reviewers": [

    ],
    "requested_teams": [

    ],
    "labels": [

    ],
    "milestone": null,
    "draft": false,
    "commits_url": "https://api.github.com/repos/packit/hello-world/pulls/2119/commits",
    "review_comments_url": "https://api.github.com/repos/packit/hello-world/pulls/2119/comments",
    "review_comment_url": "https://api.github.com/repos/packit/hello-world/pulls/comments{/number}",
    "comments_url": "https://api.github.com/repos/packit/hello-world/issues/2119/comments",
    "statuses_url": "https://api.github.com/repos/packit/hello-world/statuses/9dfd54b0737dc3002bab09919342218c81d424bc",
    "head": {
      "label": "majamassarini:tests_manual_trigger_ui",
      "ref": "tests_manual_trigger_ui",
      "sha": "9dfd54b0737dc3002bab09919342218c81d424bc",
      "user": {
        "login": "majamassarini",
        "id": 2678400,
        "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
        "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/majamassarini",
        "html_url": "https://github.com/majamassarini",
        "followers_url": "https://api.github.com/users/majamassarini/followers",
        "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
        "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
        "organizations_url": "https://api.github.com/users/majamassarini/orgs",
        "repos_url": "https://api.github.com/users/majamassarini/repos",
        "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
        "received_events_url": "https://api.github.com/users/majamassarini/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "repo": {
        "id": 490264183,
        "node_id": "R_kgDOHTjWdw",
        "name": "hello-world",
        "full_name": "majamassarini/hello-world",
        "private": false,
        "owner": {
          "login": "majamassarini",
          "id": 2678400,
          "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
          "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/majamassarini",
          "html_url": "https://github.com/majamassarini",
          "followers_url": "https://api.github.com/users/majamassarini/followers",
          "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
          "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
          "organizations_url": "https://api.github.com/users/majamassarini/orgs",
          "repos_url": "https://api.github.com/users/majamassarini/repos",
          "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
          "received_events_url": "https://api.github.com/users/majamassarini/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/majamassarini/hello-world",
        "description": "The most progresive command-line tool in the world.",
        "fork": true,
        "url": "https://api.github.com/repos/majamassarini/hello-world",
        "forks_url": "https://api.github.com/repos/majamassarini/hello-world/forks",
        "keys_url": "https://api.github.com/repos/majamassarini/hello-world/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/majamassarini/hello-world/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/majamassarini/hello-world/teams",
        "hooks_url": "https://api.github.com/repos/majamassarini/hello-world/hooks",
        "issue_events_url": "https://api.github.com/repos/majamassarini/hello-world/issues/events{/number}",
        "events_url": "https://api.github.com/repos/majamassarini/hello-world/events",
        "assignees_url": "https://api.github.com/repos/majamassarini/hello-world/assignees{/user}",
        "branches_url": "https://api.github.com/repos/majamassarini/hello-world/branches{/branch}",
        "tags_url": "https://api.github.com/repos/majamassarini/hello-world/tags",
        "blobs_url": "https://api.github.com/repos/majamassarini/hello-world/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/majamassarini/hello-world/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/majamassarini/hello-world/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/majamassarini/hello-world/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/majamassarini/hello-world/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/majamassarini/hello-world/languages",
        "stargazers_url": "https://api.github.com/repos/majamassarini/hello-world/stargazers",
        "contributors_url": "https://api.github.com/repos/majamassarini/hello-world/contributors",
        "subscribers_url": "https://api.github.com/repos/majamassarini/hello-world/subscribers",
        "subscription_url": "https://api.github.com/repos/majamassarini/hello-world/subscription",
        "commits_url": "https://api.github.com/repos/majamassarini/hello-world/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/majamassarini/hello-world/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/majamassarini/hello-world/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/majamassarini/hello-world/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/majamassarini/hello-world/contents/{+path}",
        "compare_url": "https://api.github.com/repos/majamassarini/hello-world/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/majamassarini/hello-world/merges",
        "archive_url": "https://api.github.com/repos/majamassarini/hello-world/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/majamassarini/hello-world/downloads",
        "issues_url": "https://api.github.com/repos/majamassarini/hello-world/issues{/number}",
        "pulls_url": "https://api.github.com/repos/majamassarini/hello-world/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/majamassarini/hello-world/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/majamassarini/hello-world/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/majamassarini/hello-world/labels{/name}",
        "releases_url": "https://api.github.com/repos/majamassarini/hello-world/releases{/id}",
        "deployments_url": "https://api.github.com/repos/majamassarini/hello-world/deployments",
        "created_at": "2022-05-09T12:00:35Z",
        "updated_at": "2023-08-01T12:58:52Z",
        "pushed_at": "2024-11-21T08:15:44Z",
        "git_url": "git://github.com/majamassarini/hello-world.git",
        "ssh_url": "git@github.com:majamassarini/hello-world.git",
        "clone_url": "https://github.com/majamassarini/hello-world.git",
        "svn_url": "https://github.com/majamassarini/hello-world",
        "homepage": null,
        "size": 68,
        "stargazers_count": 0,
        "watchers_count": 0,
        "language": "Python",
        "has_issues": false,
        "has_projects": true,
        "has_downloads": true,
        "has_wiki": true,
        "has_pages": false,
        "has_discussions": false,
        "forks_count": 0,
        "mirror_url": null,
        "archived": false,
        "disabled": false,
        "open_issues_count": 0,
        "license": {
          "key": "mit",
          "name": "MIT License",
          "spdx_id": "MIT",
          "url": "https://api.github.com/licenses/mit",
          "node_id": "MDc6TGljZW5zZTEz"
        },
        "allow_forking": true,
        "is_template": false,
        "web_commit_signoff_required": false,
        "topics": [

        ],
        "visibility": "public",
        "forks": 0,
        "open_issues": 0,
        "watchers": 0,
        "default_branch": "main",
        "allow_squash_merge": true,
        "allow_merge_commit": true,
        "allow_rebase_merge": true,
        "allow_auto_merge": false,
        "delete_branch_on_merge": false,
        "allow_update_branch": false,
        "use_squash_pr_title_as_default": false,
        "squash_merge_commit_message": "COMMIT_MESSAGES",
        "squash_merge_commit_title": "COMMIT_OR_PR_TITLE",
        "merge_commit_message": "PR_TITLE",
        "merge_commit_title": "MERGE_MESSAGE"
      }
    },
    "base": {
      "label": "packit:main",
      "ref": "main",
      "sha": "f2c98da9efc0190628db81cd220fe8cc2a8e9e95",
      "user": {
        "login": "packit",
        "id": 46870917,
        "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2ODcwOTE3",
        "avatar_url": "https://avatars.githubusercontent.com/u/46870917?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/packit",
        "html_url": "https://github.com/packit",
        "followers_url": "https://api.github.com/users/packit/followers",
        "following_url": "https://api.github.com/users/packit/following{/other_user}",
        "gists_url": "https://api.github.com/users/packit/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/packit/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/packit/subscriptions",
        "organizations_url": "https://api.github.com/users/packit/orgs",
        "repos_url": "https://api.github.com/users/packit/repos",
        "events_url": "https://api.github.com/users/packit/events{/privacy}",
        "received_events_url": "https://api.github.com/users/packit/received_events",
        "type": "Organization",
        "user_view_type": "public",
        "site_admin": false
      },
      "repo": {
        "id": 184635124,
        "node_id": "MDEwOlJlcG9zaXRvcnkxODQ2MzUxMjQ=",
        "name": "hello-world",
        "full_name": "packit/hello-world",
        "private": false,
        "owner": {
          "login": "packit",
          "id": 46870917,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2ODcwOTE3",
          "avatar_url": "https://avatars.githubusercontent.com/u/46870917?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/packit",
          "html_url": "https://github.com/packit",
          "followers_url": "https://api.github.com/users/packit/followers",
          "following_url": "https://api.github.com/users/packit/following{/other_user}",
          "gists_url": "https://api.github.com/users/packit/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/packit/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/packit/subscriptions",
          "organizations_url": "https://api.github.com/users/packit/orgs",
          "repos_url": "https://api.github.com/users/packit/repos",
          "events_url": "https://api.github.com/users/packit/events{/privacy}",
          "received_events_url": "https://api.github.com/users/packit/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/packit/hello-world",
        "description": "The most progresive command-line tool in the world.",
        "fork": false,
        "url": "https://api.github.com/repos/packit/hello-world",
        "forks_url": "https://api.github.com/repos/packit/hello-world/forks",
        "keys_url": "https://api.github.com/repos/packit/hello-world/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/packit/hello-world/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/packit/hello-world/teams",
        "hooks_url": "https://api.github.com/repos/packit/hello-world/hooks",
        "issue_events_url": "https://api.github.com/repos/packit/hello-world/issues/events{/number}",
        "events_url": "https://api.github.com/repos/packit/hello-world/events",
        "assignees_url": "https://api.github.com/repos/packit/hello-world/assignees{/user}",
        "branches_url": "https://api.github.com/repos/packit/hello-world/branches{/branch}",
        "tags_url": "https://api.github.com/repos/packit/hello-world/tags",
        "blobs_url": "https://api.github.com/repos/packit/hello-world/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/packit/hello-world/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/packit/hello-world/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/packit/hello-world/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/packit/hello-world/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/packit/hello-world/languages",
        "stargazers_url": "https://api.github.com/repos/packit/hello-world/stargazers",
        "contributors_url": "https://api.github.com/repos/packit/hello-world/contributors",
        "subscribers_url": "https://api.github.com/repos/packit/hello-world/subscribers",
        "subscription_url": "https://api.github.com/repos/packit/hello-world/subscription",
        "commits_url": "https://api.github.com/repos/packit/hello-world/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/packit/hello-world/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/packit/hello-world/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/packit/hello-world/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/packit/hello-world/contents/{+path}",
        "compare_url": "https://api.github.com/repos/packit/hello-world/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/packit/hello-world/merges",
        "archive_url": "https://api.github.com/repos/packit/hello-world/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/packit/hello-world/downloads",
        "issues_url": "https://api.github.com/repos/packit/hello-world/issues{/number}",
        "pulls_url": "https://api.github.com/repos/packit/hello-world/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/packit/hello-world/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/packit/hello-world/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/packit/hello-world/labels{/name}",
        "releases_url": "https://api.github.com/repos/packit/hello-world/releases{/id}",
        "deployments_url": "https://api.github.com/repos/packit/hello-world/deployments",
        "created_at": "2019-05-02T18:54:46Z",
        "updated_at": "2023-01-31T17:16:23Z",
        "pushed_at": "2024-11-21T04:50:20Z",
        "git_url": "git://github.com/packit/hello-world.git",
        "ssh_url": "git@github.com:packit/hello-world.git",
        "clone_url": "https://github.com/packit/hello-world.git",
        "svn_url": "https://github.com/packit/hello-world",
        "homepage": null,
        "size": 186,
        "stargazers_count": 4,
        "watchers_count": 4,
        "language": "Python",
        "has_issues": true,
        "has_projects": true,
        "has_downloads": true,
        "has_wiki": true,
        "has_pages": false,
        "has_discussions": false,
        "forks_count": 23,
        "mirror_url": null,
        "archived": false,
        "disabled": false,
        "open_issues_count": 98,
        "license": {
          "key": "mit",
          "name": "MIT License",
          "spdx_id": "MIT",
          "url": "https://api.github.com/licenses/mit",
          "node_id": "MDc6TGljZW5zZTEz"
        },
        "allow_forking": true,
        "is_template": false,
        "web_commit_signoff_required": false,
        "topics": [

        ],
        "visibility": "public",
        "forks": 23,
        "open_issues": 98,
        "watchers": 4,
        "default_branch": "main",
        "allow_squash_merge": true,
        "allow_merge_commit": true,
        "allow_rebase_merge": true,
        "allow_auto_merge": false,
        "delete_branch_on_merge": false,
        "allow_update_branch": false,
        "use_squash_pr_title_as_default": false,
        "squash_merge_commit_message": "COMMIT_MESSAGES",
        "squash_merge_commit_title": "COMMIT_OR_PR_TITLE",
        "merge_commit_message": "PR_BODY",
        "merge_commit_title": "PR_TITLE"
      }
    },
    "_links": {
      "self": {
        "href": "https://api.github.com/repos/packit/hello-world/pulls/2119"
      },
      "html": {
        "href": "https://github.com/packit/hello-world/pull/2119"
      },
      "issue": {
        "href": "https://api.github.com/repos/packit/hello-world/issues/2119"
      },
      "comments": {
        "href": "https://api.github.com/repos/packit/hello-world/issues/2119/comments"
      },
      "review_comments": {
        "href": "https://api.github.com/repos/packit/hello-world/pulls/2119/comments"
      },
      "review_comment": {
        "href": "https://api.github.com/repos/packit/hello-world/pulls/comments{/number}"
      },
      "commits": {
        "href": "https://api.github.com/repos/packit/hello-world/pulls/2119/commits"
      },
      "statuses": {
        "href": "https://api.github.com/repos/packit/hello-world/statuses/9dfd54b0737dc3002bab09919342218c81d424bc"
      }
    },
    "author_association": "MEMBER",
    "auto_merge": null,
    "active_lock_reason": null,
    "merged": false,
    "mergeable": null,
    "rebaseable": null,
    "mergeable_state": "unknown",
    "merged_by": null,
    "comments": 15,
    "review_comments": 0,
    "maintainer_can_modify": true,
    "commits": 1,
    "additions": 55,
    "deletions": 20,
    "changed_files": 2
  },
  "before": "ab87b9870d665472d3cfaaf78e62cdda381c83bf",
  "after": "9dfd54b0737dc3002bab09919342218c81d424bc",
  "repository": {
    "id": 184635124,
    "node_id": "MDEwOlJlcG9zaXRvcnkxODQ2MzUxMjQ=",
    "name": "hello-world",
    "full_name": "packit/hello-world",
    "private": false,
    "owner": {
      "login": "packit",
      "id": 46870917,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2ODcwOTE3",
      "avatar_url": "https://avatars.githubusercontent.com/u/46870917?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/packit",
      "html_url": "https://github.com/packit",
      "followers_url": "https://api.github.com/users/packit/followers",
      "following_url": "https://api.github.com/users/packit/following{/other_user}",
      "gists_url": "https://api.github.com/users/packit/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/packit/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/packit/subscriptions",
      "organizations_url": "https://api.github.com/users/packit/orgs",
      "repos_url": "https://api.github.com/users/packit/repos",
      "events_url": "https://api.github.com/users/packit/events{/privacy}",
      "received_events_url": "https://api.github.com/users/packit/received_events",
      "type": "Organization",
      "user_view_type": "public",
      "site_admin": false
    },
    "html_url": "https://github.com/packit/hello-world",
    "description": "The most progresive command-line tool in the world.",
    "fork": false,
    "url": "https://api.github.com/repos/packit/hello-world",
    "forks_url": "https://api.github.com/repos/packit/hello-world/forks",
    "keys_url": "https://api.github.com/repos/packit/hello-world/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/packit/hello-world/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/packit/hello-world/teams",
    "hooks_url": "https://api.github.com/repos/packit/hello-world/hooks",
    "issue_events_url": "https://api.github.com/repos/packit/hello-world/issues/events{/number}",
    "events_url": "https://api.github.com/repos/packit/hello-world/events",
    "assignees_url": "https://api.github.com/repos/packit/hello-world/assignees{/user}",
    "branches_url": "https://api.github.com/repos/packit/hello-world/branches{/branch}",
    "tags_url": "https://api.github.com/repos/packit/hello-world/tags",
    "blobs_url": "https://api.github.com/repos/packit/hello-world/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/packit/hello-world/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/packit/hello-world/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/packit/hello-world/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/packit/hello-world/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/packit/hello-world/languages",
    "stargazers_url": "https://api.github.com/repos/packit/hello-world/stargazers",
    "contributors_url": "https://api.github.com/repos/packit/hello-world/contributors",
    "subscribers_url": "https://api.github.com/repos/packit/hello-world/subscribers",
    "subscription_url": "https://api.github.com/repos/packit/hello-world/subscription",
    "commits_url": "https://api.github.com/repos/packit/hello-world/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/packit/hello-world/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/packit/hello-world/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/packit/hello-world/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/packit/hello-world/contents/{+path}",
    "compare_url": "https://api.github.com/repos/packit/hello-world/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/packit/hello-world/merges",
    "archive_url": "https://api.github.com/repos/packit/hello-world/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/packit/hello-world/downloads",
    "issues_url": "https://api.github.com/repos/packit/hello-world/issues{/number}",
    "pulls_url": "https://api.github.com/repos/packit/hello-world/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/packit/hello-world/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/packit/hello-world/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/packit/hello-world/labels{/name}",
    "releases_url": "https://api.github.com/repos/packit/hello-world/releases{/id}",
    "deployments_url": "https://api.github.com/repos/packit/hello-world/deployments",
    "created_at": "2019-05-02T18:54:46Z",
    "updated_at": "2023-01-31T17:16:23Z",
    "pushed_at": "2024-11-21T04:50:20Z",
    "git_url": "git://github.com/packit/hello-world.git",
    "ssh_url": "git@github.com:packit/hello-world.git",
    "clone_url": "https://github.com/packit/hello-world.git",
    "svn_url": "https://github.com/packit/hello-world",
    "homepage": null,
    "size": 186,
    "stargazers_count": 4,
    "watchers_count": 4,
    "language": "Python",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "has_discussions": false,
    "forks_count": 23,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 98,
    "license": {
      "key": "mit",
      "name": "MIT License",
      "spdx_id": "MIT",
      "url": "https://api.github.com/licenses/mit",
      "node_id": "MDc6TGljZW5zZTEz"
    },
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "public",
    "forks": 23,
    "open_issues": 98,
    "watchers": 4,
    "default_branch": "main",
    "custom_properties": {

    }
  },
  "organization": {
    "login": "packit",
    "id": 46870917,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2ODcwOTE3",
    "url": "https://api.github.com/orgs/packit",
    "repos_url": "https://api.github.com/orgs/packit/repos",
    "events_url": "https://api.github.com/orgs/packit/events",
    "hooks_url": "https://api.github.com/orgs/packit/hooks",
    "issues_url": "https://api.github.com/orgs/packit/issues",
    "members_url": "https://api.github.com/orgs/packit/members{/member}",
    "public_members_url": "https://api.github.com/orgs/packit/public_members{/member}",
    "avatar_url": "https://avatars.githubusercontent.com/u/46870917?v=4",
    "description": "Packit service: package it in an automated way."
  },
  "sender": {
    "login": "majamassarini",
    "id": 2678400,
    "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
    "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/majamassarini",
    "html_url": "https://github.com/majamassarini",
    "followers_url": "https://api.github.com/users/majamassarini/followers",
    "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
    "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
    "organizations_url": "https://api.github.com/users/majamassarini/orgs",
    "repos_url": "https://api.github.com/users/majamassarini/repos",
    "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
    "received_events_url": "https://api.github.com/users/majamassarini/received_events",
    "type": "User",
    "user_view_type": "public",
    "site_admin": false
  },
  "installation": {
    "id": 1924121,
    "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uMTkyNDEyMQ=="
  }
}
"""

copr_build_end_chroot_rawhide_copr_rawhide_ok = """
{
  "user": "packit-stg",
  "copr": "packit-hello-world-2119-rawhide",
  "owner": "packit-stg",
  "pkg": "hello",
  "build": 8290500,
  "chroot": "fedora-rawhide-x86_64",
  "version": "0.74-1.20241121081727566742.pr2119.15.g9dfd54b",
  "status": 1,
  "ip": "2620:52:3:1:dead:beef:cafe:c1d8",
  "who": "backend.worker-rpm_build_worker:8290500-fedora-rawhide-x86_64",
  "pid": 1090734,
  "what": "build end: user:packit-stg copr:packit-hello-world-2119-rawhide build:8290500 pkg:hello version:0.74-1.20241121081727566742.pr2119.15.g9dfd54b ip:2620:52:3:1:dead:beef:cafe:c1d8 pid:1090734 status:1"
  "topic": "org.fedoraproject.prod.copr.build.end"
}
"""

copr_build_end_chroot_fedora_41_copr_rawhide_ko = """
{
  "user": "packit-stg",
  "copr": "packit-hello-world-2119-rawhide",
  "owner": "packit-stg",
  "pkg": "hello",
  "build": 8290500,
  "chroot": "fedora-41-x86_64",
  "version": "0.74-1.20241121081727566742.pr2119.15.g9dfd54b",
  "status": 0,
  "ip": "2620:52:3:1:dead:beef:cafe:c15a",
  "who": "backend.worker-rpm_build_worker:8290500-fedora-41-x86_64",
  "pid": 1090824,
  "what": "build end: user:packit-stg copr:packit-hello-world-2119-rawhide build:8290500 pkg:hello version:0.74-1.20241121081727566742.pr2119.15.g9dfd54b ip:2620:52:3:1:dead:beef:cafe:c15a pid:1090824 status:0"
  "topic": "org.fedoraproject.prod.copr.build.end"
}
"""

copr_build_end_chroot_fedora_41_copr_latest_ko = """
{
  "user": "packit-stg",
  "copr": "packit-hello-world-2119-latest",
  "owner": "packit-stg",
  "pkg": "hello",
  "build": 8290499,
  "chroot": "fedora-41-x86_64",
  "version": "0.74-1.20241121081717469764.pr2119.15.g9dfd54b",
  "status": 0,
  "ip": "2620:52:3:1:dead:beef:cafe:c18a",
  "who": "backend.worker-rpm_build_worker:8290499-fedora-41-x86_64",
  "pid": 1088192,
  "what": "build end: user:packit-stg copr:packit-hello-world-2119-latest build:8290499 pkg:hello version:0.74-1.20241121081717469764.pr2119.15.g9dfd54b ip:2620:52:3:1:dead:beef:cafe:c18a pid:1088192 status:0"
  "topic": "org.fedoraproject.prod.copr.build.end"
}
"""

copr_build_end_chroot_rawhide_copr_latest_ok = """
{
  "user": "packit-stg",
  "copr": "packit-hello-world-2119-latest",
  "owner": "packit-stg",
  "pkg": "hello",
  "build": 8290499,
  "chroot": "fedora-rawhide-x86_64",
  "version": "0.74-1.20241121081717469764.pr2119.15.g9dfd54b",
  "status": 1,
  "ip": "54.146.35.69",
  "who": "backend.worker-rpm_build_worker:8290499-fedora-rawhide-x86_64",
  "pid": 1088401,
  "what": "build end: user:packit-stg copr:packit-hello-world-2119-latest build:8290499 pkg:hello version:0.74-1.20241121081717469764.pr2119.15.g9dfd54b ip:54.146.35.69 pid:1088401 status:1"
  "topic": "org.fedoraproject.prod.copr.build.end"
}
"""

comment_retest_failed = """
{
  "action": "created",
  "issue": {
    "url": "https://api.github.com/repos/packit/hello-world/issues/2119",
    "repository_url": "https://api.github.com/repos/packit/hello-world",
    "labels_url": "https://api.github.com/repos/packit/hello-world/issues/2119/labels{/name}",
    "comments_url": "https://api.github.com/repos/packit/hello-world/issues/2119/comments",
    "events_url": "https://api.github.com/repos/packit/hello-world/issues/2119/events",
    "html_url": "https://github.com/packit/hello-world/pull/2119",
    "id": 2181757140,
    "node_id": "PR_kwDOCwFO9M5pYoI6",
    "number": 2119,
    "title": "Create a setup with two different tests",
    "user": {
      "login": "majamassarini",
      "id": 2678400,
      "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
      "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/majamassarini",
      "html_url": "https://github.com/majamassarini",
      "followers_url": "https://api.github.com/users/majamassarini/followers",
      "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
      "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
      "organizations_url": "https://api.github.com/users/majamassarini/orgs",
      "repos_url": "https://api.github.com/users/majamassarini/repos",
      "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
      "received_events_url": "https://api.github.com/users/majamassarini/received_events",
      "type": "User",
      "user_view_type": "public",
      "site_admin": false
    },
    "labels": [

    ],
    "state": "open",
    "locked": false,
    "assignee": null,
    "assignees": [

    ],
    "milestone": null,
    "comments": 16,
    "created_at": "2024-03-12T14:24:41Z",
    "updated_at": "2024-11-21T09:43:13Z",
    "closed_at": null,
    "author_association": "MEMBER",
    "active_lock_reason": null,
    "draft": false,
    "pull_request": {
      "url": "https://api.github.com/repos/packit/hello-world/pulls/2119",
      "html_url": "https://github.com/packit/hello-world/pull/2119",
      "diff_url": "https://github.com/packit/hello-world/pull/2119.diff",
      "patch_url": "https://github.com/packit/hello-world/pull/2119.patch",
      "merged_at": null
    },
    "body": null,
    "reactions": {
      "url": "https://api.github.com/repos/packit/hello-world/issues/2119/reactions",
      "total_count": 0,
      "+1": 0,
      "-1": 0,
      "laugh": 0,
      "hooray": 0,
      "confused": 0,
      "heart": 0,
      "rocket": 0,
      "eyes": 0
    },
    "timeline_url": "https://api.github.com/repos/packit/hello-world/issues/2119/timeline",
    "performed_via_github_app": null,
    "state_reason": null
  },
  "comment": {
    "url": "https://api.github.com/repos/packit/hello-world/issues/comments/2490589832",
    "html_url": "https://github.com/packit/hello-world/pull/2119#issuecomment-2490589832",
    "issue_url": "https://api.github.com/repos/packit/hello-world/issues/2119",
    "id": 2490589832,
    "node_id": "IC_kwDOCwFO9M6Uc2KI",
    "user": {
      "login": "majamassarini",
      "id": 2678400,
      "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
      "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/majamassarini",
      "html_url": "https://github.com/majamassarini",
      "followers_url": "https://api.github.com/users/majamassarini/followers",
      "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
      "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
      "organizations_url": "https://api.github.com/users/majamassarini/orgs",
      "repos_url": "https://api.github.com/users/majamassarini/repos",
      "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
      "received_events_url": "https://api.github.com/users/majamassarini/received_events",
      "type": "User",
      "user_view_type": "public",
      "site_admin": false
    },
    "created_at": "2024-11-21T09:43:10Z",
    "updated_at": "2024-11-21T09:43:10Z",
    "author_association": "MEMBER",
    "body": "/packit-stg retest-failed",
    "reactions": {
      "url": "https://api.github.com/repos/packit/hello-world/issues/comments/2490589832/reactions",
      "total_count": 0,
      "+1": 0,
      "-1": 0,
      "laugh": 0,
      "hooray": 0,
      "confused": 0,
      "heart": 0,
      "rocket": 0,
      "eyes": 0
    },
    "performed_via_github_app": null
  },
  "repository": {
    "id": 184635124,
    "node_id": "MDEwOlJlcG9zaXRvcnkxODQ2MzUxMjQ=",
    "name": "hello-world",
    "full_name": "packit/hello-world",
    "private": false,
    "owner": {
      "login": "packit",
      "id": 46870917,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2ODcwOTE3",
      "avatar_url": "https://avatars.githubusercontent.com/u/46870917?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/packit",
      "html_url": "https://github.com/packit",
      "followers_url": "https://api.github.com/users/packit/followers",
      "following_url": "https://api.github.com/users/packit/following{/other_user}",
      "gists_url": "https://api.github.com/users/packit/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/packit/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/packit/subscriptions",
      "organizations_url": "https://api.github.com/users/packit/orgs",
      "repos_url": "https://api.github.com/users/packit/repos",
      "events_url": "https://api.github.com/users/packit/events{/privacy}",
      "received_events_url": "https://api.github.com/users/packit/received_events",
      "type": "Organization",
      "user_view_type": "public",
      "site_admin": false
    },
    "html_url": "https://github.com/packit/hello-world",
    "description": "The most progresive command-line tool in the world.",
    "fork": false,
    "url": "https://api.github.com/repos/packit/hello-world",
    "forks_url": "https://api.github.com/repos/packit/hello-world/forks",
    "keys_url": "https://api.github.com/repos/packit/hello-world/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/packit/hello-world/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/packit/hello-world/teams",
    "hooks_url": "https://api.github.com/repos/packit/hello-world/hooks",
    "issue_events_url": "https://api.github.com/repos/packit/hello-world/issues/events{/number}",
    "events_url": "https://api.github.com/repos/packit/hello-world/events",
    "assignees_url": "https://api.github.com/repos/packit/hello-world/assignees{/user}",
    "branches_url": "https://api.github.com/repos/packit/hello-world/branches{/branch}",
    "tags_url": "https://api.github.com/repos/packit/hello-world/tags",
    "blobs_url": "https://api.github.com/repos/packit/hello-world/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/packit/hello-world/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/packit/hello-world/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/packit/hello-world/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/packit/hello-world/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/packit/hello-world/languages",
    "stargazers_url": "https://api.github.com/repos/packit/hello-world/stargazers",
    "contributors_url": "https://api.github.com/repos/packit/hello-world/contributors",
    "subscribers_url": "https://api.github.com/repos/packit/hello-world/subscribers",
    "subscription_url": "https://api.github.com/repos/packit/hello-world/subscription",
    "commits_url": "https://api.github.com/repos/packit/hello-world/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/packit/hello-world/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/packit/hello-world/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/packit/hello-world/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/packit/hello-world/contents/{+path}",
    "compare_url": "https://api.github.com/repos/packit/hello-world/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/packit/hello-world/merges",
    "archive_url": "https://api.github.com/repos/packit/hello-world/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/packit/hello-world/downloads",
    "issues_url": "https://api.github.com/repos/packit/hello-world/issues{/number}",
    "pulls_url": "https://api.github.com/repos/packit/hello-world/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/packit/hello-world/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/packit/hello-world/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/packit/hello-world/labels{/name}",
    "releases_url": "https://api.github.com/repos/packit/hello-world/releases{/id}",
    "deployments_url": "https://api.github.com/repos/packit/hello-world/deployments",
    "created_at": "2019-05-02T18:54:46Z",
    "updated_at": "2023-01-31T17:16:23Z",
    "pushed_at": "2024-11-21T04:50:20Z",
    "git_url": "git://github.com/packit/hello-world.git",
    "ssh_url": "git@github.com:packit/hello-world.git",
    "clone_url": "https://github.com/packit/hello-world.git",
    "svn_url": "https://github.com/packit/hello-world",
    "homepage": null,
    "size": 186,
    "stargazers_count": 4,
    "watchers_count": 4,
    "language": "Python",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "has_discussions": false,
    "forks_count": 23,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 98,
    "license": {
      "key": "mit",
      "name": "MIT License",
      "spdx_id": "MIT",
      "url": "https://api.github.com/licenses/mit",
      "node_id": "MDc6TGljZW5zZTEz"
    },
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "public",
    "forks": 23,
    "open_issues": 98,
    "watchers": 4,
    "default_branch": "main",
    "custom_properties": {

    }
  },
  "organization": {
    "login": "packit",
    "id": 46870917,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2ODcwOTE3",
    "url": "https://api.github.com/orgs/packit",
    "repos_url": "https://api.github.com/orgs/packit/repos",
    "events_url": "https://api.github.com/orgs/packit/events",
    "hooks_url": "https://api.github.com/orgs/packit/hooks",
    "issues_url": "https://api.github.com/orgs/packit/issues",
    "members_url": "https://api.github.com/orgs/packit/members{/member}",
    "public_members_url": "https://api.github.com/orgs/packit/public_members{/member}",
    "avatar_url": "https://avatars.githubusercontent.com/u/46870917?v=4",
    "description": "Packit service: package it in an automated way."
  },
  "sender": {
    "login": "majamassarini",
    "id": 2678400,
    "node_id": "MDQ6VXNlcjI2Nzg0MDA=",
    "avatar_url": "https://avatars.githubusercontent.com/u/2678400?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/majamassarini",
    "html_url": "https://github.com/majamassarini",
    "followers_url": "https://api.github.com/users/majamassarini/followers",
    "following_url": "https://api.github.com/users/majamassarini/following{/other_user}",
    "gists_url": "https://api.github.com/users/majamassarini/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/majamassarini/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/majamassarini/subscriptions",
    "organizations_url": "https://api.github.com/users/majamassarini/orgs",
    "repos_url": "https://api.github.com/users/majamassarini/repos",
    "events_url": "https://api.github.com/users/majamassarini/events{/privacy}",
    "received_events_url": "https://api.github.com/users/majamassarini/received_events",
    "type": "User",
    "user_view_type": "public",
    "site_admin": false
  },
  "installation": {
    "id": 1924121,
    "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uMTkyNDEyMQ=="
  }
}
"""

# pull_request_synchronize = json.loads(pull_request_synchronize)
# copr_build_end_chroot_rawhide_copr_rawhide_ok = json.loads(copr_build_end_chroot_rawhide_copr_rawhide_ok)
# copr_build_end_chroot_fedora_41_copr_rawhide_ko = json.loads(copr_build_end_chroot_fedora_41_copr_rawhide_ko)
# copr_build_end_chroot_fedora_41_copr_latest_ko = json.loads(copr_build_end_chroot_fedora_41_copr_latest_ko)
# copr_build_end_chroot_rawhide_copr_latest_ok = json.loads(copr_build_end_chroot_rawhide_copr_latest_ok)
comment_retest_failed = json.loads(comment_retest_failed)

celery_app: Celery = Proxy(get_celery_application)
# celery_app.send_task(
#    name="task.steve_jobs.process_message",
#    kwargs={"event": pull_request_synchronize},
# )


# celery_app.send_task(
#    name="task.steve_jobs.process_message",
#    kwargs={"event": copr_build_end_chroot_rawhide_copr_rawhide_ok},
# )
# celery_app.send_task(
#    name="task.steve_jobs.process_message",
#    kwargs={"event": copr_build_end_chroot_fedora_41_copr_rawhide_ko},
# )
# celery_app.send_task(
#    name="task.steve_jobs.process_message",
#    kwargs={"event": copr_build_end_chroot_fedora_41_copr_latest_ko},
# )
# celery_app.send_task(
#    name="task.steve_jobs.process_message",
#    kwargs={"event": copr_build_end_chroot_rawhide_copr_latest_ok},
# )


celery_app.send_task(
    name="task.steve_jobs.process_message",
    kwargs={"event": comment_retest_failed},
)
