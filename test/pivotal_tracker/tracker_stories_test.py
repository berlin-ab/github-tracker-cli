import unittest


from github_tracker_cli.pivotal_tracker.integration import TrackerStories
from github_tracker_cli.github_tracker.domain import Story


class StubTrackerApi():
    def __init__(self):
        self.get_was_called = False
        self.stubbed_responses = []
        
    def stub_get(self, stubbed_responses):
        self.stubbed_responses = stubbed_responses
        pass

    def get(self, path):
        self.get_was_called_with = path
        return self.stubbed_responses


class TrackerStoriesTest(unittest.TestCase):
    def test_fetching_a_list_of_tracker_stories(self):
        stub_tracker_api = StubTrackerApi()
        stub_tracker_api.stub_get([
            {
                'external_id': '456',
                'labels': [{'name': 'github-issue'}]
            }
        ])
        
        stories = TrackerStories(stub_tracker_api).fetch_by_label(
            project_id=123,
            label='github-issue'
        )

        self.assertEqual(
            '456',
            stories[0].external_id()
        )

    def test_it_filters_out_stories_that_do_not_match_the_given_label_case_insensitive(self):
        stub_tracker_api = StubTrackerApi()
        
        stub_tracker_api.stub_get([
            {'external_id': '456', 'labels': [{'name': 'github-issue'}]},
            {'external_id': '789', 'labels': [{'name': 'github-issue'}]},
            {'external_id': '123', 'labels': [{'name': 'other-issue'}]}
        ])
        
        stories = TrackerStories(stub_tracker_api).fetch_by_label(
            project_id=123,
            label='Github-Issue'
        )

        self.assertEqual(['456', '789'], [story.external_id() for story in stories])

    def test_it_filters_out_stories_that_do_not_match_the_given_label(self):
        stub_tracker_api = StubTrackerApi()
        
        stub_tracker_api.stub_get([
            {'external_id': '456', 'labels': [{'name': 'github-issue'}]},
            {'external_id': '789', 'labels': [{'name': 'github-issue'}]},
            {'external_id': '123', 'labels': [{'name': 'other-issue'}]}
        ])
        
        stories = TrackerStories(stub_tracker_api).fetch_by_label(
            project_id=123,
            label='github-issue'
        )

        self.assertEqual(['456', '789'], [story.external_id() for story in stories])

        
    def test_it_returns_nil_for_story_without_external_id(self):
        stub_tracker_api = StubTrackerApi()
        
        stub_tracker_api.stub_get([
            {'id': 12345, 'labels': [{'name': 'github-issue'}]},
            ])
        
        stories = TrackerStories(stub_tracker_api).fetch_by_label(
            project_id=123,
            label='github-issue'
        )

        self.assertEqual([12345], [story.story_id() for story in stories])
        
        
    def test_fetching_a_list_of_tracker_stories_calls_get_on_api(self):
        stub_tracker_api = StubTrackerApi()
        tracker_stories = TrackerStories(
            tracker_api=stub_tracker_api
            )

        stories = tracker_stories.fetch_by_label(
            project_id=456,
            label='foo',
        )

        self.assertEqual('/projects/456/stories', stub_tracker_api.get_was_called_with)
        
    def test_fetching_stories_returns_the_story_url(self):
        stub_tracker_api = StubTrackerApi()
        tracker_stories = TrackerStories(
            tracker_api=stub_tracker_api
        )

        stub_tracker_api.stub_get([
            {
                'url': 'http://example.com/some-story-url',
                'labels': [{
                    'name': 'foo',
                }]
            }
        ])
        
        stories = tracker_stories.fetch_by_label(
            project_id=456,
            label='foo',
        )

        self.assertEqual(['http://example.com/some-story-url'],
                         [story.url() for story in stories])

