import unittest


from github_tracker_cli.github_tracker.domain import (
    TrackerStoryHistory,
    Story,
    )


from github_tracker_cli.cli.story_display import (
    display_history_as_rows,
    )


class StoryDisplayTest(unittest.TestCase):

    def test_it_displays_the_story_url(self):
        lines = []

        def dummy_printer(message):
            lines.append(message)

        history = TrackerStoryHistory(
            started_duration=None,
            story=Story(
                story_id=123,
                url="http://example.com/some-story-url",
            )
        )
            
        display_history_as_rows([history], dummy_printer)
            
        self.assertIn("http://example.com/some-story-url", lines[0])

