import requests

from github_tracker_cli.github_tracker.domain import (
    Story,
    TrackerStoryHistory,
    )


class MissingPivotalTrackerApiTokenError(RuntimeError):
    pass


class PivotalTrackerApi():
    def __init__(self, api_token):
        self._api_token = api_token

        if self._api_token  is None or self._api_token is '':
            raise MissingPivotalTrackerApiTokenError()
        
    def get(self, path):
        url = "https://www.pivotaltracker.com/services/v5%s" % path
        headers = {'X-TrackerToken': ('%s' % self._api_token)}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError('failed quering pivotal tracker api: %s, %s' % (response.status_code, response.json()))

        
def transform_json_to_story(json):
    return Story(
        story_id=json.get('id', None),
        external_id=json.get('external_id', None),
        title=json.get('name', None),
        url=json.get('url', None)
    )


def labels_in_lower_case(json):
    return [
        label_json['name'].lower()
          for label_json
          in json.get('labels', [])
    ]


class TrackerStories():
    def __init__(self, tracker_api):
        self._tracker_api = tracker_api
            
    def fetch_by_label(self, project_id, label):
        stories_as_json = self._tracker_api.get('/projects/%s/stories' % project_id)

        def remove_not_matching_label(json):
            for lower_label in labels_in_lower_case(json):
                if lower_label == label.lower():
                    return True
        
        return map(
                transform_json_to_story,
                filter(remove_not_matching_label, stories_as_json)
            )

    
def transform_json_to_history(json):
    cycle_time_details = json.get('cycle_time_details', {})
    started_duration = cycle_time_details.get('started_time')
    finished_duration = cycle_time_details.get('finished_time')
    delivered_duration = cycle_time_details.get('delivered_time')
    
    return TrackerStoryHistory(
        started_duration=started_duration,
        finished_duration=finished_duration,
        delivered_duration=delivered_duration,
        story=transform_json_to_story(json),
    )


class GetTrackerStoryHistory():
    def __init__(self, tracker_api):
        self._tracker_api = tracker_api
        self._states = ['finished', 'started', 'planned', 'rejected', 'unstarted']
        
    def fetch(self, project_id):
        results = []

        for state in self._states:
            results.extend([
                transform_json_to_history(json)
                for json
                in self._tracker_api.get('/projects/{project_id}/stories?with_state={state}&limit=500&fields=id,url,name,cycle_time_details'.format(
                    state=state,
                    project_id=project_id,
                ))
            ])

        return results






