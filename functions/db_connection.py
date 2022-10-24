import os
from functions.args import create_parser
from sqlalchemy import create_engine
from functions.database import Base

def create_db_conection():
    #TODO the function is only creating conection to sqlite and postgres, 
    #     need to take advantage of the databases sqlalchemy and create conection 
    #     to several databases
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
        print("Conecting to Postgress{}".format(host))
    else:
        os.makedirs("./database", exist_ok=True)
        db_connection = create_engine("sqlite:///database/database.sqlite")
        print("Using SQLite Database /database/database.sqlite")
    
    Base.metadata.create_all(db_connection)

    return db_connection