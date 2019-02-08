

def formatted_issue_number(issue):
    return "#{number}".format(number=issue.number())


def sort_by_last_updated_at(pull_request):
    return pull_request.last_updated_at()


class PullRequest():
    def __init__(self, number, url, title, last_updated_at, author):
        self._number = number
        self._url = url
        self._title = title
        self._last_updated_at = last_updated_at
        self._author = author

    def number(self):
        return self._number

    def url(self):
        return self._url

    def title(self):
        return self._title

    def last_updated_at(self):
        return self._last_updated_at

    def author(self):
        return self._author


class Issue():
    def __init__(self, number, url, title, description, labels, created_at, updated_at):
        self._number = number
        self._url = url
        self._title = title
        self._labels = labels
        self._description = description
        self._created_at = created_at
        self._updated_at = updated_at

    def number(self):
        return self._number

    def url(self):
        return self._url

    def title(self):
        return self._title

    def labels(self):
        return self._labels

    def description(self):
        return self._description

    def created_at(self):
        return self._created_at

    def updated_at(self):
        return self._updated_at

    def labels_contain_with_insensitive_match(self, other_label):
        lower_case_labels = [label.lower() for label in self.labels()]

        return other_label.lower() in lower_case_labels

    
class Story():
    def __init__(self, story_id = None, external_id = None, title='', url=''):
        self._story_id = story_id
        self._external_id = external_id
        self._title = title
        self._url = url

    def external_id(self):
        return self._external_id

    def story_id(self):
        return self._story_id

    def title(self):
        return self._title

    def url(self):
        return self._url

    
class MissingStories():
    
    def __init__(self, tracker_stories, github_issues):
        self._tracker_stories = tracker_stories
        self._github_issues = github_issues


    def issues_not_in_tracker(self,
                              project_id,
                              label,
                              github_label=None,
                              exclude_github_label=None,
    ):
        tracker_titles = self._tracker_titles(project_id, label)
        
        return [
            issue
              for issue
              in self._github_issues.fetch()
              if self._matches_github_label(github_label, issue)
              and not self._matches_excluded_github_label(exclude_github_label, issue)
              and self._not_in_tracker(issue, tracker_titles)
        ]
    
    def _not_in_tracker(self, issue, tracker_titles):
        for tracker_title in tracker_titles:
            if formatted_issue_number(issue) in tracker_title:
                return False
            
        return True

    def _tracker_titles(self, project_id, label):
        return [
            story.title()
            for story in self._tracker_stories.fetch_by_label(
                  project_id=project_id,
                 label=label
              )
        ]
        
    def _matches_excluded_github_label(self, exclude_github_label, issue):
        return (
            exclude_github_label and
              issue.labels_contain_with_insensitive_match(exclude_github_label)
        )

    def _matches_github_label(self, github_label, issue):
        return (
            github_label is None or
              issue.labels_contain_with_insensitive_match(github_label)
        )


    
class ClosedIssues():
    def __init__(self, github_issues, tracker_stories):
        self._github_issues = github_issues
        self._tracker_stories = tracker_stories
    
    def fetch(self, project_id, tracker_label):
        open_issues = self._github_issues.fetch()
        
        stories = self._tracker_stories.fetch_by_label(
            project_id=project_id,
            label=tracker_label,
        )

        def open_issues_match(story):
            for issue in open_issues:
                if formatted_issue_number(issue) in story.title():
                    return False

            return True

        return [story for story
                in stories
                if open_issues_match(story)]


class OpenPullRequests():
    def __init__(self, pull_requests):
        self._pull_requests = pull_requests

    def fetch(self):
        return sorted(
            self._pull_requests.fetch(),
            key=sort_by_last_updated_at,
            reverse=True
            )

