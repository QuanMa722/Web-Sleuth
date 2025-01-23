# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import logging
import time
import re

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
        response.raise_for_status()
        resp_text = response.text
        parse(resp_text)
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


def parse(resp_text):
    url = 'https://cn.nytimes.com'
    soup = BeautifulSoup(resp_text, 'html.parser')
    h3_tags = soup.find_all('h3')
    if h3_tags:
        for h3_tag in h3_tags:
            news_dict = {}
            title = h3_tag.get_text()
            link = h3_tag.find('a')['href'] if h3_tag.find('a') else None

            try:
                if link and link.startswith('/'):
                    link = url + link
                if link and 'slideshow' not in link:
                    pattern = r"/([^/]+)/([0-9]{8})/"
                    matches = re.findall(pattern, link)
                    kind = matches[0][0]
                    date = matches[0][1]

                    news_dict['title'] = title
                    news_dict['link'] = link
                    news_dict['kind'] = kind
                    news_dict['date'] = date

                    logging.info(f'Title: {title} Link: {link} Kind: {kind} Date: {date}')
                    pipline(news_dict)

            except Exception as e:
                with open('error.txt', mode='a', encoding='utf-8') as f:
                    f.write(link + '\n')
    else:
        logging.error('Specified label not found')


def pipline(news_dict):
    with open('news.txt', mode='a', encoding='utf-8') as f:
        f.write(str(news_dict) + '\n')


def main():
    kind_list = [
        'asia-pacific', 'south-asia', 'usa', 'americas', 'europe', 'mideas', 'africa',
        'policy', 'china-ec', 'dealbook',
        'lens',
        'bits', 'personal-tech',
        'science',
        'health',
        'education',
        'books', 'art', 'film-tv', 'sports',
        'fashion', 'food-wine', 'lifestyle',
        'travel',
        'real-estate',
        'op-column', 'op-ed', 'cartoon',
    ]

    url_list = [f'https://cn.nytimes.com/{kind}' for kind in kind_list]

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetch, url_list)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except Exception as error:
        logging.error(f"An error occurred: {error}.")
