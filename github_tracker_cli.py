import requests

# [u'labels', u'number', u'assignee', u'repository_url',
# u'closed_at', u'id', u'title', u'pull_request',
# u'comments', u'state', u'body', u'events_url', u'labels_url',
# u'author_association', u'comments_url', u'html_url',
# u'updated_at', u'node_id', u'user', u'milestone', u'locked',
# u'url', u'created_at', u'assignees']


import requests

DONE = 'DONE'

class GithubApi():
    def get(self, path):
        results = []
        current_page = 1

        while current_page != DONE:
            base_url = "https://api.github.com"
            api_url = "%s%s?page=%s" % (base_url, path, current_page)
            api_response = requests.get(api_url)

            if api_response.status_code == 200:
                values = api_response.json()
                results.extend(values)
                current_page += 1
            
                if (len(values) == 0):
                    current_page = DONE
            else:
                current_page = DONE
                    
        return results


class Issue():
    def __init__(self, number):
        self._number = number

    def number(self):
        return self._number


def json_to_issue(json):
    return Issue(
        number = json['number']
    )


class GithubIssues():
    def __init__(self, github_api, path='/'):
        self._github_api = github_api
        self._path = path

    def fetch(self):
        list_of_json = self._github_api.get(
            self._path
        )
        
        return map(json_to_issue, list_of_json)
        
class Story():
    def __init__(self, story_id = None, external_id = None):
        self._story_id = story_id
        self._external_id = external_id

    def external_id(self):
        return self._external_id

    def story_id(self):
        return self._story_id
        pass

    
def transform_json_to_story(json):
    return Story(
        story_id=json.get('id', None),
        external_id=json.get('external_id', None)
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
