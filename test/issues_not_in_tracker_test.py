import unittest

from github_tracker_domain import (Story, Issue, App)


class StubTrackerStories():
    def stub(self, stories):
        self._stories = stories

    def fetch_by_label(self):
        return self._stories

    
class StubGithubIssues():
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
            Issue(number=123),
            Issue(number=456),
            Issue(number=789)
        ])

        app = App(tracker_stories, github_issues)
        issues = app.issues_not_in_tracker()

        self.assertEqual([456], [issue.number() for issue in issues])
