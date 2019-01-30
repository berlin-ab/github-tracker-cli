# Github Tracker CLI

A tool to help link issues and stories between Github and Pivotal Tracker.

For some open source projects, Github Issues is a great way to interact with the community of developers that want to contribute to the project. Also, those projects may want to track the priority of the Issues using Pivotal Tracker.

`github-tracker-cli` is an attempt to make the management of an open source project that has external and internal priorities easier. 


## Installation

Installs all necessary dependencies.

Note: Assumes `pip` is installed.

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


## Usage

### Commands:

`missing-stories`: 

Look through all Pivotal Tracker stories and find ones marked with a 'github-issue' label (by default) and with a title starting with "[Github Issue #123] Some title".  If there are open issues that do not have a corresponding story, display a url to the issue so that a story can be created for the issue.


```bash
usage: ./bin/github_tracker_cli missing-stories [-h] 
    --pivotal-tracker-token PIVOTAL_TRACKER_TOKEN
    --pivotal-tracker-project-id PIVOTAL_TRACKER_PROJECT_ID
    --github-repo GITHUB_REPO
    [--pivotal-tracker-label PIVOTAL_TRACKER_LABEL]
    [--csv]
    [--github-label GITHUB_LABEL]

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
                        Default: --pivotal-tracker-label=github-issue
  --csv                 Display output in Pivotal Tracker csv format.
                        (default: false)
  --github-label GITHUB_LABEL
                        Return Github Issues matching the given label.
                        (optional)
```

`--csv` option:

The output format is the CSV import format of Pivotal Tracker. 

* output the stories into a csv file using output redirection:

	`$ ./bin/github_tracker_cli [OPTIONS] > github-issues.csv`

* Transform `github-issues.csv` into stories by visiting `https://www.pivotaltracker.com/projects/[PROJECT_ID]/settings` and navigating to 'Import CSV' from the left sidebar.

(note: you might need to remove a trailing newline from the csv file)

`closed-issues`: 

Display Tracker stories whose Github Issues have been closed.

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

    github_tracker_cli -> (github -> github_tracker <- pivotal_tracker)
	

### Notes: 

* the integration test suite needs a pivotal tracker api token to query tracker for project information
* this project assumes a public github project.


### Possible features:

* comment syncing from Github to Tracker
* automatic story creation

