"""
script to download tge index and store in a database
"""
import itertools
import os
import time
from functools import wraps

import requests
import pandas as pd
from sqlalchemy import create_engine
from args import create_parser

SEC_GOV_URL = 'https://www.sec.gov/Archives'
FORM_INDEX_URL = os.path.join(
    SEC_GOV_URL, 'edgar', 'full-index', '{}', 'QTR{}', 'form.idx').replace("\\", "/")

def main():
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    #Create database conection
    db_conection = create_db_conection(args.user,args.password,args.host, args.dbname)
      
    # Download indices
    download_indices(args.start_year, args.end_year,
                     args.quarters, db_conection, args.overwrite)


def create_db_conection(user: str, password: str, host : str, dbname : str):
    """ 
    Create database conection. If not informed, it will create a sqlite database on ./database/database.sqlite
    """  
    if user and password and host and dbname:
        db_connection = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{dbname}".format(user = user,password = password,host = host,dbname = dbname))
    else:
        os.makedirs("./database", exist_ok=True)
        db_connection = create_engine("sqlite:///database/database.sqlite")
    return db_connection


def timeit(f):
    @wraps(f)
    def wrapper(*args, **kw):
        start_time = time.time()
        result = f(*args, **kw)
        end_time = time.time()
        print("{} took {:.2f} seconds."
              .format(f.__name__, end_time-start_time))
        return result
    return wrapper


def parse_line_to_record(line, fields_begin):
    """
    Example:
    10-K        1347 Capital Corp                                             1606163     2016-03-21  edgar/data/1606163/0001144204-16-089184.txt 

    Returns:
    ["10-K", "1347 Capital Corp","160613", "2016-03-21", "edgar/data/1606163/0001144204-16-089184.txt"]
    """
    record = []
    fields_indices = fields_begin + [len(line)]
    for begin, end in zip(fields_indices[:-1], fields_indices[1:]):
        field = line[begin:end].rstrip()
        field = field.strip('\"')
        record.append(field)
    return record


@timeit
def download_indices(start_year: int, end_year: int, quarters: list, db_conection: str, overwrite: bool):
    """ Downloads edgar 10k form indices with multiprocess
    Args:
        start_year (int): starting year
        end_year (int): ending year
        quarter (list): quartes
        db_conection: database conection
    """
    # Create a list of the forms to download
    forms = []
        
    # Prepare arguments
    years = range(start_year, end_year+1)
    urls = [FORM_INDEX_URL.format(year, qtr)
            for year, qtr in itertools.product(years, quarters)]
    
    for url in urls:
        print("Requesting {}".format(url))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
        res = requests.get(url, headers=headers).text
        arrived = False
        fields_begin = None
        for line in res.split('\n'):
            if line.startswith("Form Type"):
                fields_begin = [line.find("Form Type"),
                                line.find("Company Name"),
                                line.find('CIK'),
                                line.find('Date Filed'),
                                line.find("File Name")]
            elif line.startswith("10-Q") or line.startswith("10-K"):
                assert fields_begin is not None
                arrived = True
                row = parse_line_to_record(line, fields_begin)     
                row_dict = {"form_type" : row[0],
                            "company_name" : row[1],
                            'cik' : row[2],
                            'date_filed' : row[3],
                            "file_name" : row[4]}
                forms.append(row_dict)
            elif arrived:
                    break
        
    forms_df = pd.DataFrame(forms)
    forms_df = forms_df[(forms_df['form_type'] == "10-K") | (forms_df['form_type'] == "10-Q")]
    forms_df.to_sql('index_queue',con = db_conection,if_exists='replace',index=False)


if __name__ == "__main__":
    main()