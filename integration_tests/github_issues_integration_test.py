import unittest

from github_tracker_cli.github.integration import (
    GithubIssues,
    GithubApi
)

    
class GithubIssuesIntegrationTest(unittest.TestCase):
    def test_it_does_not_return_pull_requests(self):
        real_github_api = GithubApi()

        issues = GithubIssues(
            real_github_api,
            'berlin-ab/github-tracker-cli'
        ).fetch()
        
        numbers = [issue.number() for issue in issues]
        titles = [issue.title() for issue in issues]        

        self.assertNotIn(18, numbers)
        self.assertNotIn('Fake pull request', titles)        
                        
    def test_it_returns_real_issues(self):
        real_github_api = GithubApi()

        issues = GithubIssues(
            real_github_api,
            'berlin-ab/gpdb'
        ).fetch()
        
        self.assertEqual(2, issues[0].number())
        self.assertIn('testing', issues[0].labels())
        self.assertIn('stub', issues[0].labels())
        
    def test_it_returns_results_for_a_different_repo(self):
        real_github_api = GithubApi()
        
        issues = GithubIssues(
            real_github_api,
            'berlin-ab/gpdb'
        ).fetch()

        numbers = [issue.number() for issue in issues]

        self.assertIn(2, numbers)
