from utils import create_html
import os


def main():
    if "html.txt" not in os.listdir():
        create_html()


if __name__ == "__main__":
    main()
