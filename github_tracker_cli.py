import os
import sys
import argparse


from github_integration import (GithubApi, GithubIssues)
from pivotal_tracker_integration import (PivotalTrackerApi, TrackerStories)
from github_tracker_domain import App


def format_issue(issue):
    try:
        title = "[Github Issue #%s] %s" % (issue.number(), issue.title())
        labels = "github-issue"
        description = issue.url()

        return (
            "{title},{labels},{description}".format(
                title=title,
                labels=labels,
                description=description
            )
        )
    except Exception as error:
        print "Failed to format issue:"
        print issue.number()
        print issue.title()
        print issue.url()
        raise error


def print_issue(formatted_issue):
    print formatted_issue

    
def display_issues(app, tracker_project_id, tracker_label):
    print("Title,Labels,Description")
    
    map(print_issue, map(format_issue,  app.issues_not_in_tracker(
        project_id=tracker_project_id,
        label=tracker_label,
    )))
    

def parse_arguments():
    default_tracker_label = 'github-issue'
    tracker_token_help_text = "Your personal pivotal tracker api token. See https://www.pivotaltracker.com/help/articles/api_token/"
    tracker_project_id_help_text = "Pivotal Tracker project id. https://www.pivotaltracker.com/n/projects/[PROJECTID]"
    tracker_label_help_text = "A label used to categorize stories in Pivotal Tracker. Default: --pivotal-tracker-label=%s" % default_tracker_label
    github_repo_help_text = "The organization/username and repository name as a string. For example: https://github.com/berlin-ab/github-tracker-cli would use --github-repo='berlin-ab/github-tracker-cli'"

    
    parser = argparse.ArgumentParser(
        prog='./bin/github_tracker_cli',
    )
    subparsers = parser.add_subparsers()
    
    missing_stories_parser = subparsers.add_parser('missing-stories')
    missing_stories_parser.add_argument('--pivotal-tracker-token',
                                        required=True,
                                        help=tracker_token_help_text)
    
    missing_stories_parser.add_argument('--pivotal-tracker-project-id',
                                        required=True,
                                        help=tracker_project_id_help_text)

    missing_stories_parser.add_argument('--github-repo',
                                        required=True,
                                        help=github_repo_help_text)

    missing_stories_parser.add_argument('--pivotal-tracker-label',
                                        help=tracker_label_help_text,
                                        default=default_tracker_label)
    
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
    
