# sqltrack.__main__
import argparse

from . import Client
from .commands import setup


def main():
    parser = argparse.ArgumentParser(prog="sqltrack")
    parser.add_argument("-u", "--user", help="username")
    parser.add_argument("-a", "--host", help="DB host (and port)")
    parser.add_argument("-d", "--database", help="database name")
    parser.add_argument("-s", "--schema", help="schema name")
    parser.add_argument("-c", "--config-path", help="path to config file")
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands.",
        required=True,
    )
    parser_setup = subparsers.add_parser(
        "setup",
        help="Setup (and update) the database."
    )
    parser_setup.add_argument(
        "path",
        nargs="*",
        metavar="PATH",
        help="Optional SQL scripts, executed in the given order.",
    )
    args = parser.parse_args()

    if args.command == "setup":
        client = Client(
            config_path=args.config_path,
            user=args.user,
            host=args.host,
            dbname=args.database,
            schema=args.schema,
        )
        setup(client, args.path)


main()
