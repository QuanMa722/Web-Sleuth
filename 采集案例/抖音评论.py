
# -*- coding: utf-8 -*-
# https://www.douyin.com

from fake_useragent import UserAgent
import requests
import datetime
import time
import json


def get_comment(headers: dict, aweme_id: str, page_num: int) -> None:

    cursor = 0
    page = 0

    while True:
        params = {
            "aid": 6383,
            "cursor": cursor,
            "aweme_id": aweme_id,
            "count": 20,
        }
        url = f"https://www.douyin.com/aweme/v1/web/comment/list?"

        time.sleep(1)

        json_text = get_resp(url, params, headers).text
        json_data = json.loads(json_text)

        for comment in json_data["comments"]:
            get_data(comment)

        cursor += 20
        page += 1

        print(f"第{page}页爬取完毕。")
        if page == page_num:
            break

    return None


def get_resp(url: str, params: dict, headers: dict) -> requests.Response:

    response = requests.get(url, params=params, headers=headers)
    response.encoding = "utf-8"

    return response


def get_time(time: int) -> str:

    return str(datetime.datetime.fromtimestamp(time))[0:11]


def get_data(comment: dict) -> None:

    try:

        time_correct = get_time(comment["create_time"])

        data_dict = {
            "用户id": comment["user"]["uid"].strip(),
            "用户名": comment["user"]["nickname"].strip(),
            "评论时间": time_correct,
            "IP属地": comment["ip_label"],
            "点赞数量": comment["digg_count"],
            "评论内容": comment["text"].strip().replace('\n', ""),
        }

        print(data_dict)
        with open("test.txt", "a") as f:
            try:
                f.writelines(str(data_dict))
            except Exception as e:
                print(f"An error occurred: {e}")

        global comment_count
        comment_count += 1
    except Exception as e:
        print(e)

    return None


if __name__ == '__main__':

    """
    主函数，用于控制整个程序流程
    """
    # 输入参数
    cookie = input("cookie:")
    aweme_id = input("aweme_id:")
    page_num = int(input("请输入爬取的页数:"))

    # 设置随机ua
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "cookie": cookie,
    }
    comment_count = 0
    get_comment(headers, aweme_id, page_num)
