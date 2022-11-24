import urllib.request
import shutil
import os
from datetime import date
from datetime import timedelta
from functools import wraps
from tqdm import tqdm
import zipfile
from zipfile import ZipFile
from typing import Any, Dict, List
import json
import pandas as pd
import re
from itertools import chain
from glob import glob


tmp_dir = './submissions/tmp'

submission_url = 'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip'
submissions_zip = os.path.join(tmp_dir, 'submissions.zip').replace("\\", "/")

JSONType = Dict[str, Any]
SubmissionsType = Dict[str, List[str]]


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,miniters=1, desc=url.split('/')[-1]) as t:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mauricio Codesso m.codesso@northeastern.edu')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def merge_submission_dicts(to_merge: List[SubmissionsType]) -> SubmissionsType:
    """Merge dictionaries with same keys."""
    merged = {}
    for k in to_merge[0].keys():
        merged[k] = list(chain.from_iterable(d[k] for d in to_merge))
    return merged


def submission_processing(file):
    
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
            filings_list = []
            amount = 0

            # Handle pagination for a large number of requests
            if paginated_submissions:
                to_merge = [filings["recent"]]

                for submission in paginated_submissions:
                    filename = submission["name"] 
                    g_append = zipfile.open(filename)
                    g_append = json.load(g_append)

                    to_merge.append(g_append)

                # Merge all paginated submissions from files key into recent
                # and clear files list.
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
                            "cik":cik,
                            "form": co_filings['form'][n],
                            "filingDate": co_filings['filingDate'][n],
                            "URL": f"https://www.sec.gov/Archives/edgar/data/{cik}/{co_filings['accessionNumber'][n].replace('-', '')}/{co_filings['primaryDocument'][n]}"}
                
                filings_list.append(add_filing)
                        
                idx += 1
            
            if len(filings_list) > 0:
                df = pd.DataFrame(filings_list)
                df.to_csv(tmp_dir + '/submissions.csv',header=False,index=False, mode='a')


def zip_submissions():
    with zipfile.ZipFile('./submissions/submissions.zip', 'w') as zip:
        filename = str(date.today() - timedelta(days = 1)) + '.csv'
        zip.write(tmp_dir + '/submissions.csv', arcname=filename, compress_type=zipfile.ZIP_DEFLATED)


    
if __name__ == "__main__":    
    
    #Creates a Temporary folder
    shutil.rmtree(tmp_dir,ignore_errors=True)
    os.makedirs(tmp_dir, exist_ok=True)

    #Download Submissons.zip from Edgar database
    print("Downloading file submissions.zip")
    download_url(submission_url,submissions_zip)  

    #Open Submissions.zip
    print("Openning Submissions.zip")
    zipfile = ZipFile(submissions_zip,'r')
    files = zipfile.namelist()

    #Process submissions.zip into separate csv files
    for file in tqdm(files, desc='Processing Submissions.zip'):
        submission_processing(file)

    #Zip final file
    zip_submissions()

    #remove tmp folder
    shutil.rmtree(tmp_dir,ignore_errors=True)
