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

# Setting up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

# 设置 EdgeDriver
service = Service(EdgeChromiumDriverManager().install())
options = webdriver.EdgeOptions()
options.add_argument('--headless')  # 启用无头模式


class GetPatentID:

    def __init__(self, topic):
        self.topic = topic
        self.patent_ids = []

    def fetch(self):
        # 使用无头浏览器
        with webdriver.Edge(service=service, options=options) as driver:
            base_url = f'https://patents.google.com/?assignee={self.topic}&oq={self.topic}&page='

            # 遍历多个页面
            for page in range(0, 10):
                url = f'{base_url}{page}'
                driver.get(url)

                # 使用 WebDriverWait 等待页面加载完成
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-proto="OPEN_PATENT_PDF"]'))
                    )

                except Exception as e:
                    logging.error(f"Error loading page {page}: {e}")
                    self.log_failed_page(page)
                    continue

                # 解析页面
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # 查找所有包含 patent ID 的 span 标签
                span_tags = soup.findAll('span',
                                         {'data-proto': 'OPEN_PATENT_PDF', 'class': 'style-scope search-result-item'})

                # 提取 patent_id
                for span in span_tags:
                    patent_id = span.get_text(strip=True)
                    self.patent_ids.append(patent_id)
                    logging.info(patent_id)

                logging.info('-' * 5 + str(page + 1) + '-' * 5)

                # 防止频繁请求被封禁，适当休眠
                time.sleep(1)

        # 写入文件
        self.save_patent_ids()

    def save_patent_ids(self):
        """将所有提取到的专利ID保存到文件"""
        with open('PatentID.txt', mode='a', encoding='utf-8') as f:
            for patent_id in self.patent_ids:
                f.write(patent_id + '\n')

    @staticmethod
    def log_failed_page(page):
        """记录加载失败的页面"""
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{page}\n')


if __name__ == '__main__':

    test_topic = 'Contemporary Amperex Technology'
    patentID = GetPatentID(test_topic)
    patentID.fetch()
