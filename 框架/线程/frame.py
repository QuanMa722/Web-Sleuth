# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import requests
import logging
import time

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,  # 设置日志记录级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志输出格式
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()  # 日志输出到控制台
    ]
)


# 发送请求并处理响应的函数
def fetch(url):
    try:
        # 使用 fake_useragent 库生成随机的 User-Agent 请求头
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random  # 随机生成 User-Agent 字符串，避免被网站封锁
        }

        # 发起 HTTP 请求
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # 确保响应使用 UTF-8 编码
        response.raise_for_status()  # 如果响应状态码不是 2xx，抛出异常
        resp_text = response.text  # 获取响应内容

        # 请求成功，记录日志
        logging.info(f"Successfully fetched {url}, status code {response.status_code}")

        # 调用解析函数处理响应内容
        parse(resp_text)

    except Exception as e:
        # 出现错误时，将失败的 URL 写入 'Failed.txt' 文件，便于后续排查
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{url}\n')

        logging.error(f"Error fetching {url}: {e}")  # 记录错误信息


# 解析响应内容的函数
def parse(resp_text):
    # 目前仅作为示例，直接将响应内容传递给下游函数
    text = resp_text
    pipeline(text)


# 将解析后的数据写入文件
def pipeline(text):
    with open('output.txt', mode='w', encoding='utf-8') as f:
        f.write(text + '\n')


# 生成待爬取的 URL 列表
def task():
    # 这里为了示例，使用相同的 URL 100 次，实际应用中应根据需要生成不同 URL
    url_list = ['https://www.baidu.com/'] * 100
    return url_list


# 主函数，控制多线程的并发请求
def main():
    # 生成要请求的 URL 列表，这里示例为 10 个相同 URL
    url_list = task()

    # 使用 ThreadPoolExecutor 来处理并发请求
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 使用 executor.map 来并发地执行 fetch 函数
        executor.map(lambda url: fetch(url), url_list)


# 程序入口
if __name__ == '__main__':
    start_time = time.time()  # 记录程序开始的时间

    try:
        # 执行主函数
        main()
        # 记录总耗时
        print(f"Total time: {round((time.time() - start_time), 2)}s")

    except Exception as error:
        # 捕获并记录任何异常
        logging.error(f"An error occurred: {error}.")
