
import unittest


from github_tracker_cli import GithubIssues


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

        github_api.stub_get([
            {'number': 45678}
        ])
        
        issues = GithubIssues(github_api).fetch()
        
        self.assertEqual(issues[0].number(), 45678)

    def test_it_receives_the_github_issues_api_path_when_fetching(self):
        github_api = StubGithubApi()
        
        issues = GithubIssues(
            github_api,
            '/github-issues-path'
        ).fetch()
        
        self.assertEqual(
            github_api.used_path,
            '/github-issues-path'
            )
