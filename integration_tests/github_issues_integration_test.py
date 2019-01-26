import unittest

from github_tracker_cli import (
    GithubIssues,
    GithubApi
)

    
class GithubIssuesIntegrationTest(unittest.TestCase):
    def test_it_returns_real_issues(self):
        real_github_api = GithubApi()
        

        issues = GithubIssues(
            real_github_api,
            '/repos/greenplum-db/gpdb/issues'
        ).fetch()
        
        numbers = [issue.number() for issue in issues]

        self.assertIn(6796, numbers)
        

    def test_it_returns_results_for_a_different_repo(self):
        real_github_api = GithubApi()
        
        issues = GithubIssues(
            real_github_api,
            '/repos/berlin-ab/gpdb/issues'
        ).fetch()

        numbers = [issue.number() for issue in issues]

        self.assertIn(2, numbers)

