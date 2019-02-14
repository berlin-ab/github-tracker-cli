#/usr/bin/env bash

./bin/github_tracker_cli closed-issues \
    --pivotal-tracker-token $PIVOTAL_TRACKER_TOKEN \
    --pivotal-tracker-label github-issue \
    --pivotal-tracker-project-id 2241335 \
    --github-repo berlin-ab/github-tracker-cli "$@"

