from bs4 import BeautifulSoup
import requests
from pathlib import Path
import xml.etree.cElementTree as xml

filter_1 = "If we look at the minimum salary in "
filter_2 = "Accordingly the national minimum wage has been raised"


def __GetCurrency(country_html):
    ele = country_html.find("article")
    if ele != None:
        ele = ele.find("article")
        if ele != None:
            ele = ele.find("div")
            if ele != None:
                ele = ele.find_all("p")

    currency = ""
    if ele != None:
        p1 = ele[1]
        t = p1.text

        if t.find(filter_1) == True:
            end = t.index(",")
            if end != None:
                length = len(filter_1)
                currency = t[length + 1 : end].strip()
            # else:
            #    currency = "[Can't find in text]"
        elif t.find(filter_2) == True:
            currency = "Euros"
        # else:
        #    currency = "[No text]"
    return currency


def __GetHeaders(table):
    tablethead = table.find("tr")
    col_names = tablethead.find_all("th")

    headers = []
    for cn in range(len(col_names)):
        col_name = col_names[cn]
        header = col_name.text
        header = header.replace(" ", "")

        if cn == 2:
            header = f"USD_{header}"
        elif cn == 3:
            header = f"EURO_{header}"

        headers.append(header.replace(".", "_"))

    return headers


def __ScrapeCountries(country_url, root):
    length = len(country_url)
    s = country_url.rindex("/", 1)
    start = -length + s + 1

    country_page = requests.get(country_url)
    country_html = BeautifulSoup(country_page.text, "html.parser")
    table = country_html.find("table", id="tb0")

    # National currency
    currency = __GetCurrency(country_html)

    # headers
    headers = __GetHeaders(table)

    # data
    rows = table.find_all("tr")

    for row in rows:
        tds = row.find_all("td")
        if len(tds) == 0:
            continue

        row_text = ""
        wage = xml.Element("wage")
        root.append(wage)
        wage.set("Country", country_url[start:])
        for i in range(len(tds)):
            td = tds[i]
            value = td.get("data-value")
            cell = value + ", "
            row_text += cell
            if len(value) > 0:
                wage.set(headers[i], td.get("data-value"))

        row_text += currency + ", "
        row_text += country_url
        wage.set("National_Currency", currency)
        wage.set("URL", country_url)

    print(country_url[start:])


def ScrapePages():
    url = "https://countryeconomy.com/national-minimum-wage"
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    table = html.find("table", id="tb1")

    rows = table.find_all("tr")

    index = url.index("/national-minimum-wage")
    base_url = url[0:index]

    root = xml.Element("root")
    for row in rows:
        td = row.find("td")
        if td == None:
            continue

        a = td.find("a", href=True)
        if a != None:
            country_path = a["href"]
            country_url = base_url + country_path
            __ScrapeCountries(country_url, root)

    tree = xml.ElementTree(root)
    xml.indent(tree, space="\t", level=0)
    root_node = tree.getroot()
    xmlstr = xml.tostring(
        root_node, encoding="utf8", method="xml", xml_declaration=None
    ).decode()
    # xmlstr = xmlstr[len("<?xml version='1.0' encoding='utf8'?>"):]

    with open("./Output/minimum-wages-string.xml", "w") as f:
        f.write(xmlstr)
        f.close()

    tree = xml.ElementTree(root)
    xml.indent(tree, space="\t", level=0)
    tree.write("./Output/minimum-wages-tree.xml", encoding="utf-8")


def main():
    ScrapePages()


if __name__ == "__main__":
    main()
