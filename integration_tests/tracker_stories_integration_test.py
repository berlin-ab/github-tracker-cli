import unittest
import os


from github_tracker_cli.pivotal_tracker.integration import (
    TrackerStories,
    PivotalTrackerApi,
    MissingPivotalTrackerApiTokenError
)


def get_api_token():
    return  os.environ.get('PIVOTAL_TRACKER_TOKEN', None)


class TrackerStoriesIntegrationTest(unittest.TestCase):
    def test_fetching_a_list_of_tracker_stories_by_label(self):
        tracker_api = PivotalTrackerApi(api_token=get_api_token())
        
        stories = [story for story in TrackerStories(tracker_api).fetch_by_label(
            project_id=2241335,
            label='example-label'
            )]

        self.assertIn(163577442, [story.story_id() for story in stories])
        self.assertIn('Example backlog story', [story.title() for story in stories])
        
    def test_api_throws_missing_api_token_error(self):
        with self.assertRaises(MissingPivotalTrackerApiTokenError):
            tracker_api = PivotalTrackerApi(api_token=None)
                        
    def test_it_returns_stories_from_the_icebox(self):
        tracker_api = PivotalTrackerApi(api_token=get_api_token())
        
        stories = TrackerStories(tracker_api).fetch_by_label(
            project_id=2241335,
            label='example-label'
            )

        self.assertIn('Example icebox story', [story.title() for story in stories])






