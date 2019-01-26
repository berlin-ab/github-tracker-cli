# Github Tracker CLI

A tool to help link issues and stories between Github and Pivotal Tracker.

## Development

```
export PIVOTAL_TRACKER_TOKEN='SOME_TOKEN'

./scripts/build.sh
```

Note: the integration test suite needs a pivotal tracker api token to query tracker for project information

Goal:

./github-tracker-cli --show-missing-issues
#1234,Some issue title
#5678,Some other issue title
#2343,Another issue title
#5678,Another other issue title
