# Github Tracker CLI

A tool to help link issues and stories between Github and Pivotal Tracker.

For some open source projects, Github Issues is a great way to interact with the community of developers that want to contribute to the project. Also, those projects may want to track the priority of the Issues using Pivotal Tracker.

`github-tracker-cli` is an attempt to make the management of an open source project that has external and internal priorities easier. 

[![Build Status](https://travis-ci.com/berlin-ab/github-tracker-cli.svg?branch=master)](https://travis-ci.com/berlin-ab/github-tracker-cli)

## Installation

Installs all necessary dependencies.

Notes: 

- Assumes `pip` is installed
- Supported python versions:
  - 2.7.x
  - 3.7.x

```bash
$ git clone https://github.com/berlin-ab/github-tracker-cli.git
Cloning into 'github-tracker-cli'...
remote: Enumerating objects: 307, done.
remote: Counting objects: 100% (307/307), done.
remote: Compressing objects: 100% (197/197), done.
remote: Total 307 (delta 175), reused 219 (delta 89), pack-reused 0
Receiving objects: 100% (307/307), 38.55 KiB | 5.51 MiB/s, done.
Resolving deltas: 100% (175/175), done.

$ cd github-tracker-cli

$ ./bin/install_dependencies
Collecting requests (from -r requirements.txt (line 1))
...
```


## Setting up your project

**Step 1:** Label Github Issues you'd like to import into your Pivotal Tracker backlog.

**Step 2:** Prepare Github Issues you've already entered into Pivotal Tracker:

	- Label the stories with 'github-issue'
	- Put the story number in the title (including a #) For example, "[Github #1234] Some github issue title"
	
**Step 3:** Export the Github Issues as a CSV using `./bin/github_tracker_cli missing-stories`

**Step 4:** Import the CSV file into your Pivotal Tracker backlog. 


## Usage

### Commands:


```
± |master ✓| → ./bin/github_tracker_cli --help
usage: ./bin/github_tracker_cli [-h]
                                {missing-stories,closed-issues,pull-requests,github-issues,tracker-story-history}
                                ...

positional arguments:
  {missing-stories,closed-issues,pull-requests,github-issues,tracker-story-history}

optional arguments:
  -h, --help            show this help message and exit
```


#### missing-stories: 

Look through all Pivotal Tracker stories and find ones marked with a 'github-issue' label (by default) and with a title starting with "[Github Issue #123] Some title".  If there are open issues that do not have a corresponding story, display a url to the issue so that a story can be created for the issue.

#### closed-issues: 

Display Tracker stories whose Github Issues have been closed.

#### pull-requests:

List pull requests from a Github Repository

#### github-issues:

Show all github issues for a repository.

Note: for best results with `--exclude-organizations` authenticate with Github using a personal access token by setting these environment variables: 

```
export GITHUB_USERNAME=[YOUR USERNAME]
export GITHUB_PASSWORD=[YOUR PERSONAL ACCESS TOKEN]
```

Github will only return public members of an organization if you are not authenticated, which makes the results inaccurate if the issues are created by private members of the excluded organization. Ensure that **public repo information** and **organization info** scopes are enabled for your personal access token.


### Example

Shows all Github issues matching a Github label that do not have a corresponding Pivotal Tracker story output in Pivotal Tracker CSV format.

```

# https://www.pivotaltracker.com/help/articles/api_token/
export PIVOTAL_TRACKER_TOKEN=[YOUR-TOKEN]

./bin/github_tracker_cli missing-stories \
    --pivotal-tracker-token $PIVOTAL_TRACKER_TOKEN \
    --pivotal-tracker-label example-issue \
    --pivotal-tracker-project-id 2241335 \
    --github-repo berlin-ab/github-tracker-cli \
	--github-label version-1.0 \
    --csv

"Title","Labels","Description"
"[Github Issue #2] Stub issue for integration test","github-issue","https://github.com/berlin-ab/github-tracker-cli/issues/2"
```

### Development

#### Running the full test suite

```bash
export PIVOTAL_TRACKER_TOKEN='SOME_TOKEN'

./scripts/build.sh
```

#### Running the integration test suite

```bash
export PIVOTAL_TRACKER_TOKEN='SOME_TOKEN'

./scripts/integration-test.sh
```

#### Running the unit test suite

```bash
./scripts/unit-test.sh
```

#### Planned work and issues

* https://www.pivotaltracker.com/n/projects/2241335
* https://github.com/berlin-ab/github-tracker-cli/issues

#### Project Structure


`bin/`: user-facing runnable applications

`scripts/`: developer-facing utilities

`github_tracker_cli`: core namespace

`github_tracker_cli/cli.py`: argument parsing and output formatting

`github_tracker_cli/github_tracker`: dependency-free logic and domain definition

`github_tracker_cli/pivotal_tracker`: adapting layer between Pivotal Tracker API and `github_tracker`

`github_tracker_cli/github`: adapting layer between Github API and `github_tracker`


Module dependency structure:

    cli -> (github -> github_tracker <- pivotal_tracker)

#### Debugging environment variables:

    # enable verbose logging
	export DEBUG=true 
	
	# enable github authentication
	export GITHUB_USERNAME=[some value]
	export GITHUB_PASSWORD=[some personal access token]
	

### Notes: 

* the integration test suite needs a pivotal tracker api token to query tracker for project information
* this project assumes a public github project.


### Possible features:

* comment syncing from Github to Tracker
* automatic story creation

