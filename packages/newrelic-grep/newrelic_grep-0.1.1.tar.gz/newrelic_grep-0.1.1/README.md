## grep command for New Relic Logs

This package provides a command `nrgrep` which is grep-like command for New Relic Logs.

New Relic can store plenty of logs and we can query it really fast on the very nice UI on the web site, but some of developers still prefer to use command line interface to query logs than modern UIs.
This command helps such kind of people.

## Install

```
pip install newrelic-grep
```

## Prereqiusits

Set environment variables to access New Relic API:

**NR_API_KEY**
    USER API key

**NR_ACCOUNT_ID**
    Account ID of New Relic User

## Usage

```
# nrgrep [--since DATETIME] [--until DATETIME] <KeyWord to search>
```

**Exapmple**

```
nrgrep --since 20230301140000 --until 20230301150000 'Failed to write'
```

### Options

**--since**
    Start time to be queried.
    Format is `YYYYmmddHHMMSS`.
    You can omit right part if you want.
    `2023030114` will be `20230301140000`

**--until**
    End time to be queried.
    Format is as same as `--since`

**-v**
    Show queries to be sent.
