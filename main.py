from utils import create_html, BanksParser
import os


def main():
    if "html.txt" not in os.listdir():
        create_html("html.txt")
    parser = BanksParser()
    with open("html.txt", "r") as file:
        src = file.read()
    parser.get_data(src)
    parser.save_to_csv("data.csv")
    parser.save_to_json("data.json")


if __name__ == "__main__":
    main()
