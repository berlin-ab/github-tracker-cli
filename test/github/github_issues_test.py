import unittest
import datetime
from dateutil import tz


from github_tracker_cli.github.integration import GithubIssues, PullRequests
from github_tracker_cli.github_tracker.domain import Issue, PullRequest


class StubGithubApi():
    def __init__(self):
        self.stubbed_response = []
        self.used_path = None
    
    def stub_get(self, stubbed_response):
        self.stubbed_response = stubbed_response

    def get(self, path):
        self.used_path = path
        return self.stubbed_response
    

class BaseGithubIssuesTest():
    def test_it_can_fetch_github_issues(self):
        github_api = StubGithubApi()
        github_repo = 'some/repo'

        github_api.stub_get([
            {
                'number': 45678,
                'html_url': 'http://example.com',
                'title': 'Some title',
                'body': 'Some description',
            }
        ])
        
        issues = self.get_issues(github_api, github_repo)

        self.assertEqual(issues[0].number(), 45678)
        self.assertEqual(issues[0].url(), 'http://example.com')
        self.assertEqual(issues[0].description(), 'Some description')

    def test_it_discards_issues_that_have_pull_requests(self):
        github_api = StubGithubApi()
        github_repo = 'some/repo'

        github_api.stub_get([
            {
                'number': 45678,
                'html_url': 'http://example.com',
                'title': 'Some title',
                'body': '',
                'created_at': '2010-01-01T10:10:10Z',
                'updated_at': '2010-02-02T10:10:10Z',
            },
            {
                'number': 123,
                'html_url': 'http://example.com/pr',
                'title': 'Some pr',
                'body': '',
                'pull_request': {'url': 'http://example.com/some-pr-url'}
            }
        ])
        
        issues = self.get_issues(github_api, github_repo)
        self.assertEqual(1, len(issues))
        self.assertEqual(issues[0].number(), 45678)
        self.assertEqual(issues[0].url(), 'http://example.com')
        self.assertEqual(issues[0].created_at(), datetime.datetime(2010, 1, 1, 10, 10, 10, tzinfo=tz.tzutc()))
        self.assertEqual(issues[0].updated_at(), datetime.datetime(2010, 2, 2, 10, 10, 10, tzinfo=tz.tzutc()))

    def test_it_populates_the_issue_with_labels(self):
        github_api = StubGithubApi()
        github_repo = 'some/repo'

        github_api.stub_get([
            {
                'number': 45678,
                'html_url': 'http://example.com',
                'title': 'Some title',
                'body': '',
                'labels': [
                    {
                        'name': 'some-label'
                    }
                ]
            }
        ])

        issues = self.get_issues(github_api, github_repo)
        self.assertEqual(1, len(issues))
        self.assertEqual(['some-label'], issues[0].labels())

        
class OpenGithubIssuesTest(BaseGithubIssuesTest, unittest.TestCase):
    def get_issues(self, github_api, github_repo):
        return [issue for issue in GithubIssues(
            github_api=github_api,
            github_repo=github_repo,
        ).fetch()]

    def test_it_receives_the_github_issues_api_path_when_fetching(self):
        github_api = StubGithubApi()
        github_repo = 'berlin-ab/some-repo'
        
        issues = self.get_issues(github_api, github_repo)
        
        self.assertEqual(
            github_api.used_path,
            '/repos/berlin-ab/some-repo/issues?state=open'
            )


class PullRequestsTest(unittest.TestCase):
    def get_pull_requests(self, github_api, github_repo):
        return [pull_request for pull_request in PullRequests(
            github_api=github_api,
            github_repo=github_repo,
        ).fetch()]

    def test_it_returns_pull_requests(self):
        github_api = StubGithubApi()
        github_api.stub_get([
            {
                'number': 45678,
                'html_url': 'http://example.com/abc',
                'title': 'Some title abc',
                'body': '',
                'updated_at': '2010-01-01T10:10:10Z',
                'pull_request': {
                    'url': 'http://example.com/some-pr-api-url',
                    'html_url': 'http://example.com/some-pr-url'
                },
                'user': {
                    'login': 'some-github-author'
                }
            },
            {
                'number': 12345,
                'html_url': 'http://example.com/def',
                'title': 'Some title def',
                'updated_at': '9999-99-99T01:01:01Z',
                'body': '',
            },
        ])
        github_repo = 'berlin-ab/some-repo'
        
        pull_requests = self.get_pull_requests(github_api, github_repo)

        self.assertEqual(1, len(pull_requests))
        pull_request = pull_requests[0]
        self.assertEqual(45678, pull_request.number())
        self.assertEqual('http://example.com/some-pr-url', pull_request.url())
        self.assertEqual('Some title abc', pull_request.title())
        self.assertEqual(
            datetime.datetime(year=2010, month=1, day=1, hour=10, minute=10 ,second=10, tzinfo=tz.tzutc()),
            pull_request.last_updated_at()
        )
        self.assertEqual('some-github-author', pull_request.author())

