import unittest

from github_tracker_cli.github.integration import (
    GithubIssues,
    GithubApi,
    PullRequests
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

        issues = [issue for issue in GithubIssues(
            real_github_api,
            'berlin-ab/gpdb'
        ).fetch()]
        
        self.assertEqual(2, issues[0].number())
        self.assertIn('testing', issues[0].labels())
        self.assertIn('stub', issues[0].labels())
        self.assertIsNotNone(issues[0].created_at())
        self.assertIsNotNone(issues[0].updated_at())
        self.assertEqual('berlin-ab', issues[0].author_user_id())
        
    def test_it_returns_results_for_a_different_repo(self):
        real_github_api = GithubApi()
        
        issues = GithubIssues(
            real_github_api,
            'berlin-ab/gpdb'
        ).fetch()

        numbers = [issue.number() for issue in issues]

        self.assertIn(2, numbers)

        
class PullRequestsTest(unittest.TestCase):
    def test_it_returns_pull_requests(self):
        github_repo = 'berlin-ab/github-tracker-cli'
        github_api = GithubApi()
        pull_requests_service = PullRequests(
            github_api=github_api,
            github_repo=github_repo,
        )


        pull_requests = [
            pull_request for pull_request
            in pull_requests_service.fetch()
        ]
        
        self.assertEqual(1, len(pull_requests))
        pull_request = pull_requests[0]
        self.assertEqual(18, pull_request.number())
        self.assertEqual('https://github.com/berlin-ab/github-tracker-cli/pull/18', pull_request.url())
        self.assertEqual('Fake pull request', pull_request.title())
        self.assertEqual('berlin-ab', pull_request.author_user_id())
        self.assertIsNotNone(pull_request.last_updated_at())
        self.assertIn('some-example-label', pull_request.labels())








