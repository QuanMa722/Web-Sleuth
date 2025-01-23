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
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)


def fetch(url):
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }

        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        response.raise_for_status()
        resp_text = response.text
        logging.info(f"Successfully fetched {url}, status code {response.status_code}")
        parse(resp_text)

    except Exception as e:
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{url}\n')
        logging.error(f"Error fetching {url}: {e}")


def parse(resp_text):
    text = resp_text
    pipeline(text)


def pipeline(text):
    with open('output.txt', mode='w', encoding='utf-8') as f:
        f.write(text + '\n')


def task():
    url_list = ['https://www.baidu.com/'] * 100
    return url_list


def main():
    url_list = task()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: fetch(url), url_list)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
        print(f"Total time: {round((time.time() - start_time), 2)}s")

    except Exception as error:
        logging.error(f"An error occurred: {error}.")
