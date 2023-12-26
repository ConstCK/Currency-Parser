import requests
from bs4 import BeautifulSoup
import csv
import json

URL = 'https://krasnodar.bankiros.ru/currency/sochi'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def create_html(f: str):
    with open(f, "w+") as file:
        page = requests.get(URL, headers=HEADERS)
        file.write(page.text)


class BanksParser:
    def __init__(self) -> None:
        self.banks: list = list()
        self.best_usd_buy: float = None
        self.best_usd_self: float = None
        self.best_euro_buy: float = None
        self.best_euro_sell: float = None

    def get_data(self, data: str) -> None:
        soup = BeautifulSoup(data, "lxml")
        data: list = soup.find_all("div", class_="xxx-tbl-row")
        for element in data:
            try:
                name = element.find(
                    "div", class_="xxx-tbl-cell--full").find("a").find("span").text
                usd_buy = element.find_all(
                    class_="xxx-tbl-cell")[1].find_all(class_="xxx-df")[0].find("span").text
                usd_sell = element.find_all(
                    class_="xxx-tbl-cell")[1].find_all(class_="xxx-df")[1].find("span").text
                euro_buy = element.find_all(
                    class_="xxx-tbl-cell")[2].find_all(class_="xxx-df")[0].find("span").text
                euro_sell = element.find_all(
                    class_="xxx-tbl-cell")[2].find_all(class_="xxx-df")[1].find("span").text
                self.banks.append({"name": name, "usd_buy": usd_buy, "usd_sell": usd_sell,
                                   "euro_buy": euro_buy, "euro_sell": euro_sell})

            except AttributeError:
                continue

    def save_to_csv(self, f: str):
        with open(f, "w") as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'usd_buy',
                                                      'usd_sell', 'euro_buy', 'euro_sell'])
            writer.writeheader()
            for element in self.banks:
                writer.writerow(element)

    def save_to_json(self, f: str):
        with open(f, "w") as file:
            json.dump(self.banks, file, ensure_ascii=False)
