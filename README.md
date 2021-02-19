### Geocoding CLI

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

# Installation
## Using Pip
```bash
  $ pip install geocli
```
## Manual
```bash
  $ git clone https://github.com/expandaventures/geocoding-cli
  $ cd geocoding-cli
  $ python setup.py install
```
# Usage
```bash
$ geocli
```
## Geocode a single address
`Usage: geocli geocode [OPTIONS] ADDRESS [STATE] [CITY]`
```bash
$ geocli geocode --dry_run 'Av. Reforma 222' cdmx mexico
```
## Batch: geocode a addresses in a file

`Usage: geocli batch [OPTIONS] INPUT_FILE OUTPUT_PATH`
```bash
$ geocli batch --dry_run sample.csv out.csv
```

The expected schema in the file is:

```
id, state, unused, city, ... , address
1, CDMX,,Mexico,,Av. Reforma 222

```

The **ONLY** columns used are 2nd, 4th and last. 
(e.g. row[1], row[3], row[-1])

