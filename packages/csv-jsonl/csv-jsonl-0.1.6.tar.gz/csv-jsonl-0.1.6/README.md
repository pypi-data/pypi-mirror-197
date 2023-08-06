# csv-jsonl

A convenient module for writing a list of dictionaries or list of lists to a [`.jsonl`-formatted](https://jsonlines.org/) text file, suitable for ingestion by [BigQuery](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json) and other services.

`csv-jsonl` is built on top of Python's built-in `csv` module. It allows you to specify a `fieldnames` list to add a bit of assurance. Otherwise, no schema-handling is offered.

# Why not Just Use csv Files?

If you are here asking that question, I'm guessing you have not spent exciting times attempting to clean up poorly-formatted `csv` files (I'm looking at you, Excel).

# Other Data Formats

Basically supports anything with a `__getitem__`, as well as dataclasses. See `test` for everything.


# Installation

`pip install csv-jsonl`

# Usage

## List of Dictonaries

```python
>>> from csv_jsonl import JSONLinesDictWriter
>>> l = [{"foo": "bar", "bat": 1}, {"foo": "bar", "bat": 2}]
>>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh)
...     writer.writerows(l)
...
>>> d = {"foo": "bar", "bat": 1}
>>> with open("bar.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh)
...     writer.writerow(d)
...
>>> from collections import OrderedDict
>>> od = OrderedDict([('foo', 'bar'), ('bat', 1)])
>>> with open("qux.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh)
...     writer.writerow(od)
...
>>> fieldnames = ["foo", "bar"] # keys = ["foo", "bat"] expect fail
>>> with open("baz.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh, fieldnames=fieldnames)
...     writer.writerows(l)
...
Expect ValueError
```

## List of Lists

```python
        >>> from csv_jsonl import JSONLineslistWriter
        >>> l = zip(["foo", "bar", "bat"], range(3), range(3))
        >>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesListWriter(_fh)
        ...     writer.writerows(l)
        ...
        >>> l = zip(["foo", "bar", "bat"], range(3), range(3))
        >>> with open("bar.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesDictWriter(_fh)
        ...     writer.writerow(next(l))
        ...
        >>> fieldnames = ["baz", "qux", "quux"]
        >>> l = zip(["foo", "bar", "bat"], range(3), range(3))
        >>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesListWriter(_fh, fieldnames=fieldnames)
        ...     writer.writeheader()
        ...     writer.writerows(l)
        ...
```

[![pipeline status](https://gitlab.com/doug.shawhan/csv-jsonl/badges/main/pipeline.svg)](https://gitlab.com/doug.shawhan/csv-jsonl/-/commits/main)
[![Latest Release](https://gitlab.com/doug.shawhan/csv-jsonl/-/badges/release.svg)](https://gitlab.com/doug.shawhan/csv-jsonl/-/releases)
[![Downloads](https://pepy.tech/badge/csv-jsonl/month)](https://pepy.tech/project/csv-jsonl)
