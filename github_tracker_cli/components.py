from github_tracker_cli.github.integration import (
    GithubApi,
    GithubIssues,
    PullRequests,
)

from github_tracker_cli.pivotal_tracker.integration import (PivotalTrackerApi, TrackerStories)

from github_tracker_cli.github_tracker.domain import (
    MissingStories,
    ClosedIssues,
    OpenPullRequests,
)


class Components():
    def __init__(self, arguments):
        self.arguments = arguments

    def tracker_api(self):
        return PivotalTrackerApi(
            api_token=self.arguments.pivotal_tracker_token
        )

    def github_api(self):
        return GithubApi()

    def github_issues(self):
        return  GithubIssues(
            github_api=self.github_api(),
            github_repo=self.arguments.github_repo
        )

    def tracker_stories(self):
        return TrackerStories(
            tracker_api=self.tracker_api()
        )

    def pull_requests(self):
        return PullRequests(
            github_api=self.github_api(),
            github_repo=self.arguments.github_repo,
        )
    
    def missing_stories(self):
        return MissingStories(
            tracker_stories=self.tracker_stories(),
            github_issues=self.github_issues()
        )
    
    def closed_issues(self):
        return ClosedIssues(
            tracker_stories=self.tracker_stories(),
            github_issues=self.github_issues()
        )

    def open_pull_requests(self):
        return OpenPullRequests(
            pull_requests=self.pull_requests()
        )
        
