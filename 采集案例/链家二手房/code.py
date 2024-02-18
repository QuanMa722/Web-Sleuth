
# -*- coding: utf-8 -*-
# 采集链家二手房数据
# 细分价格区间 + 多线程 + 代理池

# 导入需要的第三方库
from fake_useragent import UserAgent  # 用于获取随机User-Agent
from lxml import etree  # 用于解析HTML
import threading  # 用于多线程处理
import requests  # 用于发送HTTP请求
import random  # 用于生成随机数
import time  # 用于时间相关操作
import re  # 用于正则表达式匹配


def get_anti() -> tuple:
    """
    获取随机的User-Agent和代理IP。

    返回:
    tuple: 包含随机User-Agent和代理IP的元组。
    """
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random  # 随机ua
    }

    # 根据需求选择代理池
    api_list = [
        "124.172.117.189:19812",
        "219.133.31.120:26947",
        "183.237.194.145:28436",
        "183.62.172.50:23485",
        "163.125.157.243:17503",
        "183.57.42.79:26483",
        "202.103.150.70:17251",
        "182.254.129.124:15395",
        "58.251.132.181:20659",
        "112.95.241.76:21948",
    ]

    proxies = {
        "http": f"http: //{random.choice(api_list)}"  # 随机代理
    }

    return headers, proxies


# 获取每页的URL，并使用多线程进行数据采集
def get_url(area_list: list, page_list: list, num_threads: int) -> None:
    """
    获取每页的URL，并使用多线程进行数据采集。

    参数:
    area_list (list): 地区列表，包括城市和区域。
    page_list (list): 价格区间和页数列表。
    num_threads (int): 并发线程的数量。

    返回:
    无返回值，将采集到的数据打印出来并写入文件。
    """
    threads1 = []  # 构建线程池1
    # 根据报错信息修改代码
    try:
        for single_list in page_list:  # 遍历列表
            for page in range(1, single_list[2] + 1):  # 遍历页数
                headers, proxies = get_anti()  # 防止限制
                # 目标函数为process_page
                thread = threading.Thread(target=process_page,
                                          args=(area_list, single_list, headers, proxies, page, num_threads))
                thread.start()
                threads1.append(thread)

                # 控制线程数，避免浪费资源
                if len(threads1) >= num_threads:
                    for t in threads1:
                        t.join()
                    threads1 = []

        for thread in threads1:
            thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")  # 打印报错信息

    return None


def process_page(area_list: list, single_list: list, headers: dict, proxies: tuple, page: int, num_threads: int) -> None:
    """
    第一个多线程的目标函数，用于启动第二个多线程。

    参数:
    area_list (list): 地区列表，包括城市和区域。
    single_list (list): 价格区间和页数信息。
    headers (dict): 请求头，包括User-Agent信息。
    proxies (dict): 代理IP信息。
    page (int): 页数。
    num_threads (int): 并发线程的数量。

    返回:
    无返回值，启动第二个多线程进行数据采集。
    """
    # 初始url
    url = f"https://{area_list[0]}.lianjia.com/ershoufang/{area_list[1]}/pg{page}bp{single_list[0]}ep{single_list[1]}"
    # 发送请求
    response = requests.get(url=url, headers=headers, proxies=proxies)
    # print(f"响应：{response.status_code}  价格区间：{single_list[0]}-{single_list[1]}  页数：{page}/{single_list[2]}")

    # 利用正则表达式获取每一页的url
    re_find = '<a class="" href="(.*?)" target="_blank"'
    url_list = re.findall(re_find, response.text)

    # 构建第二个线程
    threads2 = []
    try:
        thread = threading.Thread(target=get_data, args=(url_list,))  # 目标函数为get_data
        thread.start()
        threads2.append(thread)
        if len(threads2) <= num_threads:
            for t in threads2:
                t.join()
            threads2 = []
        for thread in threads2:
            thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")  # 打印报错信息
    return None

# 获取数据
def get_data(url_list: list) -> None:
    """
    获取每页房屋信息的数据。

    参数:
    url_list (list): 包含每页URL的列表。

    返回:
    无返回值，将采集到的数据打印出来并写入文件。
    """
    # 遍历每页的url
    for every_single_url in url_list:
        # 防止限制
        headers, proxies = get_anti()
        # 发送请求
        response = requests.get(url=every_single_url, headers=headers, proxies=proxies)
        # xpath解析获取数据
        resp_text = etree.HTML(response.text)

        # 根据需求获取数据
        # 总价
        total_price = resp_text.xpath("//div[@class='overview']//div/span/text()")[2]
        # 单价
        single_price = resp_text.xpath("//div[@class='overview']//div/span/text()")[3]
        # 地点
        # place = resp_text.xpath("//div[@class='overview']//div/span/a/text()")[0] + " " + \
        #         resp_text.xpath("//div[@class='overview']//div/span/a/text()")[1] + " " + \
        #         resp_text.xpath("//div[@class='overview']//div[@class='areaName']/span/text()")[2][-4:]
        place = resp_text.xpath("//div[@class='overview']//div/span/a/text()")[1]
        # 房子名称
        name = resp_text.xpath("//div[@class='overview']//div[@class='communityName']/a/text()")[0]

        start_dict = {
            "总价": total_price,
            "单价": single_price,
            "地区": place,
            "名称": name,

        }

        # 房子属性
        base_key1 = resp_text.xpath("//div[@class='base']//span/text()")[0:12]
        base_value1 = resp_text.xpath("//div[@class='base']//li/text()")
        text_list = [text.strip() for text in base_value1 if text.strip()]
        middle_dict1 = {k: v for k, v in zip(base_key1, text_list)}

        # 交易属性
        base_key2 = resp_text.xpath("//div[@class='transaction']//span[1]/text()")
        base_value2 = resp_text.xpath("//div[@class='transaction']//span[2]/text()")
        middle_dict2 = {k: v for k, v in zip(base_key2, base_value2)}

        # 定义一个空字典，用来整合信息。
        last_dict = {

        }

        # 更新字典
        last_dict.update(start_dict)
        last_dict.update(middle_dict1)
        last_dict.update(middle_dict2)

        # 可选择打印，检验是否报错。
        print(last_dict)

        # 根据需求选择存放数据的方法
        with open("data.txt", "a") as f:
            f.writelines(str(last_dict))

    return None


def main():
    """
    主函数，用于控制整个程序流程
    """
    # 计算时间
    start_time = time.time()

    # 更换地区
    area_list = ["wh", "jianghxia"]

    # 价格区间和页数
    page_list = [
        [1, 100, 80]
    ]

    # 线程数限制
    num_threads = 50

    get_url(area_list, page_list, num_threads)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"程序运行时间为：{execution_time}秒")

    # 计算采集速度
    page_num = sum([num[2] for num in page_list])
    print("采集速度约为：" + str(round((((page_num * 30) / execution_time) * 60))) + "条/分钟")


# 主程序
if __name__ == '__main__':
    main()

