from bs4 import BeautifulSoup
import requests
from pathlib import Path


def __ScrapeCountries(base_url, country_paths):
    for path in country_paths:
        length = len(path)
        s = path.index("/", 1)
        start = -length + s + 1
        file_name = path[start:] + ".csv"
        print(file_name)

        country_page = requests.get(base_url + path)
        country_html = BeautifulSoup(country_page.text, "html.parser")
        table = country_html.find("table", id="tb0")

        with open("./Output/" + file_name, "w", encoding="utf-8") as f:
            # headers
            tablethead = table.find("tr")
            col_names = tablethead.find_all("th")
            headers = ""
            for cn in range(len(col_names)):
                col_name = col_names[cn]
                header = col_name.text
                header = header.replace(" ", "")

                if cn == 2:
                    header += "_USD"
                elif cn == 3:
                    header += "_EURO"

                headers += header + ","
            f.write(headers + "\n")

            # data
            rows = table.find_all("tr")

            for row in rows:
                tds = row.find_all("td")
                if len(tds) == 0:
                    continue

                row_text = ""

                for i in range(len(tds)):
                    td = tds[i]
                    cell = td.get("data-value") + ", "
                    row_text += cell

                # print(row_text)
                f.write(row_text + "\n")


def ScrapePages():
    url = "https://countryeconomy.com/national-minimum-wage"
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    table = html.find("table", id="tb1")

    Path("./Output").mkdir(parents=True, exist_ok=True)

    with open("Output/National_Minimum_Wages.csv", "w", encoding="utf-8") as f:
        # headers
        thead = table.find("thead")
        col_names = thead.find_all("th")
        headers = ""
        for cn in range(len(col_names)):
            col_name = col_names[cn]
            header = col_name.text
            if cn == 2:
                header += "_USD"
            elif cn == 3:
                header += "_EURO"

            if header.startswith("Nat. Curr.  NMW"):
                header = header.replace(".", ",")

            headers += header + ","
        # print(headers)
        f.write(headers + "\n")

        # data
        rows = table.find_all("tr")
        country_paths = []

        for row in rows:
            tds = row.find_all("td")
            row_text = ""
            for i in range(len(tds)):
                td = tds[i]
                cell = ""
                if i == 0:
                    index = td.text.index(" [+]")
                    cell = td.text[0:index] + ", "
                    a = td.find("a", href=True)
                    if a != None:
                        country_paths.append(a["href"])
                elif i in [1, 2, 4, 5]:
                    cell = td.get("data-value") + ", "
                elif i == 3:  # $
                    cell = td.text + ", "
                elif i == 6:
                    cell = td.text + ", "
                elif i == 7:
                    cell = td.get("data-value") + "\n"

                row_text += cell

            # print(row_text)
            f.write(row_text)

    # country_links
    index = url.index("/national-minimum-wage")
    base_url = url[0:index]
    __ScrapeCountries(base_url, country_paths)


def main():
    ScrapePages()


if __name__ == "__main__":
    main()
