import unittest
import time


from github_tracker_cli.github_tracker.domain import (
    OpenPullRequests,
)

from test_helpers import (
    make_pull_request,
    StubPullRequests,
    parse_date,
)


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
        self.assertEqual('some-github-username', pull_request.author_user_id())
        
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

    def test_it_filters_out_pull_requests_matching_the_excluded_label(self):
        stub_pull_requests = StubPullRequests()
        stub_pull_requests.stub([
            make_pull_request(number=456, labels=['abc']),
            make_pull_request(number=789, labels=['def']),
            make_pull_request(number=123, labels=['ghi']),
        ])
        
        open_pull_requests = OpenPullRequests(stub_pull_requests)
        pull_requests = open_pull_requests.fetch(
            exclude_github_label='def'
        )

        self.assertEqual(
            [456, 123],
            [pull_request.number() for pull_request in pull_requests]
        )

    def test_it_filters_out_pull_requests_matching_the_excluded_label_with_case_insensitive_match(self):
        stub_pull_requests = StubPullRequests()
        stub_pull_requests.stub([
            make_pull_request(number=456, labels=['Abc']),
            make_pull_request(number=789, labels=['def']),
            make_pull_request(number=123, labels=['ghi']),
        ])
        
        open_pull_requests = OpenPullRequests(stub_pull_requests)
        pull_requests = open_pull_requests.fetch(
            exclude_github_label='abc'
        )

        self.assertEqual(
            [789, 123],
            [pull_request.number() for pull_request in pull_requests]
        )
