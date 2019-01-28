# Github Tracker CLI

A tool to help link issues and stories between Github and Pivotal Tracker.

As of 2019, there's no good way to automatically link Issues from Github to Stories in Pivotal Tracker.  For some open source projects, Github Issues is a great way to interact with the community of developers that want to contribute to the project. Also, those projects may also have a team that wants to keep a portion of the project discussion private.

`github-tracker-cli` is an attempt to make the management of an open source project that has external and internal priorities easier. 


## Installation

Installs all necessary dependencies.

Note: Assumes `pip` is installed.

```bash
./bin/install_dependencies
```


## Usage

### Commands:

`missing-stories`: 

Look through all Pivotal Tracker stories and find ones marked with a 'github-issue' label (by default) and with a title starting with "[Github Issue #123] Some title".  If there are open issues that do not have a corresponding story, display a url to the issue so that a story can be created for the issue.


```bash
usage: ./bin/github_tracker_cli [-h] missing-stories 
	                            --pivotal-tracker-token PIVOTAL_TRACKER_TOKEN
                                --pivotal-tracker-project-id PIVOTAL_TRACKER_PROJECT_ID
                                --pivotal-tracker-label PIVOTAL_TRACKER_LABEL
                                --github-repo GITHUB_REPO

optional arguments:
  -h, --help            show this help message and exit
  --pivotal-tracker-token PIVOTAL_TRACKER_TOKEN
                        Your personal pivotal tracker api token. See https://w
                        ww.pivotaltracker.com/help/articles/api_token/
  --pivotal-tracker-project-id PIVOTAL_TRACKER_PROJECT_ID
                        Pivotal Tracker project id.
                        https://www.pivotaltracker.com/n/projects/[PROJECTID]
  --github-repo GITHUB_REPO
                        The organization/username and repository name as a
                        string. For example: https://github.com/berlin-ab
                        /github-tracker-cli would use --github-repo='berlin-ab
                        /github-tracker-cli'						  
  --pivotal-tracker-label PIVOTAL_TRACKER_LABEL
                        A label used to categorize stories in Pivotal Tracker.
                        Default: github-issue
```

### Example

Shows all Github issues that do not have a corresponding Pivotal Tracker story.

```bash

# https://www.pivotaltracker.com/help/articles/api_token/
$ export PIVOTAL_TRACKER_TOKEN=[YOUR-TOKEN]

$ ./bin/github_tracker_cli missing-stories \
	         --pivotal-tracker-token $PIVOTAL_TRACKER_TOKEN \
			 --pivotal-tracker-label example-issue \
			 --pivotal-tracker-project-id 2230629 \
			 --github-repo berlin-ab/gpdb

2 : https://github.com/berlin-ab/gpdb/issues/2 : [Github Issue #2] Stub issue for integration test

```

### Development

#### Running the full test suite

```bash
export PIVOTAL_TRACKER_TOKEN='SOME_TOKEN'

./scripts/build.sh
```


### Notes: 

* the integration test suite needs a pivotal tracker api token to query tracker for project information
* this project assumes a public github project.


### Possible features:

* comment syncing from Github to Tracker
* automatic story creation

