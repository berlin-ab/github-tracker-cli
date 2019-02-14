import unittest

from github_tracker_cli.github_tracker.domain import (
    TrackerStoryHistory,
)

class TrackerStoryHistorySearchTest(unittest.TestCase):
    def test_history_can_calculate_started_duration_in_days(self):
        history = TrackerStoryHistory(
            started_duration=(2 * 24 * 60 * 60 * 1000),
            story=None,
        )

        self.assertEqual(2, history.started_duration_in_days())
