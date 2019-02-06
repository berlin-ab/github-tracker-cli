import unittest


from github_tracker_cli.github_tracker.domain import (
    OpenPullRequests,
    PullRequest
)

class StubPullRequests():
    def fetch(self):
        return [
            PullRequest(
                number=123,
                url='http://example.com/some-pull-request-url',
                title='Some title',
                last_updated_at='some-time-stamp',
                author='some-github-username',
            )
        ]

class OpenPullRequestsTest(unittest.TestCase):
    def test_it_returns_pull_requests(self):
        stub_pull_requests = StubPullRequests()
        open_pull_requests = OpenPullRequests(stub_pull_requests)
        pull_requests = open_pull_requests.fetch()
        pull_request = pull_requests[0]
        
        self.assertEqual(123, pull_request.number())
        self.assertEqual('http://example.com/some-pull-request-url', pull_request.url())
        self.assertEqual('Some title', pull_request.title())
        self.assertEqual('some-time-stamp', pull_request.last_updated_at())
        self.assertEqual('some-github-username', pull_request.author())
        
