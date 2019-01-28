import unittest


from github_tracker_cli import format_issue
from github_tracker_domain import Issue


class TestCli(unittest.TestCase):
    def test_printout_includes_github_issue_title(self):
        issue = Issue(
            number = 123,
            title = "Some title",
            url = 'http://example.com/some-url'
        )
        
        formatted_issue = format_issue(issue)

        self.assertIn("[Github Issue #123] Some title", formatted_issue)

