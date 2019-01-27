import requests


from github_tracker_domain import Issue


class GithubApi():
    @staticmethod
    def _make_url(path, current_page):
        base_url = "https://api.github.com"
        return "%s%s?page=%s" % (base_url, path, current_page)
        
    def get(self, path):
        results = []
        current_page = 1

        while True:
            api_response = requests.get(self._make_url(path, current_page))
            
            if api_response.status_code == 200:
                values = api_response.json()
                results.extend(values)
                current_page += 1
            
                if (len(values) == 0):
                    break;
            else:
                raise RuntimeError('unable to fetch from github: %s, %s' % (api_response.status_code, api_response.text))

                    
        return results

    
def json_to_issue(json):
    return Issue(
        number = json['number'],
        url = json['html_url'],
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
