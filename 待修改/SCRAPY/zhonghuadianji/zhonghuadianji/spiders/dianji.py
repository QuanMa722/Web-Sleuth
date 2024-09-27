# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import scrapy
import time
import re

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


class DianjiSpider(scrapy.Spider):
    name = "dianji"
    allowed_domains = ["www.zhonghuadiancang.com"]

    def start_requests(self):
        for index in range(18603, 18683):
            url = f"https://www.zhonghuadiancang.com/lishizhuanji/mingshijishibenmo/{index}.html"
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        index = re.search(r"/(\d+)\.html$", response.url).group(1)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').get_text().strip()
        text = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()

        # 将抓取到的数据打印出来
        # self.log(f"Index: {index}, Title: {title}")  # 只打印文本的前30个字符

        # 可以选择将数据保存到 Item 中
        # yield {
        #     'index': index,
        #     'title': title,
        #     'text': text
        # }

    def close(self, reason):
        total_time = time.time() - self.start_time
        self.log(f"Total running time: {total_time:.2f} seconds")

    def __init__(self, *args, **kwargs):
        super(DianjiSpider, self).__init__(*args, **kwargs)
        self.start_time = time.time()
