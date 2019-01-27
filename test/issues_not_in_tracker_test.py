import unittest

from github_tracker_domain import (Story, Issue, App)


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


class IssuesNotInTrackerTest(unittest.TestCase):
    def test_list_issues_that_are_not_in_tracker(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()

        tracker_stories.stub([
            Story(external_id='123'),
            Story(external_id='789'),
            Story(external_id=None)
        ])
        
        github_issues.stub([
            Issue(number=123, url='http://example.com/foo'),
            Issue(number=456, url='http://example.com/bar'),
            Issue(number=789, url='http://example.com/baz'),
        ])

        app = App(tracker_stories, github_issues)
        issues = app.issues_not_in_tracker(project_id=123, label='something')

        self.assertEqual([456], [issue.number() for issue in issues])
        self.assertIn('http://example.com/bar', [issue.url() for issue in issues])

    def test_tracker_stories_are_filtered_by_project_id_and_label(self):
        tracker_stories = StubTrackerStories()
        github_issues = StubGithubIssues()
        app = App(tracker_stories, github_issues)
        issues = app.issues_not_in_tracker(project_id=123, label='foobar')

        self.assertEqual(123, tracker_stories.used_project_id)
        self.assertEqual('foobar', tracker_stories.used_label)
        
