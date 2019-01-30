import unittest


from github.integration import GithubIssues
from github_tracker.domain import Issue


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
            {
                'number': 45678,
                'html_url': 'http://example.com',
                'title': 'Some title',
                'body': 'Some description',
            }
        ])
        
        issues = GithubIssues(github_api, github_repo).fetch()
        
        self.assertEqual(issues[0].number(), 45678)
        self.assertEqual(issues[0].url(), 'http://example.com')
        self.assertEqual(issues[0].description(), 'Some description')

    def test_it_discards_issues_that_have_pull_requests(self):
        github_api = StubGithubApi()
        github_repo = 'some/repo'

        github_api.stub_get([
            {
                'number': 45678,
                'html_url': 'http://example.com',
                'title': 'Some title',
                'body': '',
            },
            {
                'number': 123,
                'html_url': 'http://example.com/pr',
                'title': 'Some pr',
                'body': '',
                'pull_request': {'url': 'http://example.com/some-pr-url'}
            }
        ])
        
        issues = GithubIssues(github_api, github_repo).fetch()
        self.assertEqual(1, len(issues))
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

    def test_it_populates_the_issue_with_labels(self):
        github_api = StubGithubApi()
        github_repo = 'some/repo'

        github_api.stub_get([
            {
                'number': 45678,
                'html_url': 'http://example.com',
                'title': 'Some title',
                'body': '',
                'labels': [
                    {
                        'name': 'some-label'
                    }
                ]
            }
        ])

        issues = GithubIssues(github_api, github_repo).fetch()
        self.assertEqual(1, len(issues))
        self.assertEqual(['some-label'], issues[0].labels())
        
