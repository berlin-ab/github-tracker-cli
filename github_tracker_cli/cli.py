import os
import sys
import codecs


from github_tracker_cli.argument_parsers import parse_arguments
from github_tracker_cli.runners import discover_subcommand
from github_tracker_cli.components import Components


def main():
    # Ensure that writing to standard out and to a pipe is via utf8
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    arguments = parse_arguments()
    components = Components(arguments)
    subcommand = discover_subcommand(arguments)
    subcommand(components)

