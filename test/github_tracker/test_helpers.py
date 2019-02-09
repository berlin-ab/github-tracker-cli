import datetime
import time


from github_tracker_cli.github_tracker.domain import (
    Issue,
    Story,
    PullRequest,
)


def parse_date(date_string):
    return time.strptime(date_string, "%Y-%m-%d")


def make_pull_request(
                number=123,
                url='http://example.com/some-pull-request-url',
                title='Some title',
                last_updated_at=parse_date('2010-01-01'),
                author_user_id='some-github-username',
                labels=[],
            ):
    return PullRequest(
        number=number,
        url=url,
        title=title,
        last_updated_at=last_updated_at,
        author_user_id=author_user_id,
        labels=labels,
    )


def make_story(title='', story_id=1):
    return Story(
        story_id=story_id,
        title=title,
        external_id=None
    )


def make_issue(number=000,
               url='',
               title='',
               labels=[],
               description='',
               author_user_id='',
):
    return Issue(
        number=number,
        url=url,
        title=title,
        labels=labels,
        description=description,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        author_user_id=author_user_id,
    )
    pass


def valid_issue(
        number=123,
        url='http://example.com/foo',
        title="A title",
        description='Some description',
        labels=[],
        author_user_id='some-user-id',
):
    return Issue(
        number=number,
        url=url,
        title=title,
        description=description,
        labels=labels,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        author_user_id=author_user_id,
    )


class StubGithubIssues():
    def __init__(self):
        self._stubbed_issues = []

    def stub(self, stubbed_issues):
        self._stubbed_issues = stubbed_issues

    def fetch(self):
        return self._stubbed_issues
    

class StubTrackerStories():
    def __init__(self):
        self._stubbed_stories = []
        self.used_label = None
        self.used_project_id = None
        
    def fetch_by_label(self, project_id, label):
        self.used_label = label
        self.used_project_id = project_id
        return self._stubbed_stories
            
    def stub(self, stubbed_stories):
        self._stubbed_stories = stubbed_stories


class StubPullRequests():
    def __init__(self):
        self._stubbed_pull_requests = []
        
    def stub(self, pull_requests):
        self._stubbed_pull_requests = pull_requests
        
    def fetch(self):
        return self._stubbed_pull_requests
        

