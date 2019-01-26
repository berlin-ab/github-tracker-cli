#/usr/bin/env bash

export PIVOTAL_TRACKER_PROJECT_ID='2230629'
export PIVOTAL_TRACKER_LABEL='example-issue'
export PYTHONPATH=$PWD:$PYTHONPATH

./bin/github_tracker_cli
