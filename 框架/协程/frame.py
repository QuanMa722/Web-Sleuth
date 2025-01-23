# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiofiles
import aiohttp
import asyncio
import logging
import time

# 配置日志记录，方便调试与跟踪
logging.basicConfig(
    level=logging.INFO,  # 设置日志等级为INFO，确保可以输出基本信息
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式，包括时间、日志级别和消息
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()  # 默认输出到控制台
    ]
)


# 异步请求函数，用于发送请求并处理响应
async def fetch(session, url):
    try:
        # 使用 fake_useragent 库生成随机的 User-Agent 请求头
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }

        # 发起异步 HTTP GET 请求
        async with session.get(url, headers=headers) as response:
            # 确保响应状态码为 200（成功）
            response.raise_for_status()
            # 获取响应内容
            resp_text = await response.text()
            logging.info(f"Successfully fetched {url}, status code: {response.status}")
            # 调用解析函数进行数据处理
            await parse(resp_text)

    except Exception as e:
        # 出现错误时，将失败的 URL 写入 'Failed.txt' 文件，便于后续排查
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{url}\n')

        logging.error(f"Error fetching {url}: {e}")  # 记录错误信息


# 解析获取到的响应内容
async def parse(resp_text):
    # 可以在此对获取的响应内容进行各种处理（如正则匹配、HTML解析等）
    text = resp_text
    await pipeline(text)  # 将处理过的数据写入文件


# 异步将内容写入文件
async def pipeline(text):
    # 使用 aiofiles 异步写入文件，避免阻塞主线程
    async with aiofiles.open('output.txt', mode='w', encoding='utf-8') as f:
        await f.write(text + '\n')  # 每个响应内容写入新的一行


# 生成待爬取的 URL 列表
def task():
    # 这里为了示例，使用相同的 URL 100 次，实际应用中应根据需要生成不同 URL
    url_list = ['https://www.baidu.com/'] * 100
    return url_list


# 主异步函数，负责管理并发请求
async def main():
    url_list = task()  # 获取 URL 列表
    semaphore = asyncio.Semaphore(10)  # 限制最大并发数为 10，避免请求过多导致服务器压力过大

    # 定义并发请求函数，确保每次请求都使用信号量控制并发数
    async def sem_fetch(url):
        async with semaphore:  # 使用信号量，控制并发
            await fetch(session, url)  # 调用 fetch 函数发送请求

    # 使用 aiohttp 创建一个客户端会话
    async with aiohttp.ClientSession() as session:
        # 创建所有的异步任务
        tasks = [sem_fetch(url) for url in url_list]
        # 并发执行所有任务，直到全部完成
        await asyncio.gather(*tasks)


# 主入口
if __name__ == '__main__':
    start_time = time.time()  # 记录开始时间

    try:
        # 针对 Windows 平台设置事件循环策略
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # 运行主异步函数
        asyncio.run(main())
        # 输出总耗时
        print(f"Total time: {round((time.time() - start_time), 2)}s")
    except Exception as error:
        # 捕获并记录任何异常
        logging.error(f"An error occurred: {error}.")