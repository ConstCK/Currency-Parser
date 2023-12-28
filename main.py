from utils import BanksParser
import os


def main():
    parser = BanksParser()
    if "html.txt" not in os.listdir():
        parser.create_html("html.txt")
    with open("html.txt", "r") as file:
        src = file.read()
    parser.get_data(src)
    parser.save_to_csv("data.csv")
    parser.save_to_json("data.json")
    print(parser)


if __name__ == "__main__":
    main()
