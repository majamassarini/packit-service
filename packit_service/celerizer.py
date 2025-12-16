# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

from os import getenv

from celery import Celery
from lazy_object_proxy import Proxy

from packit_service.sentry_integration import configure_sentry


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

comment_logdetective_analysis_event = """
{
  "log_detective_response": {
    "explanation": {
      "text": "The RPM build failed due to a test setup failure and a specific test case \\"XXXX\\" failing. The overall result of the build process was also reported as FAIL.\\nTo resolve this, investigate the test setup environment and the failing test case to identify the root cause.",
      "logprobs": null
    },
    "response_certainty": 0.0,
    "snippets": [
      {
        "explanation": {
          "text": "The snippet indicates uncertainty about an event that occured during the build.",
          "relevance": 95
        },
        "text": "What happened?",
        "line_number": 0
      },
      {
        "explanation": {
          "text": "The log snippet indicates a generic failure during an RPM build process. The message 'Failure!' suggests that a command or script executed during the build returned a non-zero exit code, halting the process.",
          "relevance": 95
        },
        "text": "Failure!",
        "line_number": 0
      }
    ]
  },
  "target_build": "138590969",
  "build_system": "koji",
  "result": "complete",
  "log_detective_analysis_id": "4f2fa9aa-8fe6-4325-a317-473ca180e75d",
  "identifier": "4f2fa9aa-8fe6-4325-a317-473ca180e75d",
  "log_detective_analysis_start": "2025-12-10 10:57:57.341695+00:00",
  "commit_sha": "975c6aff7ad4cf71e546970c2f14232d962a595b",
  "project_url": "https://src.fedoraproject.org/rpms/python-ogr",
  "pr_id": 867,
  "task_id": 18304,
  "headers": {
    "fedora_messaging_schema": "base.message",
    "fedora_messaging_severity": 20,
    "priority": 0,
    "sent-at": "2024-10-20T03:44:53+00:00"
  },
  "id": "36b9d2be-5452-467d-8503-d68462e8aa74",
  "priority": 0,
  "queue": null,
  "topic": "logdetective.analysis"
}
"""

event = json.loads(comment_logdetective_analysis_event)
celery_app: Celery = Proxy(get_celery_application)
celery_app.send_task(
    name="task.steve_jobs.process_message",
    kwargs={"event": event},
)

# podman-compose up -d postgres
# podman cp ~/forges/github/packit-service/packit--stg_database_packit.sql postgres:/tmp/packit.sql
# podman-compose exec postgres bash
# psql -U packit -d packit < /tmp/packit.sql
# exit
# podman-compose up -d service
# podman-compose exec postgres psql -U packit -d packit
# _service-- Create a new group (or use an existing one's ID)
# INSERT INTO log_detective_run_groups (submitted_time)
# VALUES (NOW())
# RETURNING id;
#
# -- Then use that ID in your insert
# INSERT INTO log_detective_run (
#     status,
#     analysis_id,
#     target_build,
#     build_system,
#     target,
#     identifier,
#     submitted_time,
#     koji_build_target_id,
#     log_detective_run_group_id
# )
# VALUES (
#     'running',
#     '4f2fa9aa-8fe6-4325-a317-473ca180e75d',
#     '138590969',
#     'koji',
#     'x86_64',
#     'once-in-a-while',
#     NOW(),
#     '1906',
#     (SELECT id FROM log_detective_run_groups ORDER BY id DESC LIMIT 1)
# );

# -- Find the PipelineModel associated with the koji build group
# -- and update it to link to the log_detective_run_group
# UPDATE pipelines
# SET log_detective_run_group_id = (
#    SELECT log_detective_run_group_id
#    FROM log_detective_run
#    WHERE analysis_id = '4f2fa9aa-8fe6-4325-a317-473ca180e75d'
#    LIMIT 1
# )
# WHERE koji_build_group_id = (
#    SELECT koji_build_group_id
#    FROM koji_build_targets
#    WHERE id = '1906'
# );

# exit
# podman-compose up worker
# debug...
# podman-compose down
# netstat -tulpn | grep 5678
# kill any
