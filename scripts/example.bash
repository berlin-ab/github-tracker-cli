#/usr/bin/env bash

export PYTHONPATH=$PWD:$PYTHONPATH

./bin/github_tracker_cli --pivotal-tracker-token $PIVOTAL_TRACKER_TOKEN \
			 --pivotal-tracker-label example-issue \
			 --pivotal-tracker-project-id 2230629 \
			 --github-repo berlin-ab/gpdb

