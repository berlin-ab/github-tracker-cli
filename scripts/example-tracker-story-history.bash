#!/usr/bin/env bash


export PYTHONIOENCODING=utf_8
./bin/github_tracker_cli tracker-story-history \
			 --pivotal-tracker-token $PIVOTAL_TRACKER_TOKEN \
			 --pivotal-tracker-project-id=2241335 | sort -k 2 -t '|' -n
