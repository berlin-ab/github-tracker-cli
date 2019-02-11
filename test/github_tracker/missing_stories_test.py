import unittest
import datetime


from github_tracker_cli.github_tracker.domain import (
    Story,
    Issue,
    MissingStories
)


from .test_helpers import (
    StubTrackerStories,
    StubGithubIssues,
    valid_issue,
    make_story,
)
    

class MissingStoriesTest(unittest.TestCase):
    def test_list_issues_that_are_not_in_tracker(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()

        tracker_stories.stub([
            make_story(title='[Github Issue #123] Some title.'),
            make_story(title='[Github Issue #789] Some other title.'),
            make_story(title='Non-github issue title')
        ])
        
        github_issues.stub([
            valid_issue(number=123, url='http://example.com/foo'),
            valid_issue(number=456, url='http://example.com/bar'),
            valid_issue(number=789, url='http://example.com/baz'),
        ])

        app = MissingStories(tracker_stories, github_issues)
        issues = app.issues_not_in_tracker(
            project_id=123,
            label='something'
        )

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

    def test_issue_are_filtered_by_github_label_case_insensitive(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()
        app = MissingStories(
            tracker_stories,
            github_issues
        )

        github_issues.stub([
            valid_issue(number=2, labels=["matching"]),
            valid_issue(number=3, labels=["not-matching"]),
        ])

        issues = app.issues_not_in_tracker(
            project_id=123,
            label='foobar',
            github_label='Matching',
        )
        
        self.assertEqual(
            [2], [issue.number() for issue in issues])

    def test_it_filters_out_excluded_labels(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()
        app = MissingStories(
            tracker_stories,
            github_issues
        )

        github_issues.stub([
            valid_issue(number=2, labels=["some-label"]),
            valid_issue(number=3, labels=["some-excluded-label"]),
        ])

        issues = app.issues_not_in_tracker(
            project_id=123,
            label='foobar',
            exclude_github_label='some-excluded-label',
        )
        
        self.assertEqual(
            [2], [issue.number() for issue in issues])
        
