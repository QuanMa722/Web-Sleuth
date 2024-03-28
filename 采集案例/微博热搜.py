
# -*- coding: utf-8 -*-
# https://weibo.com/ajax/side/hotSearch

from fake_useragent import UserAgent
import requests
import json


def get_reap() -> requests.Response:

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    url = "https://weibo.com/ajax/side/hotSearch"

    response = requests.get(url=url, headers=headers)

    return response


def get_infor(response: requests.Response) -> None:

    data_json = json.loads(response.text)
    data_top_str = data_json["data"]["hotgovs"][0]["note"]
    print(data_top_str)

    for num in range(0, 50):
        data_str = data_json["data"]["realtime"][num]["note"]
        print(data_str)

    return None


if __name__ == '__main__':

    try:
        response = get_reap()
        get_infor(response)

    except Exception as e:
        print(f"An error occurred: {e}")


