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

def ExtractText(main_text, start, end , debug = False):

    s = (main_text.find('"{}"'.format(start)))
    e = (main_text.find('"{}"'.format(end)))

    s , e = min(s,e) , max(s,e)

    if debug:
        print( "The text starts at : {} and ends at : {}".format(s,e))

    text = main_text[s:e]

    # some_iteration = BeautifulSoup(text,'html.parser')

    return text


def ExtractItem1A(url, companyname, debug=False):
    res = requests.get(url, headers=Headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    main_text = res.text

    # print(main_text)

    a_href = soup.find_all('a', href=True)

    if debug:
        print(url)

    foundItem1a = False
    foundItem1b = False
    foundItem2 = False

    item1a = {}
    item1b = {}
    item2 = {}

    for i in a_href:

        fullstring = i.text.lower()
        fullstring = fullstring.replace("\n", "")

        if (foundItem1a == False) and (fullstring != None) and (
                (("item" in fullstring) and ("1a" in fullstring)) or (
                ("risk" in fullstring) and ("factor" in fullstring))):

            foundItem1a = True

            item1a = i.attrs.copy()

            if debug:
                print("Item 1A")
                print(i.attrs)
                print(fullstring)

        if (foundItem1b == False) and (fullstring != None) and (
                (("item" in fullstring) and ("1b" in fullstring)) or (
                ("unresolved" in fullstring) and ("staff" in fullstring) and ("comments" in fullstring))):
            foundItem1b = True

            item1b = i.attrs.copy()

            if debug:
                print("Item 1B")
                print(i.attrs)
                print(fullstring)

        if (foundItem2 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("2" in fullstring)) or (
                ("properties" in fullstring))):

            foundItem2 = True

            item2 = i.attrs.copy()

            if debug:
                print("Item 2")
                print(i.attrs)
                print(fullstring)

    data = []

    text = ""

    some_iteration = None

    if debug:
        print("Item 1A Status: {}".format(foundItem1a))
        print("Item 1B Status: {}".format(foundItem1b))
        print("Item 2 Status: {}".format(foundItem2))

    if foundItem1a:
        item1AID = item1a['href'][1:]
        if debug:
            print("Item 7 href id/name : {}".format(item1AID))

        if foundItem1b:

            item1BID = item1b['href'][1:]

            if debug:
                print("Item 7a href id/name : {}".format(item1BID))

            startID1 = soup.find("a", {"name": item1AID})
            startID2 = soup.find(id=item1a['href'][1:])

            if (startID1 != None):

                endID1 = soup.find("a", {"name": item1BID})

                if debug:
                    print("Start ID1(name) : {}".format(startID1))

                if debug:
                    print("End ID1(name) : {}".format(endID1))

                text = ExtractText(main_text, item1AID, item1BID, debug)

            if (startID2 != None):

                endID2 = soup.find(id=item1b['href'][1:])

                if debug:
                    print("Start ID2(name) : {}".format(startID2))

                if debug:
                    print("End ID2(name) : {}".format(endID2))

                text = ExtractText(main_text, item1AID, item1BID, debug)

        else:

            item2ID = item2['href'][1:]

            if debug:
                print("Item 8 href id/name : {}".format(item2ID))

            startID1 = soup.find("a", {"name": item1AID})
            startID2 = soup.find(id=item1a['href'][1:])

            if (startID1 != None):

                endID1 = soup.find("a", {"name": item2ID})

                if debug:
                    print("Start ID1(name) : {}".format(startID1))

                if debug:
                    print("End ID1(name) : {}".format(endID1))

                text = ExtractText(main_text, item1AID, item2ID, debug)

            if (startID2 != None):

                endID2 = soup.find(id=item2['href'][1:])

                if debug:
                    print("Start ID2(name) : {}".format(startID2))

                if debug:
                    print("End ID2(name) : {}".format(endID2))

                text = ExtractText(main_text, item1AID, item2ID, debug)

    return item1a, item1b, item2, text

def Analyse1A(url, companyname, debug=False):

    if debug:
        print(companyname)

    res = requests.get(url, headers=Headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    if debug:
        print(url)

    a_href = soup.find_all('a', href=True)

    results_item1a = set()

    for i in a_href:
        fullstring = i.text.lower()
        fullstring = fullstring.replace("\n","")

        if  (fullstring != None) and (
                (("item" in fullstring) and ("1a" in fullstring)) or (
                ("risk" in fullstring) and ("factor" in fullstring) )):

            results_item1a.add(i.text)

            if debug:
                print("Possible Item 1A : {}".format(i.text))
                print(i.attrs)
                print(fullstring)

    return results_item1a

def AnalyseTable(url, companyname, debug=False):

    res = requests.get(url,headers=Headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    a_href = soup.find_all('a',href=True)

    if debug:
        print(url)

    foundItem1 = False
    foundItem1b = False
    foundItem1a = False
    foundItem2 = False
    foundItem3 = False
    foundItem4 = False
    foundItem5 = False
    foundItem6 = False
    foundItem7 = False
    foundItem7a = False
    foundItem8 = False

    item1 = {}
    item1b = {}
    item1a = {}
    item2 = {}
    item3 = {}
    item4 = {}
    item5 = {}
    item6 = {}
    item7 = {}
    item7a = {}
    item8 = {}


    for i in a_href:
        fullstring = i.text.lower()
        fullstring = fullstring.replace("\n","")

        if (foundItem1 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("1" in fullstring)) or (
                ("business" in fullstring))):
            foundItem1 = True

            #item1 = i.attrs.copy()
            item1 = i.text

            if debug:
                print("Item 1")
                print(i.attrs)
                print(fullstring)

        if (foundItem1a == False) and (fullstring != None) and (
                (("item" in fullstring) and ("1a" in fullstring)) or (
                ("risk" in fullstring) and ("factor" in fullstring) )):

            foundItem1a = True

            #item1a = i.attrs.copy()
            item1a = i.text

            if debug:
                print("Item 1A")
                print(i.attrs)
                print(fullstring)

        if (foundItem1b == False) and (fullstring != None) and (
                (("item" in fullstring) and ("1b" in fullstring)) or (
                ("unresolved" in fullstring) and ("staff" in fullstring) and ("comments" in fullstring))):

            foundItem1b = True

            #item1b = i.attrs.copy()
            item1b = i.text

            if debug:
                print("Item 1B")
                print(i.attrs)
                print(fullstring)

        if (foundItem2 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("2" in fullstring)) or (
                ("properties" in fullstring))):

            foundItem2 = True

            #item2 = i.attrs.copy()
            item2 = i.text

            if debug:
                print("Item 2")
                print(i.attrs)
                print(fullstring)

        if (foundItem3 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("3" in fullstring)) or (
                ("legal" in fullstring) and ("proceedings" in fullstring) )):

            foundItem3 = True

            #item3 = i.attrs.copy()
            item3 = i.text

            if debug:
                print("Item 3")
                print(i.attrs)
                print(fullstring)

        if (foundItem4 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("4" in fullstring)) or (
                ("mine" in fullstring) and ("safety" in fullstring) or ( ("mine" in fullstring) and ("safety" in fullstring) and ("disclosures" in fullstring)))):

            foundItem4 = True

            #item4 = i.attrs.copy()
            item4 = i.text

            if debug:
                print("Item 4")
                print(i.attrs)
                print(fullstring)

        if (foundItem5 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("5" in fullstring)) or (
                ("market" in fullstring) and ("registrant’s" in fullstring) and ("common" in fullstring))):

            foundItem5 = True

            #item5 = i.attrs.copy()
            item5 = i.text

            if debug:
                print("Item 5")
                print(i.attrs)
                print(fullstring)

        if (foundItem6 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("6" in fullstring)) or (
                ("selected" in fullstring) and ("financial" in fullstring) and ("data" in fullstring))):

            foundItem6 = True

            #item6 = i.attrs.copy()
            item6 = i.text

            if debug:
                print("Item 6")
                print(i.attrs)
                print(fullstring)

        if (foundItem7 == False) and (fullstring != None) and (
                (("item" in fullstring) and ("7" in fullstring)) or (
                ("management" in fullstring) and ("discussion" in fullstring) and ("analysis" in fullstring))):

            foundItem7 = True

            #item7 = i.attrs.copy()
            item7 = i.text

            if debug:
                print("Item 7")
                print(i.attrs)
                print(fullstring)

        if (foundItem7a == False) and ((("item" in fullstring) and ("7a" in fullstring)) or (
                ("quantitative" in fullstring) and ("qualitative" in fullstring) and (
                "disclosures" in fullstring)) or (("quantitative" in fullstring) and (
                "qualitative" in fullstring) and ("disclosure" in fullstring))):



            foundItem7a = True

            #item7a = i.attrs.copy()
            item7a = i.text

            if debug:
                print("Item 7A")
                print(i.attrs)
                print(fullstring)

        if (foundItem8 == False) and ((("item" in fullstring) and ("8" in fullstring)) or (
                ("financial" in fullstring) and ("statements" in fullstring) and (
                "supplementary" in fullstring)) or (
                                              ("financial" in fullstring) and ("statements" in fullstring))):

            foundItem8 = True

            #item8 = i.attrs.copy()
            item8 = i.text

            if debug:
                print("Item 8")
                print(i.attrs)
                print(fullstring)



    results = {}

    results["1"] = item1
    results["1A"] = item1a
    results["1B"] = item1b
    results["2"] = item2
    results["3"] = item3
    results["4"] = item4
    results["5"] = item5
    results["6"] = item6
    results["7"] = item7
    results["7A"] = item7a
    results["8"] = item8
    return results

def main():
    start_time = time.time()

    arguments = CreateParser()

    if not len(sys.argv) > 1:
        print("No arguments passed please use -h to get help on the usage")

    if arguments.number_of_companies != -1 :
        print("Getting the extract of first {} companies from the database".format(arguments.number_of_companies))

        columns = ["Company Name", "1" , "1A" , "1B" , "2" , "3" , "4" , "5" , "6" , "7" , "7A" , "8", "URL"]
        results_dict = {"Company Name":[], "1":[], "1A":[], "1B":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "7A":[], "8":[], "URL":[]}
        results_item1a = {"Possible Item 1A" : [] }
        results_item1a_set = set()

        results_item1a_extract = {"Company Name" : [] , "URL" : [] ,"Item 1A" : [] , "Item 1B" : [] , "Item 2" : [] , "Extracts" : []}

        total_companies = arguments.number_of_companies
        columns_item1 = ["Possible ITEM 1"]
        columns_item1a = ["Possible ITEM 1A"]
        columns_item1b = ["Possible ITEM 1B"]
        columns_item2 = ["Possible ITEM 2"]
        columns_item3 = ["Possible ITEM 3"]
        columns_item4 = ["Possible ITEM 4"]
        columns_item5 = ["Possible ITEM 5"]
        columns_item6 = ["Possible ITEM 6"]
        columns_item7 = ["Possible ITEM 7"]
        columns_item7a = ["Possible ITEM 7A"]
        columns_item8 = ["Possible ITEM 8"]

        results_pd = pd.DataFrame(columns = columns)

        for index, rows in tqdm(form_df.iterrows(), total=total_companies):
            # Change here to find the number of companies to be processed.
            if (index < total_companies):

                path = "../extracts/Item1A"

                os.makedirs(path, exist_ok=True)
                try:
                    i1a, i1b, i2, item1Aextract = ExtractItem1A(rows["index_htm"], rows["company_name"], debug=False)
                except Exception as e:
                    print("Exception occured for {} : {}".format(rows["company_name"], repr(e)))
                with open('../extracts/Item1A/{}.html'.format(rows["company_name"].replace('/', '-')), 'w') as f:
                    f.write(item1Aextract)

                results_item1a_extract["Company Name"].append(rows["company_name"])
                results_item1a_extract["URL"].append(rows["index_htm"])
                results_item1a_extract["Item 1A"].append(i1a)
                results_item1a_extract["Item 1B"].append(i1b)
                results_item1a_extract["Item 2"].append(i2)
                results_item1a_extract["Extracts"].append(item1Aextract)

                results_item1a_pd = pd.DataFrame(data=results_item1a_extract)
                results_item1a_pd.to_excel("Item-1A-extracts.xlsx" , index=False)
            else:
                break
                # try:
                #     results = Analyse1A(rows["index_htm"], rows["company_name"], debug=False)
                # except Exception as e:
                #     print("Exception occured for {} : {}".format(rows["company_name"], repr(e)))
                #
                # for i in results:
                #     results_item1a_set.add(i)

                # print("Running {}".format(index))
                # print("For company : {}".format(rows["company_name"]))

                # try:
                #     results = AnalyseTable(rows["index_htm"], rows["company_name"], debug=False)
                # except Exception as e:
                #     print("Exception occured for {} : {}".format(rows["company_name"], repr(e)))
                #
                # results_dict["Company Name"].append(rows["company_name"])
                # results_dict["1"].append(results["1"])
                # results_dict["1A"].append(results["1A"])
                # results_dict["1B"].append(results["1B"])
                # results_dict["2"].append(results["2"])
                # results_dict["3"].append(results["3"])
                # results_dict["4"].append(results["4"])
                # results_dict["5"].append(results["5"])
                # results_dict["6"].append(results["6"])
                # results_dict["7"].append(results["7"])
                # results_dict["7A"].append(results["7A"])
                # results_dict["8"].append(results["8"])
                # results_dict["URL"].append(rows["index_htm"])



        # results_pd = pd.DataFrame(results_dict)
        # results_pd.to_excel("Item-Headers.xlsx",index=False)


        # for i in results_item1a_set:
        #     results_item1a["Possible Item 1A"].append(i)
        #
        # possibleItem1A = pd.DataFrame(data=results_item1a)
        #
        # possibleItem1A.to_excel("Possible-Item1A.xlsx",index=False)

    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
    main()