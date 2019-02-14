import argparse


default_tracker_label = 'github-issue'
tracker_token_help_text = "Your personal pivotal tracker api token. See https://www.pivotaltracker.com/help/articles/api_token/"
tracker_project_id_help_text = "Pivotal Tracker project id. https://www.pivotaltracker.com/n/projects/[PROJECTID]"
tracker_label_help_text = "Filter (case-insensitive) by a label used to categorize stories in Pivotal Tracker. Default: --pivotal-tracker-label=%s" % default_tracker_label
github_repo_help_text = "The organization/username and repository name as a string. For example: https://github.com/berlin-ab/github-tracker-cli would use --github-repo='berlin-ab/github-tracker-cli'"
csv_help_text = "Display output in Pivotal Tracker csv format. (default: false)"
github_label_help_text = "Return Github Issues matching the given label (case insensitive). (optional)"
exclude_github_label_help_text = "Filter out github issues that match the given label"
exclude_organizations_help_text = "Filter out github issues that were created by someone that belongs to a given organization. "


def _add_github_arguments(parser):
    parser.add_argument('--github-repo',
                                        required=True,
                                        help=github_repo_help_text)

def _add_pivotal_tracker_authentication_arguments(parser):
    parser.add_argument('--pivotal-tracker-token',
                                        required=True,
                                        help=tracker_token_help_text)


def _add_pivotal_tracker_project_arguments(parser):
    parser.add_argument('--pivotal-tracker-project-id',
                                        required=True,
                                        help=tracker_project_id_help_text)
    
    
def _add_pivotal_tracker_arguments(parser):
    _add_pivotal_tracker_authentication_arguments(parser)
    _add_pivotal_tracker_project_arguments(parser)
    parser.add_argument('--pivotal-tracker-label',
                                        help=tracker_label_help_text,
                                        default=default_tracker_label)

    
def _add_shared_arguments(parser):
    _add_pivotal_tracker_arguments(parser)
    _add_github_arguments(parser)


def _add_exclude_github_labels(parser):
    parser.add_argument('--exclude-github-label',
                        help=exclude_github_label_help_text,
                        default=None)

    
def _add_missing_stories_parser(subparsers):
    parser = subparsers.add_parser('missing-stories')
    _add_shared_arguments(parser)
    _add_exclude_github_labels(parser)
    
    parser.add_argument('--csv',
                                        help=csv_help_text,
                                        action='store_true')

    parser.add_argument('--github-label',
                                       help=github_label_help_text,
                                       default=None)

    
def _add_exclude_organizations_argument(parser):
    parser.add_argument('--exclude-organizations',
                        nargs="*",
                        help=exclude_organizations_help_text,
                        default=[])


def _add_closed_issues_parser(subparsers):
    parser = subparsers.add_parser('closed-issues')
    _add_shared_arguments(parser)

    
def _add_pull_requests_parser(subparsers):
    parser = subparsers.add_parser('pull-requests')
    _add_github_arguments(parser)
    _add_exclude_github_labels(parser)


def _add_github_issues_parser(subparsers):
    parser = subparsers.add_parser('github-issues')
    _add_github_arguments(parser)
    _add_exclude_organizations_argument(parser)


def _add_tracker_story_history_parser(subparsers):
    parser = subparsers.add_parser('tracker-story-history')
    _add_pivotal_tracker_authentication_arguments(parser)
    _add_pivotal_tracker_project_arguments(parser)
        

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='./bin/github_tracker_cli',
    )
    subparsers = parser.add_subparsers(dest='chosen_command')
    _add_missing_stories_parser(subparsers)
    _add_closed_issues_parser(subparsers)
    _add_pull_requests_parser(subparsers)
    _add_github_issues_parser(subparsers)
    _add_tracker_story_history_parser(subparsers)
    
    return parser.parse_args()

