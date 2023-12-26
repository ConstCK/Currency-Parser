import requests
URL = 'https://krasnodar.bankiros.ru/currency/sochi'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def create_html():
    with open('html.txt', "w+") as file:
        page = requests.get(URL, headers=HEADERS)
        file.write(page.text)


class BanksParser:
    def __init__(self) -> None:
        self.banks: list = list()
        self.best_usd_buy = None
        self.best_usd_self = None
        self.best_euro_buy = None
        self.best_euro_sell = None
