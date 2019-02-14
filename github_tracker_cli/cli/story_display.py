import time


def display_stories_as_rows(stories, printer):
    for story in stories:
        printer(u"{id} | {url} | {title}".format(
            id=story.story_id(),
            title=story.title(),
            url=story.url(),
        ))


def display_history_as_rows(story_histories, printer):
    for story_history in story_histories:
        started_duration_in_days = "%d days" % story_history.started_duration_in_days()
        story = story_history.story()
        
        printer(
            u"{story_id} | {started_duration} | {url} | {title}".format(
                story_id=(u'%d' % story.story_id()).ljust(10),
                title=story.title(),
                url=story.url(),
                started_duration=started_duration_in_days.ljust(8),
            )
        )
    
