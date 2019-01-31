from github_tracker_cli.github.integration import (GithubApi, GithubIssues)
from github_tracker_cli.pivotal_tracker.integration import (PivotalTrackerApi, TrackerStories)


class Components():
    def __init__(self, arguments):
        self.arguments = arguments
        
        self.tracker_api = PivotalTrackerApi(
            api_token=arguments.pivotal_tracker_token
        )
        
        self.github_api = GithubApi()
        
        self.github_issues = GithubIssues(
            github_api=self.github_api,
            github_repo=arguments.github_repo
        )
        
        self.tracker_stories = TrackerStories(
            tracker_api=self.tracker_api
        )

