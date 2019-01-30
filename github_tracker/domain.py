class Issue():
    def __init__(self, number, url, title, description, labels):
        self._number = number
        self._url = url
        self._title = title
        self._labels = labels
        self._description = description

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

    def labels_contain_with_insensitive_match(self, other_label):
        lower_case_labels = [label.lower() for label in self.labels()]

        return other_label.lower() in lower_case_labels

    
class Story():
    def __init__(self, story_id = None, external_id = None, title=''):
        self._story_id = story_id
        self._external_id = external_id
        self._title = title

    def external_id(self):
        return self._external_id

    def story_id(self):
        return self._story_id

    def title(self):
        return self._title

    
def formatted_issue_number(issue):
    return "#{number}".format(number=issue.number())
        
    
class MissingStories():
    
    def __init__(self, tracker_stories, github_issues):
        self._tracker_stories = tracker_stories
        self._github_issues = github_issues
    
    def issues_not_in_tracker(self,
                              project_id,
                              label,
                              github_label=None):
        tracker_titles = [
            story.title()
            for story in self._tracker_stories.fetch_by_label(
                  project_id=project_id,
                  label=label
              )
        ]
        
        def not_in_tracker(issue):
            for tracker_title in tracker_titles:
                if formatted_issue_number(issue) in tracker_title:
                    return False

            return True

        def matches_github_label(issue):
            return (
                github_label is None or
                issue.labels_contain_with_insensitive_match(github_label)
            )

        return [
            issue
              for issue
              in self._github_issues.fetch()
              if matches_github_label(issue)
              and not_in_tracker(issue)
        ]

    
class ClosedIssues():
    def __init__(self, github_issues, tracker_stories):
        self._github_issues = github_issues
        self._tracker_stories = tracker_stories
    
    def fetch(self, project_id, tracker_label):
        closed_issues = self._github_issues.fetch_closed()
        
        stories = self._tracker_stories.fetch_by_label(
            project_id=project_id,
            label=tracker_label,
        )

        def closed_issues_match(story):
            for issue in closed_issues:
                if formatted_issue_number(issue) in story.title():
                    return True

        return [story for story
                in stories
                if closed_issues_match(story)]
