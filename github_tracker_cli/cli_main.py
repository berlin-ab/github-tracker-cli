from github_tracker_cli.cli.argument_parsers import parse_arguments
from github_tracker_cli.cli.runners import discover_subcommand
from github_tracker_cli.cli.components import Components


def main():
    arguments = parse_arguments()
    components = Components(arguments)
    subcommand = discover_subcommand(arguments)
    subcommand(components)

