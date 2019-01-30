import unittest


from github_tracker_cli.github_tracker.domain import (
    ClosedIssues,
    Issue,
    Story,
)


def make_story(title='', story_id=1):
    return Story(
        story_id=story_id,
        title=title,
        external_id=None
    )


def make_issue(number=000,
               url='',
               title='',
               labels=[],
               description=''):
    return Issue(
        number=number,
        url=url,
        title=title,
        labels=labels,
        description=description
    )
    pass


class StubGithubIssues():
    def __init__(self):
        self._stubbed_issues = []

    def stub(self, stubbed_issues):
        self._stubbed_issues = stubbed_issues

    def fetch(self):
        return self._stubbed_issues
    

class StubTrackerStories():
    def __init__(self):
        self._stubbed_stories = []
        self.used_label = None
        self.used_project_id = None
        
    def fetch_by_label(self, project_id, label):
        self.used_label = label
        self.used_project_id = project_id
        return self._stubbed_stories
            
    def stub(self, stubbed_stories):
        self._stubbed_stories = stubbed_stories


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


