# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import patent_stil
import requests
import logging
import time
import json
import os

# 设置日志
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

# 定义字段列表
fields = [
    'abstract', 'application_number', 'assignee', 'attorney_agent_or_firm',
    'claims', 'descriptions', 'field_of_search', 'filing_date',
    'international_classes', 'inventors', 'other_classes', 'other_references',
    'pdf_url', 'primary_class', 'primary_examiner', 'pub_num',
    'publication_date', 'title', 'url', 'us_patent_references',
    'view_patent_images'
]


def fetch(patent):
    try:
        resp = patent_stil.getGooglePatentInfo(patent)
        patent_data = vars(resp)
        patent_data = {key: value for key, value in patent_data.items() if not callable(value)}
        logging.info(f"Fetched {patent}")
        pipeline(patent, patent_data)

    except requests.RequestException as e:
        logging.error(f"Error fetching {patent}: {e}")


def pipeline(patent, patent_data):
    os.makedirs('PatentData')

    try:
        with open(f'PatentData/{patent}.json', 'w', encoding='utf-8') as output_file:
            json.dump(patent_data, output_file, ensure_ascii=False, indent=4)
    except IOError as e:
        logging.error(f"Error saving patent data for {patent}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while saving data for {patent}: {e}")


def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch, patents)


if __name__ == '__main__':

    with open('PatentID.txt', mode='r', encoding='utf-8') as f:
        patents = [line.strip() for line in f.readlines() if line.strip()]

    start_time = time.time()

    try:
        main()
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")

    except Exception as error:
        logging.error(f"An error occurred during execution: {error}.")
