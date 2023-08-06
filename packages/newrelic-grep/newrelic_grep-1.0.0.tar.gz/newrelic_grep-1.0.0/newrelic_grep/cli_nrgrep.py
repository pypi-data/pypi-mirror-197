#!/bin/env python3
from __future__ import annotations

import argparse
import sys

from . import nrgrep


def get_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='grep command for New Relic. Please set env vals, `NR_API_KEY` and `NR_ACCOUNT_ID`.')
    parser.add_argument("pattern", action="store")
    parser.add_argument("--since", dest="since",
                        type=str, metavar="YYYYmmddHHMMSS",
                        default=None)
    parser.add_argument("--until", dest="until",
                        type=str, metavar="YYYYmmddHHMMSS",
                        default=None)
    parser.add_argument("-a", dest="attributes",
                        action="append",
                        type=str, metavar="ATTRIBUTE_NAME",
                        default=[],
                        help="Attribute to show, you can use this multiple times")
    parser.add_argument("-q", dest="conds",
                        action="append",
                        type=str, metavar="ATTRIBUTE_NAME:VALUE",
                        default=[],
                        help="Attribute to show, you can use this multiple times")
    parser.add_argument("-e", dest="regex",
                        action="store_true",
                        default=False,
                        help="Use regular expression to pattern.")
    parser.add_argument("-l", dest="limit",
                        action="store",
                        type=int, metavar="LIMIT",
                        default=0,
                        help="Attribute to show, you can use this multiple times")
    parser.add_argument("-v", dest="verbose",
                        action="store_true",
                        default=False,
                        help="shows hostname, logtype, query")

    args = parser.parse_args()

    return args


def main() -> int:
    args = get_opt()
    nrgrep.query(
        pattern=args.pattern,
        since=args.since,
        until=args.until,
        verbose=args.verbose,
        attributes=args.attributes,
        conditions=args.conds,
        regex=args.regex,
        limit=args.limit
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
