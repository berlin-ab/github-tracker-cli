def printer(string):
    sys.stdout.write(string + "\n")


def display_stories_as_rows(stories):
    for story in stories:
        printer(u"{id} | {url} | {title}".format(
            id=story.story_id(),
            title=story.title(),
            url=story.url(),
        ))
        
