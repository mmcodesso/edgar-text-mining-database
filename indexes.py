"""
script to download tge index and store in a database
"""
import itertools
import os
from telnetlib import STATUS

from sqlalchemy.orm import Session
from sqlalchemy import select, update
from functions.args import create_parser
from functions.timeit import timeit
from functions.db_connection import create_db_conection
from functions.database import form_index, form


import requests
import pandas as pd


# Parse arguments
args =create_parser()
company = args.company 
email = args.email
SEC_GOV_URL = 'https://www.sec.gov/Archives'

#Create database conection
engine = create_db_conection()


def main():
    # Create form index url
    create_form_index_url(args.start_year, args.end_year,args.quarters)

    #Process form_index
    process_form_index()


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


def create_form_index_url(start_year: int, end_year: int, quarters: list):
    """ Downloads edgar 10k form indices with multiprocess
    Args:
        start_year (int): starting year
        end_year (int): ending year
        quarter (list): quartes
        db_conection: database conection
    """
    
    #Define SEC and FORM URL
    FORM_INDEX_URL = os.path.join(SEC_GOV_URL, 'edgar', 'full-index', '{}', 'QTR{}', 'form.idx').replace("\\", "/")
        
    # Prepare arguments
    years = range(start_year, end_year+1)
    urls = [FORM_INDEX_URL.format(year, qtr)
            for year, qtr in itertools.product(years, quarters)]

  
    #Return form indexes url already in the database
    db_forms = select(form_index)
    with Session(engine) as session:
        db_forms = session.execute(db_forms).all()

    db_forms = [form[0].form_index for form in db_forms]
    form_list = list(set(urls) - set(db_forms))
    form_list = [form_index(form_index = form, status=0) for form in form_list]
   
    with Session(engine) as session:
        session.add_all(form_list)
        session.commit()

    return

    
def process_form_index():
    """ Process Form_Index URL
    """     
    session = Session(engine)

    statement  = select(form_index.form_index).filter_by(status=0)
    urls = session.execute(statement).all()

    forms = []
    for url in urls:
        print("Requesting {}".format(url[0]))

        if company and email:
            headers = {'User-Agent': company + " " + email}
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

        res = requests.get(url[0], headers=headers).text
        arrived = False
        fields_begin = None
        forms_list = []
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
                row_dict = {"id": row[2] + "-" + str(row[4]).split('/')[-1][:-4], 
                            "form_type" : row[0],
                            "company_name" : row[1],
                            'cik' : row[2],
                            'date_filed' : row[3],
                            "file_name" : row[4],
                            "form_index": url[0],
                            "index_url": os.path.join(SEC_GOV_URL, row[4][:-4]).replace("\\", "/") +  '-index.html',
                            "file" : '',
                            "status" : 0}
                if row_dict['form_type'] == "10-K" or row_dict['form_type'] == "10-Q":
                    form_row = form(form_id = row_dict['id'],
                                    form_type = row_dict['form_type'],
                                    company_name = row_dict['company_name'], 
                                    cik = row_dict['cik'],
                                    date_filed = row_dict['date_filed'],
                                    file_name = row_dict['file_name'],
                                    form_index =row_dict['form_index'],
                                    index_url = row_dict['index_url'],
                                    file = row_dict['file'],
                                    status = row_dict['status'])
                    forms_list.append(form_row)
            elif arrived:
                    break

        #insert form into database
        stmt = (
            update(form_index)
            .where(form_index.form_index ==url[0])
            .values(status=1)
        )

        with Session(engine) as session:
            session.add_all(forms_list)
            session.execute(stmt)
            session.commit()

    return


if __name__ == "__main__":
    main()