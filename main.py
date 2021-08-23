import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver
import time


def get_price(title):
    load_dotenv()
    options = webdriver.ChromeOptions()
    options.add_argument(
        'general.useragent.override=Chrome/47.0.2526.111 Safari/537.36')
    title = quote(title)
    url = f'https://edadeal.ru/perm/offers?search={title}&title={title}'
    try:
        executable_path = os.getenv('EXECUTABLE_PATH')
        driver = webdriver.Chrome(
            executable_path=executable_path,
            options=options)
        driver.get(url=url)
        time.sleep(2)

        with open('index_selenium.html', 'w') as file:
            file.write(driver.page_source)

        with open('index_selenium.html') as file:
            src = file.read()

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    soup = BeautifulSoup(src, 'lxml')
    prices = soup.find_all(
        'div', class_='b-offer__price-new b-offer__rub_true')
    prices_list = []
    for price in prices:
        current_price = price.text.replace('\xa0', '')
        prices_list.append(current_price)
    prices_list.sort()
    return prices_list[round(len(prices_list) / 2)]


def main():
    title = 'мясо'
    print(get_price(title))


if __name__ == '__main__':
    main()
