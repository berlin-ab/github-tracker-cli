import unittest


from github_tracker_cli.cli.components import (
    Components
)


from github_tracker_cli.github.integration import (
    GithubApi,
    OrganizationMembers
)


class OrganizationMembersTest(unittest.TestCase):
    def test_greenplumdb_contains_me(self):
        organization_label = 'greenplum-db'
        components = Components({})

        organization_members_service = OrganizationMembers(
            github_api=components.github_api(),
        )

        members = organization_members_service.fetch(
            organization_label=organization_label
        )

        self.assertGreater(len(members), 100)
        self.assertIn('berlin-ab', [member.user_id() for member in members])
        
