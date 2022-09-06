from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import requests
from pathlib import Path

def ScrapeCurrencyExchange():
    url = "https://countryeconomy.com/currencies"
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    table = html.find("table", id="tb0_287")

    Path("./Output").mkdir(parents=True, exist_ok=True)

    with open("Output/Euro_Currency_Exchange.csv", "w", encoding="utf-8") as f:
        # headers
        thead = table.find("thead")
        col_names = thead.find_all("th")
        headers = "Country"
        for col_name in col_names:
            header = col_name.text
            headers += header.strip() + ","
        # print(headers)
        f.write(headers + "\n")

        # data
        rows = table.find_all("tr")
        country_links = []

        for row in rows:
            tds = row.find_all("td")
            if len(tds) == 0:
                continue

            row_text = ""
            for i in range(len(tds) - 1):
                td = tds[i]
                cell = ""
                if i == 0:
                    index = td.text.index(" [+]")
                    cell = td.text[0:index] + ", "
                    a = td.find("a", href=True)
                    if a != NULL:
                        country_links.append(a["href"])
                elif i == 5:
                    cell = td.get("data-value") + "\n"
                else:
                    cell = td.get("data-value") + ", "

                row_text += cell          
            f.write(row_text)

def main():
    ScrapeCurrencyExchange()

if __name__ == "__main__":
    main()
