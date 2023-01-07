import os
import sys
import time
from tqdm import tqdm
import pandas as pd

from functions.args import CreateParser
from functions.ExtractItems import *

form_df = pd.read_csv("form_data.csv")
Headers = {'User-Agent': 'secedgar@sharklasers.com'}

def main():
    start_time = time.time()

    arguments = CreateParser()

    path = "extracts/"
    item = arguments.item

    if not len(sys.argv) > 1:
        print("No arguments passed please use -h to get help on the usage")

    if arguments.number_of_companies != -1 :
        print("Extracting Item {}".format(item))
        print("Getting the extract of first {} companies from the database".format(arguments.number_of_companies))

        total_companies = arguments.number_of_companies
        os.makedirs(path, exist_ok=True)

        if item == "1A":

            path1A = path+"/Item 1A/"
            os.makedirs(path1A, exist_ok=True)

            item1Aresult = {"Company Name": [], "URL": [], "Item 1A": [], "Item 1B": [], "Item 2": [],
                              "Extract": []}

            for index, row in tqdm(form_df.iterrows(), total=total_companies):
                # Change here to find the number of companies to be processed.
                if (index < total_companies):
                    try:
                        i1a, i1b, i2, item1Aextract = ExtractItem1A(row["index_htm"],row["company_name"],debug=False)
                    except Exception as e:
                        print("Exception occured for {} : {}".format("URL", repr(e)))
                    with open(path1A+'{}.html'.format(row["company_name"].replace('/', '-')), 'w') as f:
                        f.write(item1Aextract)

                    item1Aresult["Company Name"].append(row["company_name"])
                    item1Aresult["URL"].append(row["index_htm"])
                    item1Aresult["Item 1A"].append(i1a)
                    item1Aresult["Item 1B"].append(i1b)
                    item1Aresult["Item 2"].append(i2)
                    item1Aresult["Extract"].append(item1Aextract)

                else:
                    break

            pd.DataFrame(item1Aresult).to_excel(path + "Item-1A-Extracts.xlsx", index=False)

        if item == "7":

            path7 = path+"/Item 7/"
            os.makedirs(path7, exist_ok=True)

            item7result = {"Company Name": [], "URL": [], "Item 7": [], "Item 7A": [], "Item 8": [],
                              "Extract": []}

            for index, row in tqdm(form_df.iterrows(), total=total_companies):

                if (index < total_companies):

                    try:
                        i7, i7a, i8, item7extract = ExtractItem7(row["index_htm"],row["company_name"],debug=False)
                    except Exception as e:
                        print("Exception occured for {} : {}".format("URL", repr(e)))
                    with open(path7+'{}.html'.format(row["company_name"].replace('/', '-')), 'w') as f:
                        f.write(item7extract)

                    item7result["Company Name"].append(row["company_name"])
                    item7result["URL"].append(row["index_htm"])
                    item7result["Item 7"].append(i7)
                    item7result["Item 7A"].append(i7a)
                    item7result["Item 8"].append(i8)
                    item7result["Extract"].append(item7extract)

                else:
                    break

            pd.DataFrame(item7result).to_excel(path + "Item-7-Extracts.xlsx", index=False)

    if arguments.link_to_index_htm!= "na":

        if item == "1A":

            path1A = path + "/Item 1A/"
            os.makedirs(path1A, exist_ok=True)

            print("Extracting Item {}".format(arguments.link_to_index_htm))

            try:
                i1a, i1b, i2, item1Aextract= ExtractItem1A(arguments.link_to_index_htm, "ExtractedCompany", debug=False)
            except Exception as e:
                print("Exception occured for {} : {}".format("URL", repr(e)))
            with open(path1A + '{}.html'.format("ExtractedCompany".replace('/', '-')), 'w') as f:
                f.write(item1Aextract)

        if item == "7":

            path7 = path+"/Item 7/"
            os.makedirs(path7, exist_ok=True)

            print("Extracting Item {}".format(arguments.link_to_index_htm))

            try:
                i7, i7a, i8, item7extract = ExtractItem7(arguments.link_to_index_htm, "ExtractedCompany", debug=False)
            except Exception as e:
                print("Exception occured for {} : {}".format("URL", repr(e)))
            with open(path7 + '{}.html'.format("ExtractedCompany".replace('/', '-')), 'w') as f:
                f.write(item7extract)


    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
