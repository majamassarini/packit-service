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

comment_copr_build_event = """
{
  "total_commits": 2,
  "start_commit": "44742d731eb4a74e5abf0c3a113b0609ccd0b745",
  "end_commit": "fe01a99843805bf2eed16146ae91e3e87333f52d",
  "old_commit": "37bd1f0639e8f4c1140dd1d3060bfdb1e38c23ec",
  "branch": "f39",
  "forced": false,
  "authors": [
    {
      "name": "mmassari",
      "fullname": "Maja Massarini",
      "url_path": "user/mmassari",
      "full_url": "https://src.fedoraproject.org/user/mmassari"
    },
    {
      "fullname": "Packit",
      "name": null,
      "url_path": null
    }
  ],
  "changed_files": {
    ".packit.yaml": "M"
  },
  "agent": "mmassari",
  "repo": {
    "id": 34882,
    "name": "packit",
    "fullname": "rpms/packit",
    "url_path": "rpms/packit",
    "full_url": "https://src.fedoraproject.org/rpms/packit",
    "description": "A set of tools to integrate upstream open source projects into Fedora operating system",
    "namespace": "rpms",
    "parent": null,
    "date_created": "1552485797",
    "date_modified": "1672657173",
    "user": {
      "name": "lachmanfrantisek",
      "fullname": "František Lachman",
      "url_path": "user/lachmanfrantisek",
      "full_url": "https://src.fedoraproject.org/user/lachmanfrantisek"
    },
    "access_users": {
      "owner": [
        "lachmanfrantisek"
      ],
      "admin": [
        "lbarczio",
        "mfocko",
        "ttomecek"
      ],
      "commit": [
        "mmassari",
        "nforro",
        "nikromen"
      ],
      "collaborator": [],
      "ticket": []
    },
    "access_groups": {
      "admin": [],
      "commit": [],
      "collaborator": [],
      "ticket": []
    },
    "tags": [
      ""
    ],
    "priorities": {},
    "custom_keys": [],
    "close_status": [],
    "milestones": {}
  },
  "pull_request_id": 1286,
  "headers": {
    "sent-at": "2024-09-18T13:31:56+00:00",
    "fedora_messaging_schema": "pagure.git.receive",
    "fedora_messaging_severity": 20,
    "fedora_messaging_user_mmassari": true
  },
  "id": "5b3d9e08-5e14-4bf2-83df-9f8fa8323f01",
  "priority": 0,
  "queue": null,
  "topic": "org.fedoraproject.prod.pagure.git.receive"
}
"""

event = json.loads(comment_copr_build_event)
celery_app: Celery = Proxy(get_celery_application)
celery_app.send_task(
    name="task.steve_jobs.process_message",
    kwargs={"event": event},
)
