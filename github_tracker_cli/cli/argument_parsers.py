import argparse


default_tracker_label = 'github-issue'
tracker_token_help_text = "Your personal pivotal tracker api token. See https://www.pivotaltracker.com/help/articles/api_token/"
tracker_project_id_help_text = "Pivotal Tracker project id. https://www.pivotaltracker.com/n/projects/[PROJECTID]"
tracker_label_help_text = "Filter (case-insensitive) by a label used to categorize stories in Pivotal Tracker. Default: --pivotal-tracker-label=%s" % default_tracker_label
github_repo_help_text = "The organization/username and repository name as a string. For example: https://github.com/berlin-ab/github-tracker-cli would use --github-repo='berlin-ab/github-tracker-cli'"
csv_help_text = "Display output in Pivotal Tracker csv format. (default: false)"
github_label_help_text = "Return Github Issues matching the given label (case insensitive). (optional)"


def add_github_arguments(parser):
    parser.add_argument('--github-repo',
                                        required=True,
                                        help=github_repo_help_text)

def add_pivotal_tracker_arguments(parser):
    parser.add_argument('--pivotal-tracker-token',
                                        required=True,
                                        help=tracker_token_help_text)
    
    parser.add_argument('--pivotal-tracker-project-id',
                                        required=True,
                                        help=tracker_project_id_help_text)

    parser.add_argument('--pivotal-tracker-label',
                                        help=tracker_label_help_text,
                                        default=default_tracker_label)

    
def add_shared_arguments(parser):
    add_pivotal_tracker_arguments(parser)
    add_github_arguments(parser)


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

    
def add_pull_requests_parser(subparsers):
    parser = subparsers.add_parser('pull-requests')
    add_github_arguments(parser)
    

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='./bin/github_tracker_cli',
    )
    subparsers = parser.add_subparsers(dest='chosen_command')
        
    add_missing_stories_parser(subparsers)
    add_closed_issues_parser(subparsers)
    add_pull_requests_parser(subparsers)
    return parser.parse_args()

