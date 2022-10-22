import edgar as e

import os
import itertools
import re
import concurrent.futures
import pandas as pd
from typing import Dict
from glob import glob
from bs4 import BeautifulSoup


def print_metrics(metrics: Dict):

    table = {
        'Total files parsed': [metrics["total_files"], ""],
        'Files skipped': [metrics["skipped_counter"], ""]
    }

    if metrics["total_files"] != 0:
        table['MDA successfully parsed'] = [metrics["passed_counter"],
                                            f"({round((metrics['passed_counter']/metrics['total_files'])  * 100, 2)}%)"]
        table['MDA parsing failures'] =  [metrics["failed_counter"] ,
                                          f"({round((metrics['failed_counter'] /metrics['total_files'])  * 100, 2)}%)"]

    else:
        table['MDA successfully parsed'] = [0, f"0.00%"]
        table['MDA parsing failures'] = [0, f"0.00%"]

    print("=" * 40)
    for metric, value in table.items():
        print(f'{metric:14} : {value[0]} {value[1]}')
    print("=" * 40)

@e.timeit
def download_forms(index_dir: str, form_dir: str, count_of_files: int, overwrite: bool = False, debug: bool = False):
    """ Reads indices and download forms
    Args:
        index_dir (str)
        form_dir (str)
    """
    # Create output directory
    os.makedirs(form_dir, exist_ok=True)

    # Prepare arguments
    combined_csv = os.path.join(index_dir, "combined.csv")
    print(f"Combining index files to {combined_csv}.")
    urls = e.read_url_from_combined_csv(combined_csv)

    download_paths = []
    for url in urls:
        download_name = "_".join(url.split('/')[-2:])
        download_path = os.path.join(form_dir, download_name)
        download_paths.append(download_path)

    print("here", count_of_files)
    # Debug
    if debug:
        print("Debug Mode invoked. Only 10 forms at the max will be downloaded.")
        download_paths = download_paths[:10]

    # limiting the number of files to 100 or value passed through args
    if count_of_files != 0:
        download_paths = download_paths[:count_of_files]

    # Download forms
    nforms = len(download_paths)
    for idx, (url, download_path) in enumerate(zip(urls, download_paths), 1):
        print(f"Downloading form {idx} / {nforms} ...")
        e.download_file(url, download_path, overwrite)


@e.timeit
def parse_html_multiprocess(form_dir, parsed_form_dir, overwrite=False):
    """ parse html with multiprocess
    Args:
        form_dir (str)

    Returns:
        parsed_form_dir (str)
    """
    # Create directory
    os.makedirs(parsed_form_dir, exist_ok=True)

    # Prepare argument
    form_paths = sorted(glob(os.path.join(form_dir, "*.txt")))
    parsed_form_paths = []
    for form_path in form_paths:
        form_name = os.path.basename(form_path)
        parsed_form_path = os.path.join(parsed_form_dir, form_name)
        parsed_form_paths.append(parsed_form_path)

    # Multiprocess
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for form_path, parsed_form_path in zip(form_paths, parsed_form_paths):
            executor.submit(parse_html, form_path, parsed_form_path, overwrite)


def parse_html(input_file, output_file, overwrite=False):
    """ Parses text from html with BeautifulSoup
    Args:
        input_file (str)
        output_file (str)
    """
    if not overwrite and os.path.exists(output_file):
        print(f"{output_file} already exists. HTML parsing will not be carried out!")
        return

    print(f"Parsing HTML from {input_file}")
    with open(input_file, 'r') as fin:
        content = fin.read()

    content = content[content.find("<DOCUMENT>"):content.find("</DOCUMENT>") + 12]

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(content, "html5lib")
    text = soup.get_text("\n")


    e.write_content(text, output_file)

    # Log message
    print(f"Data written to {output_file}")


@e.timeit
def parse_mda_multiprocess(form_dir: str, mda_dir: str, overwrite: bool = False):
    """ Parse MDA section from forms with multiprocess
    Args:
        form_dir (str)
        mda_dir (str)
    """
    # Create output directory
    os.makedirs(mda_dir, exist_ok=True)

    # Prepare arguments
    form_paths = sorted(glob(os.path.join(form_dir, "*")))
    mda_paths = []
    for form_path in form_paths:
        form_name = os.path.basename(form_path)
        root, _ = os.path.splitext(form_name)
        mda_path = os.path.join(mda_dir, '{}.mda'.format(root))
        mda_paths.append(mda_path)

    metrics = {
        "total_files": 0,
        "passed_counter": 0,
        "failed_counter": 0,
        "skipped_counter": 0
    }

    # Multiprocess
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        paths = [each for each in zip(form_paths, mda_paths, [overwrite] * len(form_paths))]
        results = executor.map(parse_mda, paths)

    for result in results:
        if result:
            metrics["total_files"] += 1
            if result == 1:
                metrics["passed_counter"] += 1
            elif result == -1:
                metrics["failed_counter"] += 1
        else:
            metrics["skipped_counter"] += 1

    return metrics


def parse_mda(args):
    """ Reads form and parses mda
    Args:
        form_path (str)
        mda_path (str)
    """
    form_path, mda_path, overwrite = args
    if not overwrite and os.path.exists(mda_path):
        print(f"{mda_path} already exists. MDA parsing skipped for this file.")
        return 0
    # Read
    print(f"Parsing MDA for {form_path}")
    with open(form_path, "r") as fin:
        text = fin.read()

    # Normalize text here
    text = e.normalize_text(text)

    # Parse MDA
    mda, end = find_mda_from_text(text)
    # Parse second time if first parse results in index
    if mda and len(mda.encode('utf-8')) < 1000:

        mda, _ = find_mda_from_text(text, start=end)

    if mda:
        print(f"Writing MDA to {mda_path}")
        e.write_content(mda, mda_path)
        return 1
    else:
        print(f"MDA parsing failed {form_path}")
        return -1


def find_mda_from_text(text, start=0):
    """Find MDA section from normalized text
    Args:
        text (str)s
    """
    debug = False

    mda = ""
    end = 0

    # Define start & end signal for parsing
    item7_begins = [
        '\nITEM 7.', '\nITEM 7 –', '\nITEM 7:', '\nITEM 7 ', '\nITEM 7\n'
    ]
    item7_ends = ['\nITEM 7A']
    if start != 0:
        item7_ends.append('\nITEM 7')  # Case: ITEM 7A does not exist
    item8_begins = ['\nITEM 8']
    """
    Parsing code section
    """
    text = text[start:]

    # Get begin
    for item7 in item7_begins:
        begin = text.find(item7)
        if debug:
            print(item7, begin)
        if begin != -1:
            break

    if begin != -1:  # Begin found
        for item7A in item7_ends:
            end = text.find(item7A, begin + 1)
            if debug:
                print(item7A, end)
            if end != -1:
                break

        if end == -1:  # ITEM 7A does not exist
            for item8 in item8_begins:
                end = text.find(item8, begin + 1)
                if debug:
                    print(item8, end)
                if end != -1:
                    break

        # Get MDA
        if end > begin:
            mda = text[begin:end].strip()
        else:
            end = 0

    return mda, end


def main():
    parser = e.create_parser()
    parser.add_argument('-c',
                        '--count_of_files',
                        type=int,
                        nargs="?",
                        help="no. of files to get")

    args = parser.parse_args()

    # Download indices
    index_dir = os.path.join(args.data_dir, "index")
    e.download_indices(args.start_year,
                       args.end_year,
                       args.quarters,
                       index_dir,
                       args.overwrite)

    # Combine indices to csv
    e.combine_indices_to_csv(index_dir)

    # Download forms
    form_dir = os.path.join(args.data_dir, "form10k")
    download_forms(index_dir,
                   form_dir,
                   args.count_of_files if args.count_of_files else 100,
                   args.overwrite,
                   args.debug)

    # Normalize forms
    parsed_form_dir = os.path.join(args.data_dir, "form10k.parsed")
    parse_html_multiprocess(form_dir,
                            parsed_form_dir,
                            args.overwrite)

    # Parse MDA
    mda_dir = os.path.join(args.data_dir, "mda")
    metrics = parse_mda_multiprocess(parsed_form_dir,
                                     mda_dir,
                                     args.overwrite)

    print_metrics(metrics)

if __name__ == "__main__":
    main()