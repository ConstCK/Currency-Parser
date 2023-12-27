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
        page.encoding = "utf-8"
        file.write(page.text)


class BanksParser:
    def __init__(self) -> None:
        self.banks: list = list()
        self.best_usd_buy: str = ""
        self.best_usd_sell: str = ""
        self.best_euro_buy: str = ""
        self.best_euro_sell: str = ""

    def get_data(self, data: str) -> None:
        soup = BeautifulSoup(data, "lxml")
        data: list = soup.find_all("div", class_="xxx-tbl-row__grid")
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
                self.banks.append({"name": name.strip(), "usd_buy": float(usd_buy), "usd_sell": float(usd_sell),
                                   "euro_buy": float(euro_buy), "euro_sell": float(euro_sell), })

            except AttributeError:
                continue

    def save_to_csv(self, f: str) -> None:
        self.get_best_rate()
        with open(f, "w") as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'usd_buy',
                                                      'usd_sell', 'euro_buy', 'euro_sell'])
            writer.writeheader()
            for element in self.banks:
                writer.writerow(element)


    def save_to_json(self, f: str) -> None:
        with open(f, "w") as file:
            json.dump(self.banks, file, ensure_ascii=False)

    def get_best_rate(self) -> None:
        best_usd_buy = sorted(
            self.banks, key=lambda x: x["usd_buy"], reverse=True)[0]
        best_usd_sell = sorted(self.banks, key=lambda x: x["usd_sell"])[0]
        best_euro_buy = sorted(
            self.banks, key=lambda x: x["euro_buy"], reverse=True)[0]
        best_euro_sell = sorted(self.banks, key=lambda x: x["euro_sell"])[0]
        self.best_usd_buy: str = f"Лучший банк для продажи долларов - {best_usd_buy['name']} с курсом {best_usd_buy['usd_buy']} руб."
        self.best_usd_sell: str = f"Лучший банк для покупки долларов - {best_usd_sell['name']} с курсом {best_usd_sell['usd_sell']} руб."
        self.best_euro_buy: str = f"Лучший банк для продажи евро - {best_euro_buy['name']} с курсом {best_euro_buy['euro_buy']} руб."
        self.best_euro_sell: str = f"Лучший банк для покупки евро - {best_euro_sell['name']} с курсом {best_euro_sell['euro_sell']} руб."
