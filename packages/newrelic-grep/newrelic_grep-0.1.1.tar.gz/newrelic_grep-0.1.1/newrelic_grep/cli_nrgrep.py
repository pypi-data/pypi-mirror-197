#!/bin/env python3
from __future__ import annotations

import argparse
import sys
import types

from . import nrgrep


def get_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='WRITE-HOW-TO-USE-THIS-COMMAND')
    parser.add_argument("pattern", action="store")
    parser.add_argument("--since", dest="since",
                        type=str, metavar="YYYYmmddHHMMSS",
                        default=None)
    parser.add_argument("--until", dest="until",
                        type=str, metavar="YYYYmmddHHMMSS",
                        default=None)
    parser.add_argument("-v", dest="verbose",
                        action="store_true",
                        default=False,
                        help="shows hostname, logtype, query")

    args = parser.parse_args()

    return args


def main() -> int:
    args = get_opt()
    nrgrep.query(args.pattern, args.since, args.until, args.verbose)

    return 0


if __name__ == "__main__":
    sys.exit(main())
