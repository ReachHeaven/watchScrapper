import csv
import json
from datetime import datetime
from bs4 import BeautifulSoup
import lxml
import requests
import os


def get_data():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    current_data = datetime.now().strftime("%d_%m_%y")

    with open(f"data/data_{current_data}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            (
                "Article",
                "Price"
            )
        )

    url = "https://shop.casio.ru/catalog/g-shock/"

    req = requests.get(url, headers=headers)
    # print(req.text)

    if not os.path.exists("data"):
        os.mkdir("data")

    with open("data/page_1.html", "w") as f:
        f.write(req.text)


    with open("data/page_1.html") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    tmp = soup.find_all("a", class_="product-item__link")
    data = []
    for item in tmp:
        product_article = item.find("p", class_="product-item__articul").text.strip()
        product_link = "https://shop.casio.ru/" + item.get("href")
        data.append(
            {"product_article": product_article,
             "product_link": product_link}
        )

        with open(f"data/data_{current_data}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(
                (
                    product_article,
                    product_link
                )
            )

    with open(f"data_{current_data}.json", "a") as f:
        json.dump(data, f, indent=4)


def main():
    get_data()


if __name__ == '__main__':
    main()