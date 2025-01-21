# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.parse
import requests
import logging
import random
import time
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def get_url(year, month):

    os.makedirs(f'{year}', exist_ok=True)
    file_path = f'{year}/{year}{month:02d}.txt'

    with open(file_path, 'a', encoding='utf-8') as file:

        for page in range(1, 11):
            url = f'http://mrxwlb.com/{year}/{month}/page/{page}'
            response = requests.get(url, headers=headers)

            time.sleep(random.uniform(3, 5))

            if response.status_code == 200:
                logging.info(f"Scraping: {url}")
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('h1', class_='entry-title')

                for link in links:
                    a_tag = link.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        href = a_tag['href']
                        decoded_url = urllib.parse.unquote(href)
                        logging.info(decoded_url)
                        file.write(decoded_url + '\n')

            else:
                break


if __name__ == '__main__':

    logging.info('Start fetching')
    start_time = time.time()

    # for year in range(2016, 2025):
    #     for month in range(1, 13):
    #         get_url(year, month)

    # get_url(2015, 12)
    # get_url(2025, 1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f'Finished fetching. Total time taken: {elapsed_time:.2f} seconds')
