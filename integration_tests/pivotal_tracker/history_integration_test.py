import unittest
import os


from github_tracker_cli.pivotal_tracker.integration import (
    PivotalTrackerApi,
    GetTrackerStoryHistory,
    )

from github_tracker_cli.github_tracker.domain import (
    Story,
    TrackerStoryHistory,
    )


def get_api_token():
    return os.environ.get('PIVOTAL_TRACKER_TOKEN')

    
class TrackerStoryCycleTimeIntegrationTest(unittest.TestCase):
    def test_it_returns_story_churn_info(self):
        tracker_api = PivotalTrackerApi(api_token=get_api_token())
        
        histories = GetTrackerStoryHistory(tracker_api).fetch(project_id=2241335)

        self.assertIn('Example backlog story', [
            history.story().title()
            for history
            in histories
        ])

        self.assertIn(1299402000, [
            history.started_duration()
            for history
            in histories
        ])
