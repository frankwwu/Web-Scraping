from bs4 import BeautifulSoup
import urllib.request
import os
import re
import json
from jsonpath_ng import jsonpath, parse
from pathlib import Path
from time import sleep
import numpy as np

def GetJsonData(body, print_json = False):
    pattern = re.compile(r'^window', re.MULTILINE | re.DOTALL)
    script = body.find('script', {"type": None}, text = pattern)
   
    # Get raw unicode json string
    json_re = re.compile(r"window\[\"initialData\"] = JSON\.parse\(\"(.*)\"\);window\[\"tags\"]")
    raw_data = ""
    for script in body.find_all('script'):
        if "initialData" in script.text:
            res_text = script.get_text(strip = True)
            raw_data = json_re.search(res_text).group(1)
            break
  
    #print(raw_data)

    # Convert unicode json string to json
    t1 = raw_data.encode("utf-8")  
    t2 = t1.decode("unicode-escape")   
    t3 = json.loads(t2)  
    json_dump = json.dumps(t3, indent = 4)
    if print_json == True:
        print(json_dump)

    json_data = json.loads(json_dump)
    return json_data

def ScrapeFile(url): 
    Path("./Output").mkdir(parents = True, exist_ok = True)
    with open(url, "r", encoding = "utf8") as f:
        doc = BeautifulSoup(f, "html.parser")

    body = doc.find('body')      
    json_data = GetJsonData(body, print_json = False)
    n = parse('cards[*].list[*]') 

    for match in n.find(json_data):       
        if match.value["cardType"] == "classified":                  
            for photo in match.value["photos"]:
                print(f'photo: {photo}')
                # download photo
                sleep(np.random.uniform(0.5, 1.6))
                head, tail = os.path.split(photo)
                output = "./Output/" + tail
                urllib.request.urlretrieve(photo, output)
            print(f'title: {match.value["title"]}')
            print(f'estateType: {match.value["estateType"]}')
            print(f'rawPrice: {match.value["pricing"]["rawPrice"]}')
            print(f'contactName: {match.value["contact"]["contactName"]}')
            print(f'phoneNumber: {match.value["contact"]["phoneNumber"]}')
            print(f'agencyLink: {match.value["contact"]["agencyLink"]}')
            print(f'tags: {match.value["tags"]}')
            print(f'cityLabel: {match.value["cityLabel"]}')
            print(f'zipCode: {match.value["zipCode"]}')           
            print(f'rooms: {match.value["rooms"]}')
            print(f'surface: {match.value["surface"]}')
            print(f'description: {match.value["description"]}')
            print()
 
def main():    
    ScrapeFile("Input/seloger.html")  

if __name__ == "__main__":
    main()