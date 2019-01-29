import requests

from github_tracker.domain import Story

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
        title=json.get('name', None)
    )
    

class TrackerStories():
    def __init__(self, tracker_api):
        self._tracker_api = tracker_api
            
    def fetch_by_label(self, project_id, label):
        stories_as_json = self._tracker_api.get('/projects/%s/stories' % project_id)
        
        def remove_not_matching_label(json):
            for label_json in json['labels']:
                if label_json['name'] == label:
                    return True
        
        return map(
                transform_json_to_story,
                filter(remove_not_matching_label, stories_as_json)
            )