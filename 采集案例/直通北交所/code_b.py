
# -*- coding: utf-8 -*-
# 采集直通北交所企业名录数据(https://www.tobse.cn/specialized/enterprise)
# 多线程

# 导入需要的第三方库
from fake_useragent import UserAgent  # 用于生成随机的User-Agent
import concurrent.futures  # 用于实现多线程并发任务
import requests  # 用于发送HTTP请求
import json  # 用于处理JSON数据
import re  # 用于正则表达式匹配


def get_process(page_num: int) -> list:
    """
    多线程的目标函数，从指定URL获取数据并处理

    :param page_num: int 采集页数
    :return: list 处理数据后的列表
    """

    # 设置URL
    url = "https://www.tobse.cn/specialized/enterprise/"

    # 生成随机User-Agent
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random  # 随机ua
    }

    # 准备POST请求的数据
    data = {
        "p": page_num,
        "key": "",
        "level": 0,
        "cat": "",
        "prov": 0,
        "city": 0,
        "ipo": 0,
        "licence_status": "",
    }

    response = requests.post(url=url, headers=headers, data=data)  # 发送POST请求

    # 数据处理
    # 解析JSON响应并获取页面信息
    text = json.loads(response.text)["pageView"]
    # 使用正则表达式提取<td>标签中的内容
    find_text = re.findall(r'<td>(.*?)</td>', text)
    elements = find_text[1:]
    # 过滤掉类似元素
    filtered_elements = [el for el in elements if not re.match(r'<.*?>', el)]

    # 构建数据列表
    num = int(len(filtered_elements) / 6)
    result_list = []
    count = 0
    for _ in range(num):
        result_list.append(filtered_elements[count:count + 6])
        # 可选择打印
        print(filtered_elements[count:count + 6])  # 输出每个结果
        count += 6

    return result_list


def get_file(item: list) -> None:
    """
    将数据写入文件中

    :param item: list 单个列表数据
    :return: None
    """

    # 根据需求选择写入的文件
    with open("company.txt", "a", encoding="utf-8") as f:
        f.write(str(item) + "\n")

    return None


def main() -> None:
    """
    主函数，用于控制整个程序流程
    """

    while True:
        try:
            # 获取用户输入的页数
            page_num = int(input("请输入采集的页数："))
            if page_num > 0:  # 添加条件判断页数是否合法
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # 提交任务并获取结果
                    result_list = list(executor.map(get_process, range(1, page_num + 1)))
                    # 将结果写入文件
                    for result in result_list:
                        for item in result:
                            get_file(item)
                break  # 输入合法，跳出循环
            else:
                print("请输入大于0的页数！")
        # 根据报错信息修改代码
        except Exception as e:
            print(f"An error occurred: {e}")

    print("数据采集完毕！")


if __name__ == "__main__":
    main()