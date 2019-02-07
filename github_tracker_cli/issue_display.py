from __future__ import print_function


from backports import csv
import sys


def _format_issue_title(issue):
    return u'[Github Issue #%s] %s' % (issue.number(), issue.title())


def printer(string):
    print(string)


def format_issue(issue):
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


def _display_issues_as_csv(issues):
    writer = csv.DictWriter(
        sys.stdout,
        [u'Title', u'Labels', u'Description'],
        quoting=csv.QUOTE_ALL
    )

    writer.writeheader()
    writer.writerows(map(format_issue,  issues))


def _display_issues_as_rows(issues):
    for issue in issues:
        formatted_issue = format_issue(issue)
        
        printer(u'{id} | {url} | {created_at} | {updated_at} | {title}'.format(
            id=str(issue.number()).ljust(5),
            url=issue.url(),
            title=_format_issue_title(issue),
            created_at=issue.created_at(),
            updated_at=issue.updated_at(),
        ))


def get_issues_display_style(arguments):
    if arguments.csv:
        return _display_issues_as_csv

    return _display_issues_as_rows
        

