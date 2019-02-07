import unittest
import time


from github_tracker_cli.github_tracker.domain import (
    OpenPullRequests,
    PullRequest
)


def parse_date(date_string):
    return time.strptime(date_string, "%Y-%m-%d")


def make_pull_request(
                number=123,
                url='http://example.com/some-pull-request-url',
                title='Some title',
                last_updated_at=parse_date('2010-01-01'),
                author='some-github-username',
            ):
    return PullRequest(
        number=number,
        url=url,
        title=title,
        last_updated_at=last_updated_at,
        author=author,
    )


class StubPullRequests():
    def __init__(self):
        self._stubbed_pull_requests = []
        
    def stub(self, pull_requests):
        self._stubbed_pull_requests = pull_requests
        
    def fetch(self):
        return self._stubbed_pull_requests
        

class OpenPullRequestsTest(unittest.TestCase):
    def test_it_returns_pull_requests(self):
        stub_pull_requests = StubPullRequests()
        stub_pull_requests.stub([make_pull_request()])
        
        open_pull_requests = OpenPullRequests(stub_pull_requests)
        pull_requests = open_pull_requests.fetch()
        pull_request = pull_requests[0]
        
        self.assertEqual(123, pull_request.number())
        self.assertEqual('http://example.com/some-pull-request-url', pull_request.url())
        self.assertEqual('Some title', pull_request.title())
        self.assertEqual(parse_date('2010-01-01'), pull_request.last_updated_at())
        self.assertEqual('some-github-username', pull_request.author())
        
    def test_it_orders_the_results_based_on_last_updated_descending(self):
        stub_pull_requests = StubPullRequests()
        stub_pull_requests.stub([
            make_pull_request(number=456, last_updated_at=parse_date('2010-01-01')),
            make_pull_request(number=789, last_updated_at=parse_date('2050-01-01')),
            make_pull_request(number=123, last_updated_at=parse_date('2000-01-01')),
        ])

        
        open_pull_requests = OpenPullRequests(stub_pull_requests)
        pull_requests = open_pull_requests.fetch()

        self.assertEqual([789, 456, 123], [pull_request.number() for pull_request in pull_requests])
