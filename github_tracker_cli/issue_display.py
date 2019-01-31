from backports import csv
import sys


def _format_issue_title(issue):
    return u'[Github Issue #%s] %s' % (issue.number(), issue.title())


def format_issue(issue):
    try:
        title = _format_issue_title(issue)
        labels = u"github-issue"

        description = u'{url}\n\n{description}'.format(
            url=issue.url(),
            description=issue.description()
        )

        return {
            u'Title': title,
            u'Labels': labels,
            u'Description': description
        }
    except Exception as error:
        print "Failed to format issue:"
        print issue.number()
        print issue.title()
        print issue.url()
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
        
        print u'{id} | {url} | {title}'.format(
            id=unicode(issue.number()),
            url=unicode(issue.url()),
            title=_format_issue_title(issue),
        )


def get_issues_display_style(arguments):
    if arguments.csv:
        return _display_issues_as_csv

    return _display_issues_as_rows
        

