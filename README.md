# Github Tracker CLI

A tool to help link issues and stories between Github and Pivotal Tracker.

* Look through all Pivotal Tracker stories and find ones marked with a 'github-issue' label and with a title starting with "[Github Issue #123] Some title".  If there are open issues that do not have a corresponding story, display a url to the issue so that a story can be created for the issue.

## Example

* see `./scripts/example.bash` for an example.

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
