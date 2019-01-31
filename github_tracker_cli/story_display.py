
def display_stories_as_rows(stories):
    for story in stories:
        print u"{id} | {url} | {title}".format(
            id=story.story_id(),
            title=story.title(),
            url=story.url(),
        )

        
