from github_tracker_cli.cli.issue_display import (
    display_issues_as_rows,
    display_issues_as_csv,
)

from github_tracker_cli.cli.story_display import (
    display_stories_as_rows,
    display_history_as_rows,
)

from github_tracker_cli.cli.pull_request_display import (
    print_pull_requests_as_rows,
)


def missing_stories_runner(components):
    arguments = components.arguments
    missing_stories = components.missing_stories()

    issues = missing_stories.issues_not_in_tracker(
        project_id=arguments.pivotal_tracker_project_id,
        label=arguments.pivotal_tracker_label,
        github_label=arguments.github_label,
        exclude_github_label=arguments.exclude_github_label,
    )

    if arguments.csv:
        display_issues_as_csv(issues, components.csv_writer(), components.printer())
    else:
        display_issues_as_rows(issues, components.printer())
     

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
    arguments = components.arguments
    pull_requests = components.open_pull_requests()
    
    print_pull_requests_as_rows(
        pull_requests.fetch(
            exclude_github_label=arguments.exclude_github_label,
            exclude_organizations=arguments.exclude_organizations,
        ),
        components.printer()
    )

def github_issues_runner(components):
    arguments = components.arguments
    github_issues_search = components.github_issues_search()

    display_issues_as_rows(
        github_issues_search.fetch(
            exclude_organizations=components.arguments.exclude_organizations
        ),
        components.printer()
    )
    

def tracker_story_history_runner(components):
    search = components.tracker_story_history_search()
    story_histories = search.all_history(
        project_id=components.arguments.pivotal_tracker_project_id
    )

    display_history_as_rows(story_histories, components.printer())


def unknown_subcommand_runner(components):
    printer = components.printer()
    printer("Unknown command")


def discover_subcommand(arguments):
    commands = {
        'missing-stories': missing_stories_runner,
        'closed-issues': closed_issues_runner,
        'pull-requests': pull_requests_runner,
        'github-issues': github_issues_runner,
        'tracker-story-history': tracker_story_history_runner,
    }
    
    return commands.get(
        arguments.chosen_command,
        unknown_subcommand_runner
    )
