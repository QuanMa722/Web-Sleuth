import json

# -*- coding: utf-8 -*-
# 采集抖音网页版用户评论数据

# 导入需要的库
from fake_useragent import UserAgent  # 用于生成随机的User-Agent
import requests  # 用于发送HTTP请求
import datetime  # 用于处理时间
import time  # 用于暂停程序执行


# 爬取评论数据
def get_comment(headers: dict, aweme_id: str, page_num: int) -> None:
    """
    爬取指定抖音视频的评论数据并打印每条评论的信息。

    :param headers: dict，请求头，包括用户代理和cookie信息。
    :param aweme_id: str，抖音视频的ID。
    :param page_num: int，需要爬取的评论页数。
    :return: None，将评论信息打印出来。
    """
    # 评论条数
    cursor = 0
    # 评论页数
    page = 0

    while True:
        params = {
            "aid": 6383,
            "cursor": cursor,
            "aweme_id": aweme_id,
            "count": 20,
        }
        url = f"https://www.douyin.com/aweme/v1/web/comment/list?"

        time.sleep(1)  # 暂停1秒，防止请求过于频繁被封IP

        json_text = get_resp(url, params, headers).text  # 发送请求获取响应

        json_data = json.loads(json_text)

        for comment in json_data["comments"]:
            get_data(comment)  # 处理评论数据并打印评论信息

        cursor += 20  # 更新评论条数
        page += 1  # 更新评论页数

        print(f"第{page}页爬取完毕。")
        if page == page_num:
            break
    return None


# 发送请求获取响应
def get_resp(url: str, params: dict, headers: dict) -> requests.Response:
    """
    发送GET请求获取指定URL的响应数据。

    :param url: str，请求的URL。
    :param params: dict，请求的参数。
    :param headers: dict，请求头，包括用户代理和cookie信息。
    :return: requests.Response，返回响应对象。
    """
    response = requests.get(url, params=params, headers=headers)
    response.encoding = "utf-8"
    return response


# 将时间戳转换为 yyyy-mm-dd 格式
def get_time(time: int) -> str:
    """
    将时间戳转换为指定格式的日期字符串。

    :param time: int，时间戳。
    :return: str，格式化后的日期字符串。
    """
    return str(datetime.datetime.fromtimestamp(time))[0:11]


# 处理评论数据
def get_data(comment: dict) -> None:
    """
    处理每条评论数据并打印评论信息。
    :param comment: dict，评论数据。
    :return: None，将评论信息打印出来。
    """
    try:
        # 处理时间
        time_correct = get_time(comment["create_time"])

        data_dict = {
            "用户id": comment["user"]["uid"].strip(),
            "用户名": comment["user"]["nickname"].strip(),
            "评论时间": time_correct,
            "IP属地": comment["ip_label"],
            "点赞数量": comment["digg_count"],
            "评论内容": comment["text"].strip().replace('\n', ""),
        }

        print(data_dict)  # 打印评论信息
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
