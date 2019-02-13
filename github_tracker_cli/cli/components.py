from __future__ import print_function
from backports import csv


import os
import sys
import codecs


from github_tracker_cli.github.integration import (
    GithubApi,
    GithubIssues,
    PullRequests,
    OrganizationMembers,
)


from github_tracker_cli.pivotal_tracker.integration import (
    PivotalTrackerApi,
    TrackerStories
)


from github_tracker_cli.github_tracker.domain import (
    MissingStories,
    ClosedIssues,
    OpenPullRequests,
    GithubIssuesSearch,
)

class CsvWriter():
    def __init__(self, stdout):
        self.header_columns = []
        self.row_columns = []
        self.stdout = stdout
        
    def write_header(self, header_columns):
        self.internal_writer = csv.DictWriter(
            self.stdout,
            fieldnames=header_columns,
            quoting=csv.QUOTE_ALL
        )
        self.internal_writer.writeheader()

    def write_row(self, row_columns):
        self.internal_writer.writerow(row_columns)

    
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
            pull_requests=self.pull_requests()
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
    
