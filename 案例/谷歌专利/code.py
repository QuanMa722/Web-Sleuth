# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
import patent_stil
import requests
import logging
import time
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)


def fetch(patent):
    try:
        response = patent_stil.getGooglePatentInfo(patent)
        patent_data = {key: value for key, value in vars(response).items() if not callable(value)}
        logging.info(f"Fetched {patent}")
        pipeline(patent, patent_data)

    except requests.RequestException as e:
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(patent + '\n')
        logging.error(f"Error fetching {patent}: {e}")


def pipeline(patent, patent_data):
    os.makedirs('PatentData', exist_ok=True)
    with open(f'PatentData/{patent}.json', 'w', encoding='utf-8') as output_file:
        json.dump(patent_data, output_file, ensure_ascii=False, indent=4)


def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch, patents)


if __name__ == '__main__':

    with open('PatentID.txt', mode='r', encoding='utf-8') as f:
        patents: list[str] = [line.strip() for line in f.readlines() if line.strip()][:100] # test

    start_time = time.time()
    try:
        main()
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")

    except Exception as error:
        logging.error(f"An error occurred during execution: {error}.")
