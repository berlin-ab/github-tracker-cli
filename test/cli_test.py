# -*- coding: utf-8 -*- 
import unittest


from github_tracker_cli.cli import format_issue
from github_tracker.domain import Issue


class TestCli(unittest.TestCase):
    def test_printout_includes_github_issue_title(self):
        issue = Issue(
            number=123,
            title="Some title",
            url='http://example.com/some-url',
            labels=[]
        )
        
        formatted_issue = format_issue(issue)

        self.assertIn("[Github Issue #123] Some title", formatted_issue['Title'])

    def test_formatting_can_handle_unicode_characters(self):
        title = u"-错误的版本"
        issue = Issue(
            number=123,
            title=title,
            url="http://example.com/",
            labels=[]
        )
        formatted_issue = format_issue(issue)
        self.assertIn(title, formatted_issue['Title'])

