import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import shutil
import time
from tqdm import tqdm
import argparse
import sys

form_df = pd.read_csv("form_data.csv")
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

def ExtractText(main_text, start, end , debug = False):
    s = (main_text.find('"{}"'.format(start)))
    e = (main_text.find('"{}"'.format(end)))

    s , e = min(s,e) , max(s,e)

    if debug:
        print( "The text starts at : {} and ends at : {}".format(s,e))

    text = main_text[s:e]

    # some_iteration = BeautifulSoup(text,'html.parser')

    return text


def CheckHyperLinksForAll(url, companyname, debug=False):
    res = requests.get(url, headers=Headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    main_text = res.text

    # print(main_text)

    a_href = soup.find_all('a', href=True)

    if debug == True:
        print(url)

    foundItem7 = False
    foundItem7a = False
    foundItem8 = False

    item7 = {}
    item7a = {}
    item8 = {}

    for i in a_href:

        fullstring = i.text.lower()
        fullstring = fullstring.replace("\n", "")

        if (foundItem7 == False) and (fullstring != None) and ((("item" in fullstring) and ("7" in fullstring)) or (
                ("management" in fullstring) and ("discussion" in fullstring) and ("analysis" in fullstring))):

            foundItem7 = True

            item7 = i.attrs.copy()

            if debug:
                print("Item 7")
                print(i.attrs)
                print(fullstring)

        if (foundItem7a == False) and ((("item" in fullstring) and ("7a" in fullstring)) or (("quantitative" in fullstring) and ("qualitative" in fullstring) and ("disclosures" in fullstring)) or (("quantitative" in fullstring) and ("qualitative" in fullstring) and ("disclosure" in fullstring))  ):

            foundItem7a = True

            item7a = i.attrs.copy()

            if debug:
                print("Item 7a")
                print(i.attrs)
                print(fullstring)

        if (foundItem8 == False) and ((("item" in fullstring) and ("8" in fullstring)) or (
                ("financial" in fullstring) and ("statements" in fullstring) and ("supplementary" in fullstring)) or (
                                              ("financial" in fullstring) and ("statements" in fullstring))):

            foundItem8 = True

            item8 = i.attrs.copy()

            if debug:
                print("Item 8")
                print(i.attrs)
                print(fullstring)

    data = []

    text = ""

    some_iteration = None

    if debug:
        print("Item 7 Status: {}".format(foundItem7))
        print("Item 7a Status: {}".format(foundItem7a))
        print("Item 8 Status: {}".format(foundItem8))

    if foundItem7:
        item7ID = item7['href'][1:]
        if debug:
            print("Item 7 href id/name : {}".format(item7ID))

        if foundItem7a:

            item7aID = item7a['href'][1:]

            if debug:
                print("Item 7a href id/name : {}".format(item7aID))

            startID1 = soup.find("a", {"name": item7ID})
            startID2 = soup.find(id=item7['href'][1:])

            if (startID1 != None):

                endID1 = soup.find("a", {"name": item7aID})

                if debug:
                    print("Start ID1(name) : {}".format(startID1))

                if debug:
                    print("End ID1(name) : {}".format(endID1))

                text = ExtractText(main_text, item7ID, item7aID,debug)

            if (startID2 != None):

                endID2 = soup.find(id=item7a['href'][1:])

                if debug:
                    print("Start ID2(name) : {}".format(startID2))

                if debug:
                    print("End ID2(name) : {}".format(endID2))

                text = ExtractText(main_text, item7ID, item7aID,debug)

        else:

            item8ID = item8['href'][1:]

            if debug:
                print("Item 8 href id/name : {}".format(item8ID))

            startID1 = soup.find("a", {"name": item7ID})
            startID2 = soup.find(id=item7['href'][1:])

            if (startID1 != None):

                endID1 = soup.find("a", {"name": item8ID})

                if debug:
                    print("Start ID1(name) : {}".format(startID1))

                if debug:
                    print("End ID1(name) : {}".format(endID1))

                text = ExtractText(main_text, item7ID, item8ID,debug)

            if (startID2 != None):

                endID2 = soup.find(id=item8['href'][1:])

                if debug:
                    print("Start ID2(name) : {}".format(startID2))

                if debug:
                    print("End ID2(name) : {}".format(endID2))

                text = ExtractText(main_text, item7ID, item8ID,debug)

    return item7, item7a, item8, text

def CompaniesFromCSV(total_companies):
    result_for_all = {"Company Name": [], "URL": [], "Item 7": [], "Item 7A": [], "Item 8": [], "MDA Extract": []}

    path = "extracts/"

    os.makedirs(path, exist_ok=True)

    for index, rows in tqdm(form_df.iterrows(), total=total_companies):
        # Change here to find the number of companies to be processed.
        if (index < total_companies):

            # print("Running {}".format(index))
            # print("For company : {}".format(rows["company_name"]))

            try:
                i7, i7a, i8, mda = CheckHyperLinksForAll(rows["index_htm"], rows["company_name"], debug=False)
            except Exception as e:
                print("Exception occured for {} : {}".format(rows["company_name"], repr(e)))

            result_for_all["Company Name"].append(rows["company_name"])

            result_for_all["URL"].append(rows["index_htm"], )

            result_for_all["Item 7"].append(i7)

            result_for_all["Item 7A"].append(i7a)

            result_for_all["Item 8"].append(i8)

            result_for_all["MDA Extract"].append(mda)

            with open('extracts/{}.html'.format(rows["company_name"].replace('/', '')), 'w') as f:
                f.write(mda)

            # management_set.update(checkHyperlinksMDA(rows["index_htm"],rows["company_name"],debug=False))

            # item_set7.update(checkHyperlinksItem7(rows["index_htm"],rows["company_name"],debug=False))

            # item_set7a.update(checkHyperlinksItem7A(rows["index_htm"],rows["company_name"],debug=False))

            # item_set8.update(checkHyperlinksItem8(rows["index_htm"],rows["company_name"],debug=False))

        else:
            break

    result_for_all_pd = pd.DataFrame(result_for_all)

    result_for_all_pd.to_excel('Final-a-hrefs.xlsx', index=False)

def main():
    start_time = time.time()

    arguments = CreateParser()

    if not len(sys.argv) > 1:
        print("No arguments passed please use -h to get help on the usage")

    if arguments.number_of_companies != -1 :
        print("Getting the extract of first {} companies from the database".format(arguments.number_of_companies))
        CompaniesFromCSV(arguments.number_of_companies)

    if arguments.link_to_index_htm != "na" :

        path = "extracts/"

        os.makedirs(path, exist_ok=True)

        print("Getting the extract of  : {}".format(arguments.link_to_index_htm))

        try:
            i7, i7a, i8, mda = CheckHyperLinksForAll(arguments.link_to_index_htm, "", debug=True)
        except Exception as e:
            print("Exception occured for {} : {}".format(arguments.link_to_index_htm, repr(e)))

        with open('extracts/{}.html'.format(arguments.link_to_index_htm.replace('/', '-')), 'w') as f:
            f.write(mda)

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
