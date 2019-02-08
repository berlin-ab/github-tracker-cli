from github_tracker_cli.cli.issue_display import get_issues_display_style
from github_tracker_cli.cli.story_display import display_stories_as_rows
from github_tracker_cli.cli.pull_request_display import print_pull_requests_as_rows


def missing_stories_runner(components):
    arguments = components.arguments
    missing_stories = components.missing_stories()

    issues = missing_stories.issues_not_in_tracker(
        project_id=arguments.pivotal_tracker_project_id,
        label=arguments.pivotal_tracker_label,
        github_label=arguments.github_label,
        exclude_github_label=arguments.exclude_github_label,
    )
    
    display_style = get_issues_display_style(
        csv=arguments.csv
    )
    
    display_style(issues, components.printer())
 

def closed_issues_runner(components):
    arguments = components.arguments
    
    closed_issues = components.closed_issues()

    display_stories_as_rows(
        closed_issues.fetch(
            project_id=arguments.pivotal_tracker_project_id,
            tracker_label=arguments.pivotal_tracker_label,
        ),
        components.printer()
    )


def pull_requests_runner(components):
    pull_requests = components.open_pull_requests()
    print_pull_requests_as_rows(pull_requests.fetch(), components.printer())
    

def unknown_subcommand_runner(components):
    printer = components.printer()
    printer("Unknown command")


def discover_subcommand(arguments):
    if arguments.chosen_command == 'missing-stories':
        return missing_stories_runner

    elif arguments.chosen_command == 'closed-issues':
        return closed_issues_runner

    elif arguments.chosen_command == 'pull-requests':
        return pull_requests_runner
    
    else:
        return unknown_subcommand_runner
