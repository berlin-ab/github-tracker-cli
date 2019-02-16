from __future__ import print_function


import os
import sys
import codecs


from github_tracker_cli.csv.csv_writer import (
    CsvWriter,
)


from github_tracker_cli.github.integration import (
    GithubApi,
    GithubIssues,
    PullRequests,
    OrganizationMembers,
)


from github_tracker_cli.pivotal_tracker.integration import (
    PivotalTrackerApi,
    TrackerStories,
    GetTrackerStoryHistory,
)


from github_tracker_cli.github_tracker.domain import (
    MissingStories,
    ClosedIssues,
    OpenPullRequests,
    GithubIssuesSearch,
    TrackerStoryHistorySearch,
)


class Components():
    def __init__(self, arguments):
        self.arguments = arguments

    def log(self, message):
        if os.environ.get('DEBUG'):
            self._printer(message)
        
    def printer(self):
        return lambda message: self.stdout().write(message + "\n")

    def tracker_api(self):
        return PivotalTrackerApi(
            api_token=self.arguments.pivotal_tracker_token
        )

    def github_api(self):
        return GithubApi(
            logger=self.log,
            printer=(lambda message: self.stdout().write(message + "\n")),
            credentials=self._github_credentials()
        )

    def github_issues(self):
        return GithubIssues(
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
            pull_requests=self.pull_requests(),
            organization_members=self.organization_members()
        )

    def github_issues_search(self):
        return GithubIssuesSearch(
            github_issues=self.github_issues(),
            organization_members=self.organization_members(),
        )

    def organization_members(self):
        return OrganizationMembers(
            github_api=self.github_api()
        )

    def get_tracker_story_history(self):
        return GetTrackerStoryHistory(
            tracker_api=self.tracker_api()
            )
    
    def tracker_story_history_search(self):
        return TrackerStoryHistorySearch(
            get_tracker_story_history=self.get_tracker_story_history()
            )

    def stdout(self):
        if not sys.stdout.encoding:
            raise RuntimeError("System requires ability to write utf-8 to standard out. Please set the environment variable: PYTHONIOENCODING=utf_8")
        
        return sys.stdout
    
    def csv_writer(self):
        return CsvWriter(self.stdout())
        
    def _github_credentials(self):
        github_username = os.environ.get('GITHUB_USERNAME', None)
        github_password = os.environ.get('GITHUB_PASSWORD', None)
        
        if github_username and github_password:
            return (github_username, github_password)

        return ()
    
