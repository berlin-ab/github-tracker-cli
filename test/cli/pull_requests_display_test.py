# -*- coding: utf-8 -*- 
import unittest


from github_tracker_cli.cli.pull_request_display import (
    print_pull_requests_as_rows,
)

from github_tracker_cli.github_tracker.domain import (
    PullRequest
)


printed_values = None


def reset_printed_values():
    global printed_values
    printed_values = []


def get_printed_values():
    global printed_values
    return printed_values


def sample_printer(some_string):
    get_printed_values().append(some_string)


class DisplayPullRequestsTest(unittest.TestCase):
    def setUp(self):
        reset_printed_values()
        
        self.pull_requests = [
            PullRequest(
                number=1234,
                title=u'Some cool title 错误',
                url=u'http://example.com/some-printable-url',
                author=u'me',
                last_updated_at=u'some-timestamp',
                labels=[]
            )
        ]

    def test_it_shows_the_number(self):
        print_pull_requests_as_rows(self.pull_requests, sample_printer)
        
        self.assertIn("1234", printed_values[0])

    def test_it_shows_the_author(self):
        print_pull_requests_as_rows(self.pull_requests, sample_printer)
        
        self.assertIn("me", printed_values[0])

    def test_it_shows_the_url(self):
        print_pull_requests_as_rows(self.pull_requests, sample_printer)
        
        self.assertIn("http://example.com/some-printable-url", printed_values[0])

    def test_it_shows_the_last_updated_timestamp(self):
        print_pull_requests_as_rows(self.pull_requests, sample_printer)
        
        self.assertIn("some-timestamp", printed_values[0])

    def test_it_shows_the_title(self):
        print_pull_requests_as_rows(self.pull_requests, sample_printer)
        
        self.assertIn("Some cool title", printed_values[0])


