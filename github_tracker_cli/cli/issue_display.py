from backports import csv
import sys


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


def _display_issues_as_csv(issues, printer):
    try:
        writer = csv.DictWriter(
            sys.stdout,
            [u'Title', u'Labels', u'Description'],
            quoting=csv.QUOTE_ALL
        )

        writer.writeheader()

        while issues:
            writer.writerow(_format_issue(issues.pop(), printer))
    except UnicodeEncodeError:
        import codecs
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        _display_issues_as_csv(issues, printer)

        


def display_issues_as_rows(issues, printer):
    for issue in issues:
        printer(u'{id} | {url} | {created_at} | {updated_at} | {title} | {labels}'.format(
            id=str(issue.number()).ljust(5),
            url=issue.url().ljust(50),
            title=issue.title(),
            created_at=issue.created_at(),
            updated_at=issue.updated_at(),
            labels=", ".join(issue.labels()),
        ))


def get_issues_display_style(csv):
    if csv:
        return _display_issues_as_csv

    return display_issues_as_rows
        

