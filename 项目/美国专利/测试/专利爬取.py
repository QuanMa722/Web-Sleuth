# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import csv

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def get_content(url):
    response = requests.get(url, headers=headers, timeout=20)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    patent_title: str = soup.find(itemprop="title").text.strip()

    pub_num: str = soup.find(itemprop="publicationNumber").text

    abstract: str = soup.find(class_="abstract").text

    # 提取所有 img 标签的 src 属性，并将其存储在一个列表中
    img_list = [img['src'] for img in soup.find_all(itemprop="thumbnail")]

    inventor: list[str] = [i.get_text(strip=True) for i in soup.find_all(itemprop="inventor")]

    current_assignee: list[str] = [i.get_text(strip=True) for i in soup.find_all(itemprop="assigneeCurrent")]

    events_dict = {}
    for i in range(1, 30):
        event = soup.find_all(itemprop="title")[i].text.strip()
        time = soup.find_all(itemprop="date")[i].text.strip()

        if event:
            if event == 'Anticipated expiration' or event == 'Adjusted expiration':
                events_dict[time] = event
                break
            events_dict[time] = event
        else:
            break

    # 提取 'Code' 属性的文本并将其转为列表
    classifications_code: list[str] = [i.get_text(strip=True) for i in soup.find_all(itemprop="Code")]

    # 提取 'classifications' 属性的文本并将其转为列表
    classifications: list[str] = [i.get_text(strip=True) for i in soup.find_all(itemprop="classifications")]

    # 细分
    infor_list = []

    # 处理 1 到 9 的情况
    for num in range(1, 10):
        infor = soup.find(num=f"000{num}")
        if infor:
            infor_list.append(infor.text.strip())

    # 处理 10 到 99 的情况
    for num in range(10, 100):
        infor = soup.find(num=f"00{num}")
        if infor:
            infor_list.append(infor.text.strip())
        else:
            break

    # 处理 100 到 199 的情况
    for num in range(100, 200):
        try:
            infor = soup.find(num=f"0{num}")
            if infor:
                infor_list.append(infor.text.strip())
        except Exception as e:
            print(e)
            print('over')
            break

    # publicationNumber = ','.join([i.get_text(strip=True) for i in soup.find_all(itemprop="publicationNumber")])
    # priorityDate = ','.join([i.get_text(strip=True) for i in soup.find_all(itemprop="priorityDate")])
    # publicationDate = ','.join([i.get_text(strip=True) for i in soup.find_all(itemprop="publicationDate")])
    # assigneeOriginal = ','.join([i.get_text(strip=True) for i in soup.find_all(itemprop="assigneeOriginal")])

    # 写入CSV文件
    with open(file='patent_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # 写入标题行
        writer.writerow(
            ['Patent Title', 'Publication Number', 'Abstract', 'Images', 'Inventors', 'Current Assignees', 'Events',
             'Classifications Code', 'Classifications', 'Information'])

        # 写入数据行
        writer.writerow([
            patent_title,
            pub_num,
            abstract,
            img_list,
            inventor,
            current_assignee,
            events_dict,
            classifications_code,
            classifications,
            infor_list,
        ])


if __name__ == "__main__":
    url = 'https://patents.google.com/patent/US11885138B2'
    get_content(url)
