import requests
from bs4 import BeautifulSoup

Headers = {'User-Agent': 'secedgar@sharklasers.com'}

from .CheckItems import *

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

        if (foundItem1a == False) and CheckItem1ALabel(fullstring, debug=debug):

            foundItem1a = True

            item1a = i.attrs.copy()

            if debug:
                print("Item 1A")
                print(i.attrs)
                print(fullstring)

        if (foundItem1b == False) and CheckItem1BLabel(fullstring, debug=debug):
            foundItem1b = True

            item1b = i.attrs.copy()

            if debug:
                print("Item 1B")
                print(i.attrs)
                print(fullstring)

        if (foundItem2 == False) and CheckItem2Label(fullstring, debug=debug):

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
            print("Item 1A href id/name : {}".format(item1AID))

        if foundItem1b:

            item1BID = item1b['href'][1:]

            if debug:
                print("Item 1B href id/name : {}".format(item1BID))

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
                print("Item 2 href id/name : {}".format(item2ID))

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

def ExtractItem7(url, companyname, debug=False):
    res = requests.get(url, headers=Headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    main_text = res.text

    # print(main_text)

    a_href = soup.find_all('a', href=True)

    if debug:
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

        if (foundItem7 == False) and CheckItem7Label(fullstring, debug=debug):

            foundItem7 = True

            item7 = i.attrs.copy()

            if debug:
                print("Item 7")
                print(i.attrs)
                print(fullstring)

        if (foundItem7a == False) and CheckItem7ALabel(fullstring, debug=debug):

            foundItem7a = True

            item7a = i.attrs.copy()

            if debug:
                print("Item 7a")
                print(i.attrs)
                print(fullstring)

        if (foundItem8 == False) and CheckItem8Label(fullstring, debug=debug):

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
