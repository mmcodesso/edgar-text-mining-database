import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import argparse
import sys

form_df = pd.read_csv("../form_data.csv")
Headers = {'User-Agent': 'secedgar@sharklasers.com'}

def CreateParser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n","--number_of_companies", help="Enter the number of companies for which the extract is needed",
                        type=int,default=-1)
    group.add_argument("-l", "--link_to_index_htm",help="Link to the index html file for a company",
                        type=str, default="na")
    args = parser.parse_args()
    return args

def TableOfContent(url, companyname, debug=False):

    res = requests.get(url,headers=Headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    tables = soup.findAll('table')

    maxReferences = -1
    result = {}
    contents = []
    tableContents = None

    tableCount = 0

    for table in tables:

        if tableCount < 25:

            data = []

            currentReferences = 0

            tableFoundReferences = {
                "foundItem1": False, "foundItem1b": False,
                "foundItem1a": False,
                "foundItem2": False,
                "foundItem3": False,
                "foundItem4": False,
                "foundItem5": False,
                "foundItem6": False,
                "foundItem7": False,
                "foundItem7a": False,
                "foundItem8": False
            }

            for row in table.find_all('tr'):
                cols = row.find_all('td')
                cols1 = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols1 if ele])

                for ele in cols:
                    fullstring = ele.text.lower()
                    fullstring = fullstring.replace("\n","")

                    if (tableFoundReferences["foundItem1"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("1" in fullstring)) or (
                            ("business" in fullstring))):
                        tableFoundReferences["foundItem1"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem1a"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("1a" in fullstring)) or (
                            ("risk" in fullstring) and ("factor" in fullstring) )):

                        tableFoundReferences["foundItem1a"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem1b"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("1b" in fullstring)) or (
                            ("unresolved" in fullstring) and ("staff" in fullstring) and ("comments" in fullstring))):

                        tableFoundReferences["foundItem1b"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem2"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("2" in fullstring)) or (
                            ("properties" in fullstring))):

                        tableFoundReferences["foundItem2"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem3"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("3" in fullstring)) or (
                            ("legal" in fullstring) and ("proceedings" in fullstring) )):

                        tableFoundReferences["foundItem3"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem4"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("4" in fullstring)) or (
                            ("mine" in fullstring) and ("safety" in fullstring) or ( ("mine" in fullstring) and ("safety" in fullstring) and ("disclosures" in fullstring)))):

                        tableFoundReferences["foundItem4"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem5"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("5" in fullstring)) or (
                            ("market" in fullstring) and ("registrant’s" in fullstring) and ("common" in fullstring))):

                        tableFoundReferences["foundItem5"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem6"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("6" in fullstring)) or (
                            ("selected" in fullstring) and ("financial" in fullstring) and ("data" in fullstring))):

                        tableFoundReferences["foundItem6"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem7"] == False) and (fullstring != None) and (
                            (("item" in fullstring) and ("7" in fullstring)) or (
                            ("management" in fullstring) and ("discussion" in fullstring) and ("analysis" in fullstring))):

                        tableFoundReferences["foundItem7"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem7a"] == False) and ((("item" in fullstring) and ("7a" in fullstring)) or (
                            ("quantitative" in fullstring) and ("qualitative" in fullstring) and (
                            "disclosures" in fullstring)) or (("quantitative" in fullstring) and (
                            "qualitative" in fullstring) and ("disclosure" in fullstring))):


                        tableFoundReferences["foundItem7a"] = True
                        currentReferences += 1

                        if debug:
                            print(fullstring)

                    if (tableFoundReferences["foundItem8"] == False) and ((("item" in fullstring) and ("8" in fullstring)) or (
                            ("financial" in fullstring) and ("statements" in fullstring) and (
                            "supplementary" in fullstring)) or (
                                                          ("financial" in fullstring) and ("statements" in fullstring))):

                        tableFoundReferences["foundItem8"] = True
                        currentReferences += 1


                        if debug:
                            print(fullstring)

            if currentReferences > maxReferences and currentReferences > 4:
                maxReferences = currentReferences
                result = tableFoundReferences
                contents = data
                tableContents = table
        tableCount+=1
    if debug:
        table_df = pd.DataFrame(contents)
        print(table_df)


    return result,tableContents

def main():
    arguments = CreateParser()

    if not len(sys.argv) > 1:
        print("No arguments passed please use -h to get help on the usage")

    if arguments.number_of_companies != -1:
        total_companies = arguments.number_of_companies
        print("Getting the extract of first {} companies from the database".format(arguments.number_of_companies))

        results = []

        for index, rows in tqdm(form_df.iterrows(), total=total_companies):
            # Change here to find the number of companies to be processed.
            if (index < total_companies):

                # print("Running {}".format(index))
                # print("For company : {}".format(rows["company_name"]))

                try:
                    status,table = TableOfContent(rows["index_htm"], rows["company_name"], debug=False)
                except Exception as e:
                    print("Exception occured for {} : {}".format(rows["company_name"], repr(e)))

                status["Company"] = rows["company_name"]
                status["Index_htm"] = rows["index_htm"]
                status["Table HTML"] = table

                results.append(status)

        resultDF = pd.DataFrame(results)
        resultDF.to_excel("table-of-contents.xlsx",index=False)

    if arguments.link_to_index_htm != "na" :

        print("Getting the extract of  : {}".format(arguments.link_to_index_htm))


        url = arguments.link_to_index_htm

        status,table = TableOfContent(url,"",debug=False)

        print(status)
        print(table)


        # res = requests.get(arguments.link_to_index_htm, headers=Headers)
        #
        # soup = BeautifulSoup(res.text, 'html.parser')
        #
        # tables = soup.findAll('table')
        #
        # table_data = []
        #
        # text = ""
        #
        # for table in tables:
        #     data = []
        #     for row in table.find_all('tr'):
        #         cols = row.find_all('td')
        #
        #         cols = [ele.text.strip() for ele in cols]
        #
        #         data.append([ele for ele in cols if ele])  # Get rid of empty values
        #
        #     table_data.append(data)
        #
        # #print(text)
        #
        # with open("tables.html" , 'w') as f:
        #     f.write(text)
        #
        # i = 0
        # for table in table_data:
        #     table_df = pd.DataFrame(table)
        #
        #     table_df.to_excel('{}.xlsx'.format(i),index=False)
        #     i += 1



if __name__ == "__main__":
    main()