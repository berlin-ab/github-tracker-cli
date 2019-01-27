import os
import sys
import argparse


from github_integration import (GithubApi, GithubIssues)
from pivotal_tracker_integration import (PivotalTrackerApi, TrackerStories)
from github_tracker_domain import App


def print_issue(issue):
    print "issue=%s : url=%s : story-title=[Github Issue #%s] " % (issue.number(), issue.url(), issue.number())

    
def display_issues(app, tracker_project_id, tracker_label):
    map(print_issue,  app.issues_not_in_tracker(
        project_id=tracker_project_id,
        label=tracker_label,
    ))
    

def parse_arguments():
    parser = argparse.ArgumentParser(prog='./bin/github_tracker_cli')
    parser.add_argument('--pivotal-tracker-token', required=True)
    parser.add_argument('--pivotal-tracker-project-id', required=True)
    parser.add_argument('--pivotal-tracker-label', required=True)
    parser.add_argument('--github-repo', required=True)
    return parser.parse_args()

    
def main(arguments=parse_arguments()):
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
    
