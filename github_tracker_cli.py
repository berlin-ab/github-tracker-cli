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
        
