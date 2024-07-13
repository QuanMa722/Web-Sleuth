# -*- coding: utf-8 -*-
# Simplification and improvement with https://github.com/raindrop-hb/douyin_spider

from fake_useragent import UserAgent
from urllib.parse import quote
from uuid import uuid4
import requests
import asyncio
import aiohttp
import time
import csv
import os
import re


async def printt(msg):
    print("[" + str(time.strftime("%H:%M:%S", time.localtime(int(time.time())))) + "] " + str(msg))


async def get_machine_code():
    return str(uuid4().hex[-12:])


async def get_urls(session, cookie, user_id):
    form = f'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={user_id}&max_cursor={int(round(time.time() * 1000))}&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'

    ua = UserAgent()
    headers = {
        'referer': f'https://www.douyin.com/user/{user_id}',
        'User-Agent': ua.random,
        'cookie': str(cookie),
    }

    xbogus_api = "http://xbogus.tom14.top/?form=" + quote(form)
    xb = requests.get(url=xbogus_api + quote(form), timeout=3).json()
    url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?{form}' + "&X-Bogus=" + xb['data']["X_Bogus"]

    async with session.get(url, headers=headers) as resp:
        resp_data = await resp.json()
        nickname = resp_data["aweme_list"][0]["author"]["nickname"]
        os.makedirs(nickname, exist_ok=True)
        for element in ["video", "cover", "bgmusic", "picture"]:
            os.makedirs(os.path.join(nickname, element), exist_ok=True)

        await download_videos(session, resp_data["aweme_list"], nickname, headers)


async def download_videos(session, aweme_list, nickname, headers):
    tasks = []
    for aweme in aweme_list:
        tasks.append(download_video(session, aweme, nickname, headers))
    await asyncio.gather(*tasks)


async def download_video(session, aweme, nickname, headers):
    desc = aweme["statistics"]
    desc['标题'] = aweme['desc']
    desc['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(aweme["create_time"])))
    desc['收藏'] = desc.pop('collect_count')
    desc['评论'] = desc.pop('comment_count')
    desc['点赞'] = desc.pop('digg_count')
    desc['分享'] = desc.pop('share_count')
    desc['分享链接'] = aweme["share_info"]['share_url']
    desc['作品id'] = aweme["aweme_id"]
    del desc['play_count']
    del desc['admire_count']

    if aweme['images'] is None:
        desc['格式'] = "video"
    else:
        desc['格式'] = "picture"

    file_exists = os.path.isfile(nickname + "/video_data.csv")
    with open(nickname + "/video_data.csv", mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=desc.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(desc)

    if aweme['images'] is None:
        await download_file(session, aweme["video"]["play_addr"]["url_list"][0],
                            f'{nickname}/video/{aweme["aweme_id"]}.mp4', headers)
        await download_file(session, aweme["music"]["play_url"]["url_list"][0],
                            f'{nickname}/bgmusic/{aweme["aweme_id"]}.mp3', headers)
        await download_file(session, aweme["video"]["cover"]["url_list"][1],
                            f'{nickname}/cover/{aweme["aweme_id"]}.jpg', headers)

    else:
        for count, image in enumerate(aweme["images"]):
            image_url = image["url_list"][-1]
            await download_file(session, image_url, f'{nickname}/picture/{aweme["aweme_id"]}_{count}.jpeg', headers)

    await printt("Download the video message.")


async def download_file(session, url, file_path, headers):
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)


async def main():
    start_time = time.time()
    try:
        url = ""
        cookie = ""
        user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]
        async with aiohttp.ClientSession() as session:
            await printt("Start crawling the video of the user.")
            await get_urls(session, cookie, user_id)
    except Exception as e:
        await printt(f"An error occurred: {e}")
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        await printt("Stop crawling the video of the user. ")
        await printt(f"Elapsed time: {elapsed_time:.2f} seconds.")


if __name__ == '__main__':
    asyncio.run(main())
