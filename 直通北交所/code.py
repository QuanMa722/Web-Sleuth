
# -*- coding: utf-8 -*-
# 采集直通北交所企业名录数据
# 多线程

# 导入需要的第三方库
from fake_useragent import UserAgent  # 用于生成随机的User-Agent
import concurrent.futures  # 用于实现多线程并发任务
import requests  # 用于发送HTTP请求
import json  # 用于处理JSON数据
import re  # 用于正则表达式匹配


def get_process_data(i):
    """
    从指定URL获取数据并处理

    参数:
    i (int): 页数

    返回:
    list: 包含处理后数据的列表
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
        "p": i,
        "key": "",
        "level": 0,
        "cat": "",
        "prov": 0,
        "city": 0,
        "ipo": 0,
        "licence_status": "",
    }

    response = requests.post(url=url, headers=headers, data=data)  # 发送POST请求
    # 解析JSON响应并获取页面信息
    infor = json.loads(response.text)["pageView"]
    # 使用正则表达式提取<td>标签中的内容
    find_text = re.findall(r'<td>(.*?)</td>', infor)
    elements = find_text[1:]
    # 过滤掉类似元素
    filtered_elements = [el for el in elements if not re.match(r'<.*?>', el)]
    num = int(len(filtered_elements) / 6)
    result = []
    count = 0
    for _ in range(num):
        result.append(filtered_elements[count:count + 6])
        print(filtered_elements[count:count + 6])  # 输出每个结果
        count += 6

    return result


def main():
    """
    主函数，用于控制整个程序流程
    """
    # 获取用户输入的页数
    page_num = int(input("请输入页数："))
    # 根据需求选择写入数据的方式
    with open("data.txt", "a", encoding="utf-8") as f:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 提交任务并获取结果
            results = list(executor.map(get_process_data, range(1, page_num + 1)))
            # 将结果写入文件
            for result in results:
                for item in result:
                    f.writelines(str(item) + "\n")


if __name__ == "__main__":
    main()