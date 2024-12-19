# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import datetime
import aiohttp
import asyncio
import logging
import time
import json
import re
import os

# 构造伪请求头
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
}

# 设置日志信息
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)


async def failed_fetch(video_id):
    with open('Failed.txt', mode='a', encoding='utf-8') as f:
        f.write(f"{video_id}\n")


# 异步请求获取页面内容
async def fetch(session, video_id):
    # 构造URL
    url = f'https://www.iesdouyin.com/share/video/{video_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                page_content = await response.text()
                # 提取视频信息
                pattern = re.compile(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>")
                re_find = pattern.search(page_content)
                if re_find:
                    json_data = json.loads(re_find.group(1).strip())
                    video_data = json_data["loaderData"]["video_(id)/page"]['videoInfoRes']['item_list'][0]
                    # 解析视频数据
                    await parse(video_data)

                else:
                    logging.error(f"Failed to fetch page for {video_id}.")
                    await failed_fetch(video_id)
            else:
                logging.error(f"Failed to fetch page for {video_id}. Status code: {response.status}")
                await failed_fetch(video_id)


# 异步解析视频信息
async def parse(video_data):
    aweme_id = video_data['aweme_id']
    desc = video_data['desc']
    create_time = str(datetime.datetime.fromtimestamp(video_data['create_time']))
    author = video_data['author']['nickname']
    sec_uid = video_data['author']['sec_uid']
    cover_url = video_data["video"]["cover"]["url_list"][0]

    statistics = video_data['statistics']
    comment_count = statistics['comment_count']
    digg_count = statistics['digg_count']
    share_count = statistics['share_count']
    collect_count = statistics['collect_count']

    text_extra = [text_dict['hashtag_name'] for text_dict in video_data['text_extra']]
    text_extra_str = '|'.join(str(item) for item in text_extra)

    video_infor = {
        'video_id': aweme_id,  # 视频ID
        'video_title': desc,  # 视频标题
        'video_keywords': text_extra_str,  # 视频关键词
        'video_release_date': create_time,  # 视频发布时间
        'video_author': author,  # 视频作者
        'video_author_page_id': sec_uid,  # 视频作者主页ID
        'video_cover_url': cover_url,  # 视频封面URL
        'video_likes': digg_count,  # 视频点赞数
        'video_comments': comment_count,  # 视频评论数
        'video_favorites': collect_count,  # 视频收藏数
        'video_shares': share_count,  # 视频分享数
    }

    if video_data['images']:
        video_infor['video_music'] = video_data['video']['play_addr']['uri']

        images = []  # 存储提取的图片链接
        for img in video_data["images"]:
            url_list = img.get("url_list")
            if isinstance(url_list, list) and url_list and url_list[0]:
                images.append(url_list[0])

        video_infor['video_images'] = images

    else:
        video_infor['video'] = video_data["video"]["play_addr"]["url_list"][0].replace("playwm", "play").replace("720",
                                                                                                                 "1080")
    await pipline(video_infor)


# 写入JSON文件
async def pipline(video_infor):
    video_id = video_infor['video_id']
    filename = f'{video_id}.json'
    os.makedirs('VIDEO', exist_ok=True)

    with open(f'VIDEO/{filename}', mode='w', encoding='utf-8') as output_file:
        json.dump(video_infor, output_file, ensure_ascii=False, indent=4)
    logging.info(f"Fetched {filename}")


async def main():
    # 构造视频ID列表
    video_id_list = ['7449653909674544441']

    # 限制并发数量
    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(video_id):
        async with semaphore:
            await fetch(session, video_id)
            # 减小风险
            await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(video_id) for video_id in video_id_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # 计算采集时间
    start_time = time.time()
    try:
        # 设置时间循环方式
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")

    except Exception as error:
        logging.error(f"An error occurred: {error}.")
