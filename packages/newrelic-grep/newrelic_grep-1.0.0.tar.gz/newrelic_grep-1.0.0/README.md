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
    Default is 3 days ago.

**--until**
    End time to be queried.
    Format is as same as `--since`

**-a**
    Show attibute before log message.
    You can use this option multiple times.

Ex.
```
nrgrep -a hostname -a logtype 'Failed to write'
```

**-q**
    Query to attributes. Format is `Attribute Name:Value`.
    You can use this option multiple times.

Ex.
```
ngrep -q hostname:myhost -q service=api 'Failed to write'
```

**-v**
    Show queries to be sent.
