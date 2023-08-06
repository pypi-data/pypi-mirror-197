from __future__ import annotations
from typing import Optional
import sys
import os
import json
import datetime
import requests

URL = "https://api.newrelic.com/graphql"
API_KEY = os.environ["NR_API_KEY"]
ACCOUNT_ID = os.environ["NR_ACCOUNT_ID"]


def query(pattern: str, since: Optional[str], until: Optional[str], verbose: bool = False) -> None:
    if not since:
        _since = "3 DAYS AGO"
    else:
        since += "20000101000000"[len(since):]
        _since = datetime.datetime.strptime(since, "%Y%m%d%H%M%S").strftime("'%Y-%m-%d %H:%M:%S +0900'")

    headers = {
        "Content-Type": "application/json",
        "API-Key": API_KEY,
    }

    query = f"SELECT * FROM Log WHERE message LIKE '%{pattern}%' LIMIT MAX SINCE {_since}"
    if until:
        until += "20000101000000"[len(until):]
        _until = datetime.datetime.strptime(until, "%Y%m%d%H%M%S").strftime("'%Y-%m-%d %H:%M:%S +0900'")
        query += f" UNTIL {_until}"

    print(query)

    params = {
        "query": """
            {
              actor {
                account(id: %s) {
                  nrql(query: "%s", timeout: 120) {
                    results
                  }
                }
              }
            }
        """ % (ACCOUNT_ID, query)
    }

    if verbose:
        print(params["query"])

    r = requests.post(URL, json.dumps(params), headers=headers)

    res = r.json()

    if not res["data"]["actor"]["account"]["nrql"]:
        sys.stderr.write("\n".join([_["message"] for _ in res["errors"]]))
        sys.exit(2)

    for log in res["data"]["actor"]["account"]["nrql"]["results"][::-1]:
        if verbose:
            print(log["hostname"], log["logtype"], log["message"])
        else:
            print(log["message"])
