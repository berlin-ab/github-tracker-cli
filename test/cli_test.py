# -*- coding: utf-8 -*- 
import unittest


from github_tracker_cli.cli import format_issue
from github_tracker.domain import Issue


def make_issue(number=123,
               title="Some title",
               description='Something',
               url='http://example.com/some-url'):
    return Issue(
        number=123,
        title=title,
        url=url,
        description=description,
        labels=[]
    )


class TestCli(unittest.TestCase):
    
    def test_printout_includes_github_issue_title(self):
        issue = make_issue(number=123, title="Some title")
        formatted_issue = format_issue(issue)

        self.assertIn("[Github Issue #123] Some title", formatted_issue['Title'])

    def test_formatting_can_handle_unicode_characters(self):
        title = u"-错误的版本"
        issue = make_issue(title=title)

        formatted_issue = format_issue(issue)
        self.assertIn(title, formatted_issue['Title'])

    def test_formatted_description_includes_issue_description_and_url(self):
        issue = make_issue(
            url="http://example.com/foobar",
            description="Something else"
        )

        formatted_issue = format_issue(issue)
        self.assertIn("Something else", formatted_issue['Description'])
        self.assertIn("http://example.com/foobar", formatted_issue['Description'])

