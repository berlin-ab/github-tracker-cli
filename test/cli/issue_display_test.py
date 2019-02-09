# -*- coding: utf-8 -*- 
import unittest
import datetime


from github_tracker_cli.cli.issue_display import (
     get_issues_display_style
)

from github_tracker_cli.github_tracker.domain import Issue


def make_issue(number=123,
               title="Some title",
               description='Something',
               url='http://example.com/some-url',
               created_at=datetime.datetime.now(),
               updated_at=datetime.datetime.now(),
               author_user_id='some-author-user-id',
):
    return Issue(
        number=123,
        title=title,
        url=url,
        description=description,
        labels=[],
        created_at=created_at,
        updated_at=updated_at,
        author_user_id=author_user_id,
    )


class IssueDisplayTest(unittest.TestCase):
    def test_printout_includes_github_issue_title(self):
        formatted_issues = []

        def dummy_printer(string):
            formatted_issues.append(string)
        
        formatter = get_issues_display_style(csv=False)
        
        issue = make_issue(number=123, title="Some title")

        formatter([issue], dummy_printer)

        self.assertIn("[Github Issue #123] Some title", formatted_issues[0])

    def test_formatting_can_handle_unicode_characters(self):
        formatted_issues = []

        def dummy_printer(string):
            formatted_issues.append(string)
        
        formatter = get_issues_display_style(csv=False)

        title = u"-错误的版本"
        issue = make_issue(title=title)

        formatter([issue], dummy_printer)
        
        self.assertIn(title, formatted_issues[0])

    def test_formatted_description_includes_issue_url(self):
        formatted_issues = []

        def dummy_printer(string):
            formatted_issues.append(string)
        
        formatter = get_issues_display_style(csv=False)

        issue = make_issue(
            url="http://example.com/foobar",
        )

        formatter([issue], dummy_printer)

        self.assertIn("http://example.com/foobar", formatted_issues[0])

    def test_it_includes_updated_at_date(self):
        formatted_issues = []

        def dummy_printer(string):
            formatted_issues.append(string)
        
        formatter = get_issues_display_style(csv=False)

        issue = make_issue(
            updated_at=datetime.datetime(year=2000, month=1, day=1)
            )

        formatter([issue], dummy_printer)

        self.assertIn("2000-", formatted_issues[0])

    def test_it_includes_created_at_date(self):
        formatted_issues = []

        def dummy_printer(string):
            formatted_issues.append(string)
        
        formatter = get_issues_display_style(csv=False)

        issue = make_issue(
            updated_at=datetime.datetime(year=1999, month=1, day=1)
        )

        formatter([issue], dummy_printer)

        self.assertIn("1999-", formatted_issues[0])
        
