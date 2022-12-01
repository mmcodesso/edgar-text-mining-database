import urllib.request
from datetime import date
from datetime import timedelta
from tqdm import tqdm
from zipfile import ZipFile 
from typing import Any, Dict, List
from itertools import chain
import json
import pandas as pd
import re


JSONType = Dict[str, Any]
SubmissionsType = Dict[str, List[str]]

submission_url = 'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip'

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url):
    """Download the file and return the local file path"""
    with DownloadProgressBar(unit='B', unit_scale=True,miniters=1, desc= 'Downloading ' + url.split('/')[-1]) as t:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mauricio Codesso m.codesso@northeastern.edu')]
        urllib.request.install_opener(opener)
        local_filename, headers = urllib.request.urlretrieve(url, reporthook=t.update_to)
    return local_filename

def merge_submission_dicts(to_merge: List[SubmissionsType]) -> SubmissionsType:
    """Merge dictionaries with same keys."""
    merged = {}
    for k in to_merge[0].keys():
        merged[k] = list(chain.from_iterable(d[k] for d in to_merge))
    return merged


def submission_processing(file,zipfile):
    filings_list = []

    sublist = re.split('[-.]',file)[1]

    if file.endswith('.json') and sublist != 'submissions':

            g = zipfile.open(file)
            data = json.load(g)

            cik = file[3:13]
            
            while cik[0] == '0':
                cik = cik[1:]

            filings = data["filings"]
            paginated_submissions = filings["files"]

            co_filings = data['filings']['recent']                        
            amount = 0

            # Handle pagination for a large number of submissions
            if paginated_submissions:
                to_merge = [filings["recent"]]

                for submission in paginated_submissions:
                    filename = submission["name"] 
                    g_append = zipfile.open(filename)
                    g_append = json.load(g_append)

                    to_merge.append(g_append)

                # Merge all paginated submissions from files key into recent and clear files list.
                co_filings = merge_submission_dicts(to_merge)
                filings["files"] = []

            form_types = ['10-K', '10-Q']
            amount = len(co_filings['form']) if amount == 0 else amount
            idx = 0

            for n in range(len(co_filings['form'])):
                if idx == amount:
                    break
                if co_filings['form'][n] not in form_types and len(form_types) > 0:
                    continue
                add_filing = {
                            "accessionNumber": co_filings['accessionNumber'][n],
                            "cik":cik,
                            "name":data["name"],
                            "form": co_filings['form'][n],
                            "filingDate": co_filings['filingDate'][n],
                            "URL": f"https://www.sec.gov/Archives/edgar/data/{cik}/{co_filings['accessionNumber'][n].replace('-', '')}/{co_filings['primaryDocument'][n]}"
                            }
                filings_list.append(add_filing)          
                idx += 1

    df = pd.DataFrame()            
    if len(filings_list) > 0:
        df = pd.DataFrame(filings_list)
            
    return df

def process_submissions(file_path):
    zipfile = ZipFile(file_path,'r')
    files = zipfile.namelist()
    
    #Process submissions.zip into a list of dataframes
    filings_list = []
    for file in tqdm(files, desc='Processing Submissions.zip'):
        fiiling_df = submission_processing(file,zipfile)
        filings_list.append(fiiling_df)

    #Transform the list into a single dataframe
    df = pd.concat(filings_list, axis=0)
    return df

    
def zip_submissions(submissions_df, output_file):
    filename = str(date.today() - timedelta(days = 1)) + '.csv'
    compression_opts = dict(method='zip',
                        archive_name=filename)  

    submissions_df.to_csv(output_file, compression=compression_opts)


def return_submissions_df(submission_url):
    """Download and process submissions.zip and return a pandas dataframe"""
    submissions_zip = download_url(submission_url) 
    submissions_df = process_submissions(submissions_zip)
    return submissions_df


if __name__ == "__main__":    
    
    submissions_df = return_submissions_df(submission_url)   
    
    #Export submissions.zip into zipped csv file
    output_file = './submissions/submissions.zip'
    zip_submissions(submissions_df,output_file)
