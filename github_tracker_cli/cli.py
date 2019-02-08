from __future__ import print_function


import os
import sys
import codecs


from github_tracker_cli.github_tracker.domain import (
    MissingStories,
    ClosedIssues,
    OpenPullRequests,
)


from github_tracker_cli.argument_parsers import parse_arguments
from github_tracker_cli.components import Components
from github_tracker_cli.issue_display import get_issues_display_style
from github_tracker_cli.story_display import display_stories_as_rows
from github_tracker_cli.pull_request_display import print_pull_requests_as_rows


def printer(string):
    print(string)


def missing_stories_runner(components):
    arguments = components.arguments
    
    missing_stories = MissingStories(
        tracker_stories=components.tracker_stories(),
        github_issues=components.github_issues()
    )

    issues = missing_stories.issues_not_in_tracker(
        project_id=arguments.pivotal_tracker_project_id,
        label=arguments.pivotal_tracker_label,
        github_label=arguments.github_label,
    )
    
    display_style = get_issues_display_style(
        csv=arguments.csv
    )
    
    display_style(issues, printer)
 

def closed_issues_runner(components):
    arguments = components.arguments
    
    closed_issues = ClosedIssues(
        tracker_stories=components.tracker_stories(),
        github_issues=components.github_issues()
    )

    display_stories_as_rows(
        closed_issues.fetch(
            project_id=arguments.pivotal_tracker_project_id,
            tracker_label=arguments.pivotal_tracker_label,
        ),
        printer
    )


def pull_requests_runner(components):
    command = OpenPullRequests(components.pull_requests())
    print_pull_requests_as_rows(command.fetch(), printer)
    

def unknown_subcommand_runner(components):
    printer("Unknown command.")

        
def discover_subcommand(arguments):
    if arguments.chosen_command == 'missing-stories':
        return missing_stories_runner

    elif arguments.chosen_command == 'closed-issues':
        return closed_issues_runner

    elif arguments.chosen_command == 'pull-requests':
        return pull_requests_runner
    
    else:
        return unknown_subcommand_runner
    

def main():
    # Ensure that writing to standard out and to a pipe is via utf8
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    arguments = parse_arguments()
    components = Components(arguments)
    subcommand = discover_subcommand(arguments)
    subcommand(components)

