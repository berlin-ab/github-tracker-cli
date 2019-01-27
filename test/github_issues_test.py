
import unittest


from github_integration import GithubIssues
from github_tracker_domain import Issue


class StubGithubApi():
    def __init__(self):
        self.stubbed_response = []
        self.used_path = None
    
    def stub_get(self, stubbed_response):
        self.stubbed_response = stubbed_response

    def get(self, path):
        self.used_path = path
        return self.stubbed_response
    

class GithubIssuesTest(unittest.TestCase):
    def test_it_can_fetch_github_issues(self):
        github_api = StubGithubApi()
        github_repo = 'some/repo'

        github_api.stub_get([
            {'number': 45678, 'html_url': 'http://example.com'}
        ])
        
        issues = GithubIssues(github_api, github_repo).fetch()
        
        self.assertEqual(issues[0].number(), 45678)
        self.assertEqual(issues[0].url(), 'http://example.com')        

    def test_it_receives_the_github_issues_api_path_when_fetching(self):
        github_api = StubGithubApi()
        
        issues = GithubIssues(
            github_api,
            'berlin-ab/some-repo'
        ).fetch()
        
        self.assertEqual(
            github_api.used_path,
            '/repos/berlin-ab/some-repo/issues'
            )
        
