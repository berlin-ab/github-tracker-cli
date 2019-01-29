import unittest

from github_tracker.domain import (
    Story,
    Issue,
    MissingStories
)


class StubTrackerStories():
    def __init__(self):
        self._stories = []
        self.used_project_id = None
        self.used_label = None
        
    def stub(self, stories):
        self._stories = stories

    def fetch_by_label(self, project_id, label):
        self.used_project_id = project_id
        self.used_label = label
        return self._stories

    
class StubGithubIssues():
    def __init__(self):
        self._issues = []

    def stub(self, issues):
        self._issues = issues

    def fetch(self):
        return self._issues


def valid_issue(
        number=123,
        url='http://example.com/foo',
        title="A title",
        labels=[]):

    return Issue(
        number=number,
        url=url,
        title=title,
        labels=labels
    )

class IssuesNotInTrackerTest(unittest.TestCase):
    def test_list_issues_that_are_not_in_tracker(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()

        tracker_stories.stub([
            Story(external_id='unimportant', title='[Github Issue #123] Some title.'),
            Story(external_id='something', title='[Github Issue #789] Some other title.'),
            Story(external_id=None, title='Non-github issue title')
        ])
        
        github_issues.stub([
            Issue(
                number=123,
                url='http://example.com/foo',
                title="A title",
                labels=[],
            ),
            Issue(
                number=456,
                url='http://example.com/bar',
                title="B title",
                labels=[],
            ),
            Issue(
                number=789,
                url='http://example.com/baz',
                title="C title",
                labels=[],
            ),
        ])

        app = MissingStories(tracker_stories, github_issues)
        issues = app.issues_not_in_tracker(project_id=123, label='something')

        self.assertEqual([456], [issue.number() for issue in issues])
        self.assertIn('http://example.com/bar', [issue.url() for issue in issues])

    def test_tracker_stories_are_filtered_by_project_id_and_label(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()
        app = MissingStories(tracker_stories, github_issues)
        issues = app.issues_not_in_tracker(project_id=123, label='foobar')

        self.assertEqual(123, tracker_stories.used_project_id)
        self.assertEqual('foobar', tracker_stories.used_label)

    def test_issue_are_filtered_by_github_label(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()
        app = MissingStories(
            tracker_stories,
            github_issues
        )

        github_issues.stub([
            valid_issue(number=1, labels=[]),
            valid_issue(number=2, labels=["matching"]),
            valid_issue(number=3, labels=["not-matching"]),
        ])

        issues = app.issues_not_in_tracker(
            project_id=123,
            label='foobar',
            github_label='matching',
        )
        
        self.assertEqual(
            [2], [issue.number() for issue in issues])
