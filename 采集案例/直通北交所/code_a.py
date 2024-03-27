
# -*- coding: utf-8 -*-
# https://www.tobse.cn/specialized/enterprise

from fake_useragent import UserAgent
import requests
import json
import re


def get_resp():

    url = r"https://www.tobse.cn/specialized/enterprise/"

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    data = {
        "p": 5582,
        "key": "", 
        "level": 0,
        "cat": "",
        "prov": 0,
        "city": 0,
        "ipo": 0,
        "licence_status": "",
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.status_code)
    get_infor(response)

    return None


def get_infor(response):

    text = json.loads(response.text)["pageView"]
    print(text)
    find_text = re.findall(r'<td>(.*?)</td>', text)
    elements = find_text[1:]
    filtered_elements = [el for el in elements if not re.match(r'<.*?>', el)]

    num = int(len(filtered_elements) / 6)
    result_list = []
    count = 0
    for _ in range(num):
        result_list.append(filtered_elements[count:count + 6])
        print(filtered_elements[count:count + 6])
        count += 6

    return None


if __name__ == '__main__':
    try:
        page_num = int(input("page:"))
        get_resp()
    except Exception as e:
        print(f"An error occurred: {e}")
