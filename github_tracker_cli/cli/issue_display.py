def _format_issue_title(issue):
    return u'[Github Issue #%s] %s' % (issue.number(), issue.title())


def _format_issue(issue, printer):
    try:
        title = _format_issue_title(issue)
        labels = u"github-issue"

        description = u'{url}'.format(
            url=issue.url(),
        )

        return {
            u'Title': title,
            u'Labels': labels,
            u'Description': description
        }
    except Exception as error:
        printer("Failed to format issue:")
        printer(issue.number())
        printer(issue.title())
        printer(issue.url())
        raise error


def display_issues_as_csv(issues, csv_writer, printer):
    csv_writer.write_header([u'Title', u'Labels', u'Description'])

    for issue in issues:
        csv_writer.write_row(
            _format_issue(issue, printer)
        )


def display_issues_as_rows(issues, printer):
    for issue in issues:
        printer(u'{id} | {url} | {created_at} | {updated_at} | {author} | {title} | {labels}'.format(
            id=str(issue.number()).ljust(5),
            url=issue.url().ljust(50),
            title=issue.title(),
            author=issue.author_user_id().ljust(20),
            created_at=issue.created_at(),
            updated_at=issue.updated_at(),
            labels=", ".join(issue.labels()),
        ))






