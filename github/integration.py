import requests


from github_tracker.domain import Issue


class GithubApi():
    @staticmethod
    def _make_url(path, current_page):
        base_url = "https://api.github.com"
        per_page = 100

        return "{base_url}{path}&page={page}&per_page={per_page}".format(
            base_url=base_url,
            path=path,
            page=current_page,
            per_page=per_page,
        )
        
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
            elif api_response.status_code == 403:
                print "Unable to authenticate with Github: %s" % api_response.text
                break
            else:
                raise RuntimeError('unable to fetch from github: %s, %s' % (api_response.status_code, api_response.text))

                    
        return results

    
def json_to_issue(json):
    labels = [
        label_json['name']
        for label_json in json.get('labels', [])
    ]

    return Issue(
        number = json['number'],
        url = json['html_url'],
        title = json['title'],
        description = json['body'],
        labels = labels,
    )

def non_pull_requests(json):
    if 'pull_request' in json:
        return False

    return True


class GithubIssues():
    def __init__(self, github_api, github_repo):
        self._github_api = github_api
        self._path = "/repos/%s/issues" % github_repo

    def fetch(self):
        return self._fetch(state='open')
        
    def fetch_closed(self):
        return self._fetch(state='closed')

    def _fetch(self, state):
        list_of_json = self._github_api.get(
            self._path + '?state={state}'.format(state=state)
        )
        
        return map(json_to_issue,
                   filter(non_pull_requests, list_of_json))
        
