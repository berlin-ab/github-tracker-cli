import os
import sys
import argparse
import codecs



from github_tracker_cli.github_tracker.domain import (
    MissingStories,
    ClosedIssues
)

from github_tracker_cli.components import Components
from github_tracker_cli.issue_display import get_issues_display_style
from github_tracker_cli.story_display import display_stories_as_rows


default_tracker_label = 'github-issue'
tracker_token_help_text = "Your personal pivotal tracker api token. See https://www.pivotaltracker.com/help/articles/api_token/"
tracker_project_id_help_text = "Pivotal Tracker project id. https://www.pivotaltracker.com/n/projects/[PROJECTID]"
tracker_label_help_text = "Filter (case-insensitive) by a label used to categorize stories in Pivotal Tracker. Default: --pivotal-tracker-label=%s" % default_tracker_label
github_repo_help_text = "The organization/username and repository name as a string. For example: https://github.com/berlin-ab/github-tracker-cli would use --github-repo='berlin-ab/github-tracker-cli'"
csv_help_text = "Display output in Pivotal Tracker csv format. (default: false)"
github_label_help_text = "Return Github Issues matching the given label (case insensitive). (optional)"



def add_shared_arguments(parser):
    parser.add_argument('--pivotal-tracker-token',
                                        required=True,
                                        help=tracker_token_help_text)
    
    parser.add_argument('--pivotal-tracker-project-id',
                                        required=True,
                                        help=tracker_project_id_help_text)

    parser.add_argument('--github-repo',
                                        required=True,
                                        help=github_repo_help_text)

    parser.add_argument('--pivotal-tracker-label',
                                        help=tracker_label_help_text,
                                        default=default_tracker_label)


def add_missing_stories_parser(subparsers):
    parser = subparsers.add_parser('missing-stories')
    add_shared_arguments(parser)
    parser.add_argument('--csv',
                                        help=csv_help_text,
                                        action='store_true')

    parser.add_argument('--github-label',
                                       help=github_label_help_text,
                                       default=None)

    
def add_closed_issues_parser(subparsers):
    parser = subparsers.add_parser('closed-issues')
    add_shared_arguments(parser)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='./bin/github_tracker_cli',
    )
    subparsers = parser.add_subparsers(dest='chosen_command')
        
    add_missing_stories_parser(subparsers)
    add_closed_issues_parser(subparsers)
    return parser.parse_args()


def missing_stories_runner(components):
    arguments = components.arguments
    
    missing_stories = MissingStories(
        tracker_stories=components.tracker_stories,
        github_issues=components.github_issues
    )

    issues = missing_stories.issues_not_in_tracker(
        project_id=arguments.pivotal_tracker_project_id,
        label=arguments.pivotal_tracker_label,
        github_label=arguments.github_label,
    )
    
    display_style = get_issues_display_style(arguments)
    display_style(issues)
 

def closed_issues_runner(components):
    arguments = components.arguments
    
    closed_issues = ClosedIssues(
        tracker_stories=components.tracker_stories,
        github_issues=components.github_issues
    )

    display_stories_as_rows(
        closed_issues.fetch(
            project_id=arguments.pivotal_tracker_project_id,
            tracker_label=arguments.pivotal_tracker_label,
        )
    )
 

def unknown_subcommand_runner(components):
    print "Unknown command."

        
def discover_subcommand(arguments):
    if arguments.chosen_command == 'missing-stories':
        return missing_stories_runner

    elif arguments.chosen_command == 'closed-issues':
        return closed_issues_runner

    else:
        return unknown_subcommand_runner
    
            
def main():
    # Ensure that writing to standard out and to a pipe is via utf8
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    arguments = parse_arguments()
    components = Components(arguments)
    subcommand = discover_subcommand(arguments)
    subcommand(components)


