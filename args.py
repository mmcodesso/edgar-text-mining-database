import argparse
from sqlalchemy import create_engine
import os

#set default year to last year
import datetime
current_time = datetime.datetime.now()
year = current_time.year - 1

def create_parser():
    """Argument Parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_year', type=int, default=year,
                        help="year to start")
    parser.add_argument('-e', '--end_year', type=int, default=year,
                        help="year to end")
    parser.add_argument('-q', '--quarters', type=int, nargs="+",
                        default=[1, 2, 3, 4], help="quarters to download for start to end years")
    parser.add_argument('-d', '--data_dir', type=str,
                        default="./data", help="path to save data")
    parser.add_argument('--overwrite', action="store_true",
                        help="If True, overwrites downloads and processed files.")
    parser.add_argument('-u','--user', help="database username")
    parser.add_argument('-p','--password', help="database password")
    parser.add_argument('-server','--host', help="database address")
    parser.add_argument('-db','--dbname', help="database")
    parser.add_argument('--debug', action="store_true",help="Debug mode")
    parser.add_argument('-company','--company', type=str, help="Company to inform EDGAR")
    parser.add_argument('-email','--email', type=str, help="Email to inform EDGAR")
    return parser.parse_args()

def create_db_conection():
    #create_db_conection(user: str, password: str, host : str, dbname : str):
    """ 
    Create database conection. If not informed, it will create a 
    sqlite database on ./database/database.sqlite
    """ 
    args =create_parser()
    user = args.user
    password = args.password
    host = args.host
    dbname = args.dbname

    if user and password and host and dbname:
        db_connection = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{dbname}"
                    .format(user = user,password = password,host = host,dbname = dbname))
    else:
        os.makedirs("./database", exist_ok=True)
        db_connection = create_engine("sqlite:///database/database.sqlite")
    return db_connection