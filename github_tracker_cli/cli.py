import os
import sys
import argparse


from github.integration import (GithubApi, GithubIssues)
from pivotal_tracker.integration import (PivotalTrackerApi, TrackerStories)
from github_tracker.domain import MissingStories

       
def format_issue(issue):
    try:
        title = u'[Github Issue #%s] %s' % (issue.number(), issue.title())
        labels = u"github-issue"
        description = issue.url()

        return {
            u'Title': title,
            u'Labels': labels,
            u'Description': description
        }
    except Exception as error:
        print "Failed to format issue:"
        print issue.number()
        print issue.title()
        print issue.url()
        raise error


def display_issues_as_csv(issues):
    from backports import csv
    import sys

    writer = csv.DictWriter(
        sys.stdout,
        [u'Title', u'Labels', u'Description'],
        quoting=csv.QUOTE_ALL
    )

    writer.writeheader()
    writer.writerows(map(format_issue,  issues))


def display_issues_as_rows(issues):
    for issue in issues:
        formatted_issue = format_issue(issue)
        
        print u'{id} | {title} | {url}'.format(
            id=unicode(issue.number()),
            title=unicode(issue.title()),
            url=unicode(issue.url()),
        )


def parse_arguments():
    default_tracker_label = 'github-issue'
    tracker_token_help_text = "Your personal pivotal tracker api token. See https://www.pivotaltracker.com/help/articles/api_token/"
    tracker_project_id_help_text = "Pivotal Tracker project id. https://www.pivotaltracker.com/n/projects/[PROJECTID]"
    tracker_label_help_text = "A label used to categorize stories in Pivotal Tracker. Default: --pivotal-tracker-label=%s" % default_tracker_label
    github_repo_help_text = "The organization/username and repository name as a string. For example: https://github.com/berlin-ab/github-tracker-cli would use --github-repo='berlin-ab/github-tracker-cli'"
    csv_help_text = "Display output in Pivotal Tracker csv format. (default: false)"
    github_label_help_text = "Return Github Issues matching the given label. (optional)"
    
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

    missing_stories_parser.add_argument('--csv',
                                        help=csv_help_text,
                                        action='store_true')

    missing_stories_parser.add_argument('--github-label',
                                       help=github_label_help_text,
                                       default=None)
    
    return parser.parse_args()


def get_display_style(arguments):
    if arguments.csv:
        return display_issues_as_csv

    return display_issues_as_rows


def main(arguments=None):
    if arguments is None:
        arguments = parse_arguments()

    #
    # Components
    #
    tracker_api = PivotalTrackerApi(
        api_token=arguments.pivotal_tracker_token
    )
    
    github_api = GithubApi()

    github_issues = GithubIssues(
        github_api=github_api,
        github_repo=arguments.github_repo
    )

    tracker_stories = TrackerStories(
        tracker_api=tracker_api
    )

    missing_stories = MissingStories(
        tracker_stories = tracker_stories,
        github_issues = github_issues
    )

    #
    # Query and display issues
    #
    get_display_style(arguments)(
        issues=missing_stories.issues_not_in_tracker(
            project_id=arguments.pivotal_tracker_project_id,
            label=arguments.pivotal_tracker_label,
            github_label=arguments.github_label,
        )
    )
   







