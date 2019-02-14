import unittest


from github_tracker_cli.pivotal_tracker.integration import (
    GetTrackerStoryHistory,
    )


class StubTrackerApi():
    def __init__(self):
        self.responses = []
        self._used_urls = []
        
    def stub_request(self, response):
        self.responses.append(response)

    def get(self, path):
        self._used_urls.append(path)
        if self.responses:
            return self.responses.pop()

        return []


    def used_urls(self):
        return self._used_urls
    

class TrackerStoryHistoryTest(unittest.TestCase):
    def test_it_returns_a_list_of_history(self):
        stub_tracker_api = StubTrackerApi()
        stub_tracker_api.stub_request([
            {
                'name': 'My fake title',
                'cycle_time_details': {
                    'started_time': 123,
                    'finished_time': 456,
                    'delivered_time': 789,
                }
            }
        ])
        
        history = GetTrackerStoryHistory(stub_tracker_api).fetch(
            project_id=123,
            )
        
        self.assertEqual(history[0].story().title(), 'My fake title')
        self.assertEqual(history[0].started_at(), 123)
        self.assertEqual(history[0].finished_at(), 456)
        self.assertEqual(history[0].delivered_at(), 789)

    def test_it_combines_responses(self):
        stub_tracker_api = StubTrackerApi()
        stub_tracker_api.stub_request([
            {
                'name': 'My fake title',
            }
        ])
        stub_tracker_api.stub_request([
            {
                'name': 'My other fake title',
            }
        ])

        histories = GetTrackerStoryHistory(stub_tracker_api).fetch(
            project_id=123,
            )

        self.assertIn('My fake title', [history.story().title() for history in histories])
        self.assertIn('My other fake title', [history.story().title() for history in histories])        
        

    def test_it_sends_requests_to_the_path_specified_for_the_project_id_given(self):
        stub_tracker_api = StubTrackerApi()
        history = GetTrackerStoryHistory(stub_tracker_api).fetch(
            project_id=456,
            )

        self.assertIn(
            '/projects/456/stories?with_state=finished&limit=500&fields=id,name,cycle_time_details',
            stub_tracker_api.used_urls()
        )
        
    def test_it_sends_requests_to_the_right_path(self):
        stub_tracker_api = StubTrackerApi()
        history = GetTrackerStoryHistory(stub_tracker_api).fetch(
            project_id=123,
            )

        self.assertIn(
            '/projects/123/stories?with_state=finished&limit=500&fields=id,name,cycle_time_details',
            stub_tracker_api.used_urls()
        )
        
        self.assertIn(
            '/projects/123/stories?with_state=started&limit=500&fields=id,name,cycle_time_details',
            stub_tracker_api.used_urls()
        )

        self.assertIn(
            '/projects/123/stories?with_state=planned&limit=500&fields=id,name,cycle_time_details',
            stub_tracker_api.used_urls()
        )
        
        self.assertIn(
            '/projects/123/stories?with_state=rejected&limit=500&fields=id,name,cycle_time_details',
            stub_tracker_api.used_urls()
        )

        self.assertIn(
            '/projects/123/stories?with_state=unstarted&limit=500&fields=id,name,cycle_time_details',
            stub_tracker_api.used_urls()
        )
