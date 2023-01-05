def CheckItem1Label(text, debug = False):
    "Checks if the label belongs to Item 1"

    if (text != None) and (
            (("item" in text) and ("1" in text)) or (
            ("business" in text))):

        if debug:
            print("Item 1 found with text : {}".format(text))

        return True

    return False

def CheckItem1ALabel(text, debug = False):
    "Checks if the label belongs to Item 1A"

    if (text != None) and (
                (("item" in text) and ("1a" in text)) or (
                ("risk" in text) and ("factor" in text) )):

        if debug:
            print("Item 1A with text : {}".format(text))

        return True

    return False

def CheckItem1BLabel(text, debug = False):
    "Checks if the label belongs to Item 1B"

    if (text != None) and (
            (("item" in text) and ("1b" in text)) or (
            ("unresolved" in text) and ("staff" in text) and ("comments" in text))):

        if debug:
            print("Item 1B with text : {}".format(text))

        return True

    return False

def CheckItem2Label(text, debug = False):
    "Checks if the label belongs to Item 2"

    if (text != None) and (
            (("item" in text) and ("2" in text)) or (
            ("properties" in text))):
        if debug:
            print("Item 2 with text : {}".format(text))

        return True

    return False

def CheckItem3Label(text, debug = False):
    "Checks if the label belongs to Item 3"

    if (text != None) and (
            (("item" in text) and ("3" in text)) or (
            ("legal" in text) and ("proceedings" in text))):

        if debug:
            print("Item 3 with text : {}".format(text))

        return True

    return False

def CheckItem4Label(text, debug = False):
    "Checks if the label belongs to Item 4"

    if (text != None) and (
            (("item" in text) and ("4" in text)) or (
            ("mine" in text) and ("safety" in text) or (
            ("mine" in text) and ("safety" in text) and ("disclosures" in text)))):

        if debug:
            print("Item 4 with text : {}".format(text))

        return True

    return False

def CheckItem5Label(text, debug = False):
    "Checks if the label belongs to Item 5"

    if (text != None) and (
            (("item" in text) and ("5" in text)) or (
            ("market" in text) and ("registrant’s" in text) and ("common" in text))):

        if debug:
            print("Item 5 with text : {}".format(text))

        return True

    return False

def CheckItem6Label(text, debug = False):
    "Checks if the label belongs to Item 6"

    if (text != None) and (
            (("item" in text) and ("6" in text)) or (
            ("selected" in text) and ("financial" in text) and ("data" in text))):
        if debug:
            print("Item 6 with text : {}".format(text))

        return True

    return False

def CheckItem7Label(text, debug = False):
    "Checks if the label belongs to Item 7"

    if (text != None) and (
            (("item" in text) and ("7" in text)) or (
            ("management" in text) and ("discussion" in text) and ("analysis" in text))):
        if debug:
            print("Item 7 with text : {}".format(text))

        return True

    return False

def CheckItem7ALabel(text, debug = False):
    "Checks if the label belongs to Item 7A"

    if (text != None) and ((("item" in text) and ("7a" in text)) or (
            ("quantitative" in text) and ("qualitative" in text) and (
            "disclosures" in text)) or (("quantitative" in text) and (
            "qualitative" in text) and ("disclosure" in text))):
        if debug:
            print("Item 7A with text : {}".format(text))

        return True

    return False

def CheckItem8Label(text, debug = False):
    "Checks if the label belongs to Item 8"

    if (text != None) and ((("item" in text) and ("8" in text)) or (
            ("financial" in text) and ("statements" in text) and (
            "supplementary" in text)) or (
                                          ("financial" in text) and ("statements" in text))):
        if debug:
            print("Item 7A with text : {}".format(text))

        return True

    return False

# def AnalyseTable(url, companyname, debug=False):
#
#     res = requests.get(url,headers=Headers)
#     soup = BeautifulSoup(res.text, 'html.parser')
#
#     a_href = soup.find_all('a',href=True)
#
#     if debug:
#         print(url)
#
#     foundItem1 = False
#     foundItem1b = False
#     foundItem1a = False
#     foundItem2 = False
#     foundItem3 = False
#     foundItem4 = False
#     foundItem5 = False
#     foundItem6 = False
#     foundItem7 = False
#     foundItem7a = False
#     foundItem8 = False
#
#     item1 = {}
#     item1b = {}
#     item1a = {}
#     item2 = {}
#     item3 = {}
#     item4 = {}
#     item5 = {}
#     item6 = {}
#     item7 = {}
#     item7a = {}
#     item8 = {}
#
#
#     for i in a_href:
#         fullstring = i.text.lower()
#         fullstring = fullstring.replace("\n","")
#
#         if (foundItem1 == False) and CheckSection1Label(fullstring,debug=debug):
#             foundItem1 = True
#
#             #item1 = i.attrs.copy()
#             item1 = i.text
#
#             if debug:
#                 print("Item 1")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem1a == False) and CheckSection1ALabel(fullstring,debug=debug):
#
#             foundItem1a = True
#
#             #item1a = i.attrs.copy()
#             item1a = i.text
#
#             if debug:
#                 print("Item 1A")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem1b == False) and CheckSection1BLabel(fullstring,debug=debug):
#             foundItem1b = True
#
#             #item1b = i.attrs.copy()
#             item1b = i.text
#
#             if debug:
#                 print("Item 1B")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem2 == False) and CheckSection2Label(fullstring,debug=debug):
#
#             foundItem2 = True
#
#             #item2 = i.attrs.copy()
#             item2 = i.text
#
#             if debug:
#                 print("Item 2")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem3 == False) and CheckSection3Label(fullstring,debug=debug):
#
#             foundItem3 = True
#
#             #item3 = i.attrs.copy()
#             item3 = i.text
#
#             if debug:
#                 print("Item 3")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem4 == False) and CheckSection4Label(fullstring,debug=debug):
#
#             foundItem4 = True
#
#             #item4 = i.attrs.copy()
#             item4 = i.text
#
#             if debug:
#                 print("Item 4")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem5 == False) and CheckSection5Label(fullstring,debug=debug):
#
#             foundItem5 = True
#
#             #item5 = i.attrs.copy()
#             item5 = i.text
#
#             if debug:
#                 print("Item 5")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem6 == False) and CheckSection6Label(fullstring,debug=debug):
#
#             foundItem6 = True
#
#             #item6 = i.attrs.copy()
#             item6 = i.text
#
#             if debug:
#                 print("Item 6")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem7 == False) and CheckSection7Label(fullstring,debug=debug):
#
#             foundItem7 = True
#
#             #item7 = i.attrs.copy()
#             item7 = i.text
#
#             if debug:
#                 print("Item 7")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem7a == False) and CheckSection7ALabel(fullstring,debug=debug):
#
#             foundItem7a = True
#
#             #item7a = i.attrs.copy()
#             item7a = i.text
#
#             if debug:
#                 print("Item 7A")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem8 == False) and CheckSection8Label(fullstring,debug=debug):
#
#             foundItem8 = True
#
#             #item8 = i.attrs.copy()
#             item8 = i.text
#
#             if debug:
#                 print("Item 8")
#                 print(i.attrs)
#                 print(fullstring)
#
#
#
#     results = {}
#
#     results["1"] = item1
#     results["1A"] = item1a
#     results["1B"] = item1b
#     results["2"] = item2
#     results["3"] = item3
#     results["4"] = item4
#     results["5"] = item5
#     results["6"] = item6
#     results["7"] = item7
#     results["7A"] = item7a
#     results["8"] = item8
#     return results
#
# def ExtractText(main_text, start, end , debug = False):
#
#     s = (main_text.find('"{}"'.format(start)))
#     e = (main_text.find('"{}"'.format(end)))
#
#     s , e = min(s,e) , max(s,e)
#
#     if debug:
#         print( "The text starts at : {} and ends at : {}".format(s,e))
#
#     text = main_text[s:e]
#
#     # some_iteration = BeautifulSoup(text,'html.parser')
#
#     return text
#
# def ExtractItem1A(url, companyname, debug=False):
#     res = requests.get(url, headers=Headers)
#
#     soup = BeautifulSoup(res.text, 'html.parser')
#
#     main_text = res.text
#
#     # print(main_text)
#
#     a_href = soup.find_all('a', href=True)
#
#     if debug:
#         print(url)
#
#     foundItem1a = False
#     foundItem1b = False
#     foundItem2 = False
#
#     item1a = {}
#     item1b = {}
#     item2 = {}
#
#     for i in a_href:
#
#         fullstring = i.text.lower()
#         fullstring = fullstring.replace("\n", "")
#
#         if (foundItem1a == False) and CheckSection1ALabel(fullstring,debug=debug):
#
#             foundItem1a = True
#
#             item1a = i.attrs.copy()
#
#             if debug:
#                 print("Item 1A")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem1b == False) and CheckSection1BLabel(fullstring,debug=debug):
#             foundItem1b = True
#
#             item1b = i.attrs.copy()
#
#             if debug:
#                 print("Item 1B")
#                 print(i.attrs)
#                 print(fullstring)
#
#         if (foundItem2 == False) and CheckSection2Label(fullstring,debug=debug):
#
#             foundItem2 = True
#
#             item2 = i.attrs.copy()
#
#             if debug:
#                 print("Item 2")
#                 print(i.attrs)
#                 print(fullstring)
#
#     data = []
#
#     text = ""
#
#     some_iteration = None
#
#     if debug:
#         print("Item 1A Status: {}".format(foundItem1a))
#         print("Item 1B Status: {}".format(foundItem1b))
#         print("Item 2 Status: {}".format(foundItem2))
#
#     if foundItem1a:
#         item1AID = item1a['href'][1:]
#         if debug:
#             print("Item 1A href id/name : {}".format(item1AID))
#
#         if foundItem1b:
#
#             item1BID = item1b['href'][1:]
#
#             if debug:
#                 print("Item 1B href id/name : {}".format(item1BID))
#
#             startID1 = soup.find("a", {"name": item1AID})
#             startID2 = soup.find(id=item1a['href'][1:])
#
#             if (startID1 != None):
#
#                 endID1 = soup.find("a", {"name": item1BID})
#
#                 if debug:
#                     print("Start ID1(name) : {}".format(startID1))
#
#                 if debug:
#                     print("End ID1(name) : {}".format(endID1))
#
#                 text = ExtractText(main_text, item1AID, item1BID, debug)
#
#             if (startID2 != None):
#
#                 endID2 = soup.find(id=item1b['href'][1:])
#
#                 if debug:
#                     print("Start ID2(name) : {}".format(startID2))
#
#                 if debug:
#                     print("End ID2(name) : {}".format(endID2))
#
#                 text = ExtractText(main_text, item1AID, item1BID, debug)
#
#         else:
#
#             item2ID = item2['href'][1:]
#
#             if debug:
#                 print("Item 2 href id/name : {}".format(item2ID))
#
#             startID1 = soup.find("a", {"name": item1AID})
#             startID2 = soup.find(id=item1a['href'][1:])
#
#             if (startID1 != None):
#
#                 endID1 = soup.find("a", {"name": item2ID})
#
#                 if debug:
#                     print("Start ID1(name) : {}".format(startID1))
#
#                 if debug:
#                     print("End ID1(name) : {}".format(endID1))
#
#                 text = ExtractText(main_text, item1AID, item2ID, debug)
#
#             if (startID2 != None):
#
#                 endID2 = soup.find(id=item2['href'][1:])
#
#                 if debug:
#                     print("Start ID2(name) : {}".format(startID2))
#
#                 if debug:
#                     print("End ID2(name) : {}".format(endID2))
#
#                 text = ExtractText(main_text, item1AID, item2ID, debug)
#
#     return item1a, item1b, item2, text