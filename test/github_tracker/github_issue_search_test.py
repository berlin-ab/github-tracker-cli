import unittest


from github_tracker_cli.github_tracker.domain import (
    GithubIssuesSearch,
    )


from .test_helpers import (
    make_issue,
    StubGithubIssues,
    make_member,
    )


def get_issue_numbers(issues):
    return [issue.number() for issue in issues]


class GithubIssueSearchTest(unittest.TestCase):
    def test_it_returns_github_issues(self):
        stub_github_issues = StubGithubIssues()
        stub_github_issues.stub([
            make_issue(
                number=555,
            )
        ])
        stub_organization_members = StubOrganizationMembers()
        
        search = GithubIssuesSearch(
            github_issues=stub_github_issues,
            organization_members=stub_organization_members,
        )
        issues = [issue for issue in search.fetch()]
        self.assertEqual(555, issues[0].number())

    def test_it_excludes_issues_that_are_created_by_members_in_the_given_organization(self):
        stub_github_issues = StubGithubIssues()
        stub_github_issues.stub([
            make_issue(
                number=111,
                author_user_id='abc'
            ),
            make_issue(
                number=222,
                author_user_id='def'
            ),
            make_issue(
                number=333,
                author_user_id='ghi'
            ),
        ])

        stub_organization_members = StubOrganizationMembers()
        stub_organization_members.stub('xxx', [make_member(user_id='abc')])
        stub_organization_members.stub('zzz', [make_member(user_id='def')])
        
        search = GithubIssuesSearch(
            github_issues=stub_github_issues,
            organization_members=stub_organization_members,
        )

        self.assertEqual(
            [222, 333],
            get_issue_numbers(search.fetch(exclude_organizations=['xxx'])))

        self.assertEqual(
            [111, 333],
            get_issue_numbers(search.fetch(exclude_organizations=['zzz'])))

        self.assertEqual(
            [333],
            get_issue_numbers(search.fetch(exclude_organizations=['xxx', 'zzz'])))

        self.assertEqual(
            [111, 222, 333],
            get_issue_numbers(search.fetch(exclude_organizations=[])))
        

class StubOrganizationMembers():
    def __init__(self):
        self.stubs = {}
        
    def stub(self, organization_name, stubbed_members):
        self.stubs[organization_name] = stubbed_members

    def fetch(self, organization_label):
        return self.stubs[organization_label]
