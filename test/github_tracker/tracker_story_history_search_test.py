import unittest

from github_tracker_cli.github_tracker.domain import (
    TrackerStoryHistory,
    TrackerStoryHistorySearch,
)

from test_helpers import (
    make_story,
)


class StubGetTrackerStoryHistory():

    def __init__(self):
        self._stubbed_history = []

    def stub(self, stubbed_history):
        self._stubbed_history = stubbed_history
        
    def fetch(self, project_id):
        return self._stubbed_history


class TrackerStoryHistorySearchTest(unittest.TestCase):
    def test_history_can_calculate_started_duration_in_days(self):
        history = TrackerStoryHistory(
            started_duration=(2 * 24 * 60 * 60 * 1000),
            story=None,
        )

        self.assertEqual(2, history.started_duration_in_days())

    def test_it_does_not_return_stories_that_are_of_type_release(self):
        stub_get_tracker_story_history = StubGetTrackerStoryHistory()
        stub_get_tracker_story_history.stub([
            TrackerStoryHistory(
                started_duration=1,
                story=make_story(story_type='feature')
            ),
            TrackerStoryHistory(
                started_duration=1,
                story=make_story(story_type='release')
            ),
            TrackerStoryHistory(
                started_duration=1,
                story=make_story(story_type='chore')
            ),
        ])
        
        search = TrackerStoryHistorySearch(
            get_tracker_story_history=stub_get_tracker_story_history
        )

        self.assertEqual(search.all_history(project_id=123)[0].story().story_type(), 'feature')
        self.assertEqual(2, len(search.all_history(project_id=123)))

