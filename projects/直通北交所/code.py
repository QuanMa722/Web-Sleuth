# -*- coding: utf-8 -*-
# https://www.tobse.cn/specialized/enterprise

from fake_useragent import UserAgent
import requests
import time
import json
import re


def get_resp(page) -> requests.Response:

    url = r"https://www.tobse.cn/specialized/enterprise/"

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    data = {
        "p": page,
        "key": "",
        "level": 0,
        "cat": "",
        "prov": 0,
        "city": 0,
        "ipo": 0,
        "licence_status": "",
    }

    response = requests.post(url=url, headers=headers, data=data)

    return response


def get_index(page_input: int):

    pages: list = list(range(1, page_input + 1))

    index = 0
    while index < len(pages):
        page = pages[index]

        time.sleep(1)

        response = get_resp(page)
        text_json = json.loads(response.text)["pageView"]

        if text_json[6] != "t":
            print(f"Page{page} after have been queued.")
            pages.append(page)

        else:
            print(f"Page{page} is successfully obtained.")
            get_data(text_json)

        index += 1

    return None


def get_data(text_json):

    find_text = re.findall(r'<td>(.*?)</td>', text_json)
    elements = find_text[1:]
    filtered_elements = [el for el in elements if not re.match(r'<.*?>', el)]

    num = int(len(filtered_elements) / 6)
    count = 0

    with open(file="company.txt", mode="a", encoding="utf-8") as f:
        for _ in range(num):
            infor = filtered_elements[count:count + 6]
            f.write(str(infor) + "\n")

            print(infor)
            count += 6

    return None


def main():

    try:
        get_index(10)  # page

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()


