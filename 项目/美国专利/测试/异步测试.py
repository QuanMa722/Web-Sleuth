# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import time


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime(int(time.time())))
    msgs = msg.split("\n")
    for word in msgs:
        print("[" + nowt + "] " + str(word))


def fetch_patent_title(url):
    """
    从指定的专利 URL 中提取专利名
    :param url: 专利 URL
    :return: 专利名或 None（如果请求失败）
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        patent_title = soup.find(itemprop="title")

        return patent_title.text.strip()

    except requests.RequestException as e:
        printt(f'请求失败: {e}')
        return None


if __name__ == "__main__":

    url = 'https://patents.google.com/patent/US11883499B2'
    count_list = []

    for attempt in range(10):
        for num in range(1, 51):
            printt(f'第 {num} 次请求')
            title = fetch_patent_title(url)

            if title:
                printt("专利名称: " + title)
                if num == 50:
                    count_list.append(50)
                else:
                    pass
            else:
                count_list.append(num)
                break

        time.sleep(60)  # 每轮尝试后的间隔时间

    if count_list:
        printt(f'尝试列表: {count_list}')
        printt(f'最小请求成功次数: {min(count_list)}')

    else:
        printt('没有成功的请求次数记录')
