class Issue():
    def __init__(self, number, url, title):
        self._number = number
        self._url = url
        self._title = title

    def number(self):
        return self._number

    def url(self):
        return self._url

    def title(self):
        return self._title

    
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
    
    
class App():
    
    def __init__(self, tracker_stories, github_issues):
        self._tracker_stories = tracker_stories
        self._github_issues = github_issues
    
    def issues_not_in_tracker(self, project_id, label):
        tracker_titles = [
            story.title()
            for story
            in self._tracker_stories.fetch_by_label(project_id=project_id, label=label)]
        
        def not_in_tracker(issue):
            for tracker_title in tracker_titles:
                if ("Github Issue #%s" % issue.number()) in tracker_title:
                    return False

            return True

        
        return filter(not_in_tracker, self._github_issues.fetch())
    

