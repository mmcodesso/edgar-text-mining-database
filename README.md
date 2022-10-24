# Edgar Texting Mining Database

This repo contains python code to download form10k filings  from [EDGAR database](https://www.sec.gov/edgar.shtml), 
and then extract the MDA section from the downloaded form10k filings heuristically


### Installation

I used python3.6
```bash
#python36
pip install -r requirements.txt
```


### Quick Start

Specify the starting year and end year and the directory to save outputs.
By default, indices, forms and mdas will be saved to `./data`

```bash
# Downloads and parses MDA section from 2021 to 2021 quarter 1 and 2, and saves to `./database/database.sqlite`
# It will use SQLite database. You can pass postgres database connection
python edgar.py --start_year 2021 --end_year 2021
```

### Usage
```bash
usage: edgar.py [-h] -s START_YEAR -e END_YEAR [-q QUARTERS [QUARTERS ...]]
                [--overwrite] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  -s START_YEAR, --start_year START_YEAR
                        year to start
  -e END_YEAR, --end_year END_YEAR
                        year to end
  -q QUARTERS [QUARTERS ...], --quarters QUARTERS [QUARTERS ...]
                        quarters to download for start to end years
  --overwrite           If True, overwrites downloads and processed files.
  --debug               Debug mode
  -u USER,              database username
  -p PASSWORD,          database password
  -server SERVERNAME,    database address
  -db DBNAME,           database

```

### Workflow

The code runs the extraction in the following steps
1. Download indices for form 10k
2. COMMING SOON

### Notes

- MDA section is parsed heuristically, and may not work for all forms. You'll probably need to modify the `find_mda_from_text` function for coverage.
- You also might need to modify `normalize_text` function for MDA parsing.