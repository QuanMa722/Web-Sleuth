# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import requests
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def fetch(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        response.raise_for_status()
        resp_text = response.text
        logging.info(f"Fetched {url}, status code {response.status_code}")
        parse(resp_text)
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")


def parse(resp_text):
    text = resp_text
    pipeline(text)


def pipeline(text):
    with open('output.txt', mode='a', encoding='utf-8') as f:
        f.write(text + '\n')


def main():
    url_list = ['https://www.baidu.com/'] * 10

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: fetch(url), url_list)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except FileExistsError as error:
        logging.error(f"An error occurred: {error}.")
