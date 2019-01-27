# Github Tracker CLI

A tool to help link issues and stories between Github and Pivotal Tracker.

* Look through all Pivotal Tracker stories and find ones marked with a 'github-issue' label and with a title starting with "[Github Issue #123] Some title".  If there are open issues that do not have a corresponding story, display a url to the issue so that a story can be created for the issue.

## Example

* see `./scripts/example.bash` for an example.

```bash
± |master U:1 ✗| → ./scripts/example.bash
issue=2 : url=https://github.com/berlin-ab/gpdb/issues/2 : story-title=[Github Issue #2]
```

## Development

```bash
export PIVOTAL_TRACKER_TOKEN='SOME_TOKEN'

./scripts/build.sh
```

Note: the integration test suite needs a pivotal tracker api token to query tracker for project information

