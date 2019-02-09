def _print_pull_request_row(pull_request, printer):
    printer(u"{number} | {url} | {last_updated_at} | {author} | {title}".format(
        number=pull_request.number(),
        url=pull_request.url(),
        title=pull_request.title(),
        last_updated_at=pull_request.last_updated_at(),
        author=pull_request.author_user_id().ljust(20),
    ))


def print_pull_requests_as_rows(pull_requests, printer):
    for pull_request in pull_requests:
        _print_pull_request_row(pull_request, printer)
