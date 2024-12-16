# -*- coding: utf-8 -*-

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
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

service = Service(EdgeChromiumDriverManager().install())
options = webdriver.EdgeOptions()
options.add_argument('--headless')


class GetPatentID:

    def __init__(self, topic):
        self.topic = topic

        self.years = [
            2019, 2020, 2021
                      ]

        self.months = [
            '01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12',
        ]

    def fetch(self):


        for year in self.years:

            for index in range(0, 12):

                with webdriver.Edge(service=service, options=options) as driver:

                    base_url = f'https://patents.google.com/?assignee=Contemporary+Amperex+Technology&before=priority:{year}{self.months[index]}31&after=priority:{year}{self.months[index]}01&patents=false&page='

                    for page in range(0, 35):
                        url = f'{base_url}{page}'
                        driver.get(url)

                        try:
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-proto="OPEN_PATENT_PDF"]'))
                            )

                        except Exception as e:
                            logging.error(f"Error loading page {page}: {e}")
                            with open('Failed.txt', mode='a', encoding='utf-8') as f:
                                failed_str = str(year) + str(index + 1) + str(page)
                                f.write(failed_str + '\n')
                            break

                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')

                        span_tags = soup.findAll('span',
                                                 {'data-proto': 'OPEN_PATENT_PDF',
                                                  'class': 'style-scope search-result-item'})

                        logging.info(span_tags)

                        if span_tags:

                            for span in span_tags:
                                patent_id = span.get_text(strip=True)
                                logging.info(patent_id)

                                with open(f'{year}_{index + 1}.txt', mode='a', encoding='utf-8') as f:
                                    f.write(patent_id + '\n')

                            logging.info('-' * 5 + str(page + 1) + '-' * 5)

                            time.sleep(1)

                        else:
                            break


if __name__ == '__main__':

    test_topic = 'Contemporary Amperex Technology'
    patentID = GetPatentID(test_topic)
    patentID.fetch()
