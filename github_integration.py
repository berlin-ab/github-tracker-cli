
import requests

DONE = 'DONE'

from github_tracker_domain import Issue

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
