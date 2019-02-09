import unittest


from github_tracker_cli.github_tracker.domain import (
    ClosedIssues,
)


from test_helpers import (
    make_story,
    make_issue,
    StubGithubIssues,
    StubTrackerStories,
)


class ClosedIssuesTest(unittest.TestCase):
        
    def test_shows_no_issues_when_no_stories(self):
        github_issues = StubGithubIssues()
        tracker_stories = StubTrackerStories()

        app = ClosedIssues(
            github_issues=github_issues,
            tracker_stories=tracker_stories,
        )
        
        self.assertEqual([], app.fetch(
            project_id=111,
            tracker_label='',
        ))

    def test_shows_issue_with_story_not_in_issue_numbers(self):
        github_issues = StubGithubIssues()
        tracker_stories = StubTrackerStories()

        github_issues.stub([
            make_issue(number=222),
        ])
        
        tracker_stories.stub([
            make_story(story_id=456, title="#222"),
            make_story(story_id=123, title="#111"),
        ])
        
        app = ClosedIssues(
            github_issues=github_issues,
            tracker_stories=tracker_stories,
        )

        self.assertEqual(
            [123],
            [story.story_id() for story in app.fetch(
                project_id=999,
                tracker_label='foobar'
            )]
        )

    def test_it_queries_tracker_with_label_and_project_id(self):
        github_issues = StubGithubIssues()
        tracker_stories = StubTrackerStories()
        
        app = ClosedIssues(
            github_issues=github_issues,
            tracker_stories=tracker_stories,
        )
        
        app.fetch(project_id=111, tracker_label='sample')

        self.assertEqual('sample', tracker_stories.used_label)
        self.assertEqual(111, tracker_stories.used_project_id)


