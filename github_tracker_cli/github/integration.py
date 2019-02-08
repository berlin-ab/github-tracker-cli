import requests


from dateutil import parser


from github_tracker_cli.github_tracker.domain import (
    Issue,
    PullRequest
)


def default_logger(message):
    pass


def default_printer(message):
    pass


class GithubApi():
    def __init__(self, logger=default_logger, printer=default_printer, credentials=()):
        self.log = logger
        self.printer = printer
        self._credentials = credentials
        
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
            self.log("current page: %s" % current_page)
            url = self._make_url(path, current_page)
            self.log("url: %s" % url)
            api_response = requests.get(url, auth=self._credentials)
            
            if api_response.status_code == 200:
                self.log("api response status code: %s" % 200)
                self.log("data: %s" % api_response.json())
                values = api_response.json()
                results.extend(values)
                current_page += 1
            
                if (len(values) == 0):
                    break;
            elif api_response.status_code == 403:
                self.printer("Unable to authenticate with Github: %s" % api_response.text)
                break
            else:
                raise RuntimeError('unable to fetch from github: %s, %s' % (api_response.status_code, api_response.text))

                    
        return results

    
def parse_date(date_string):
    if date_string:
        return parser.parse(date_string)

    
def parse_labels(json):
    return [
        label_json['name']
        for label_json in json.get('labels', [])
    ]
    
    
def json_to_issue(json):
    labels = parse_labels(json)

    return Issue(
        number=json['number'],
        url=json['html_url'],
        title=json['title'],
        description=json['body'],
        labels=labels,
        created_at=parse_date(json.get('created_at')),
        updated_at=parse_date(json.get('updated_at')),
    )


def json_to_pull_request(json):
    updated_at_string = json.get('updated_at')
    updated_at = parse_date(updated_at_string)
    labels = parse_labels(json)

    return PullRequest(
        number=json['number'],
        url=json.get('pull_request', {}).get('html_url'),
        title=json['title'],
        last_updated_at=updated_at,
        author=json.get('user', {}).get('login'),
        labels=labels,
    )


def non_pull_requests(json):
    return not only_pull_requests(json)


def only_pull_requests(json):
    return 'pull_request' in json


class GithubIssues():
    def __init__(self, github_api, github_repo):
        self._github_api = github_api
        self._path = "/repos/%s/issues" % github_repo

    def fetch(self):
        return self._fetch(state='open')
        
    def _fetch(self, state):
        list_of_json = self._github_api.get(
            self._path + '?state={state}'.format(state=state)
        )
        
        return map(json_to_issue,
                   filter(non_pull_requests, list_of_json))

    
class PullRequests():
    def __init__(self, github_api, github_repo):
        self._github_api = github_api
        self._path = "/repos/%s/issues" % github_repo

    def fetch(self):
        return self._fetch(state='open')
        
    def _fetch(self, state):
        list_of_json = self._github_api.get(
            self._path + '?state={state}'.format(state=state)
        )
        
        return map(json_to_pull_request,
                   filter(only_pull_requests, list_of_json))
    
