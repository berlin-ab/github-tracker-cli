import os
import sys
import argparse


from github_integration import (GithubApi, GithubIssues)
from pivotal_tracker_integration import (PivotalTrackerApi, TrackerStories)
from github_tracker_domain import App


def format_issue(issue):
    return (
        "issue=%s : url=%s : story-title=[Github Issue #%s] %s" % (
            issue.number(),
            issue.url(),
            issue.number(),
            issue.title(),
        )
    )


def print_issue(formatted_issue):
    print formatted_issue

    
def display_issues(app, tracker_project_id, tracker_label):
    map(print_issue, map(format_issue,  app.issues_not_in_tracker(
        project_id=tracker_project_id,
        label=tracker_label,
    )))
    

def parse_arguments():
    parser = argparse.ArgumentParser(prog='./bin/github_tracker_cli')
    parser.add_argument('--pivotal-tracker-token', required=True, help="Your personal pivotal tracker api token. See https://www.pivotaltracker.com/help/articles/api_token/")
    parser.add_argument('--pivotal-tracker-project-id', required=True, help="Pivotal Tracker project id. https://www.pivotaltracker.com/n/projects/[PROJECTID]")
    parser.add_argument('--pivotal-tracker-label', required=True, help="A label used to categorize stories in Pivotal Tracker. For example: some-label")
    parser.add_argument('--github-repo', required=True, help="The organization/username and repository name as a string. For example: https://github.com/berlin-ab/github-tracker-cli would use --github-repo='berlin-ab/github-tracker-cli'")
    return parser.parse_args()

    
def main(arguments=None):
    if arguments is None:
        arguments = parse_arguments()
        
    pivotal_tracker_token = arguments.pivotal_tracker_token
    tracker_project_id = arguments.pivotal_tracker_project_id
    tracker_label = arguments.pivotal_tracker_label
    github_repo = arguments.github_repo
    
    tracker_api = PivotalTrackerApi(
        api_token=pivotal_tracker_token
    )
    
    github_api = GithubApi()

    app = App(
        tracker_stories = TrackerStories(
            tracker_api=tracker_api
        ),
        github_issues = GithubIssues(
            github_api=github_api,
            github_repo=github_repo
        )
    )

    display_issues(app, tracker_project_id, tracker_label)
    
