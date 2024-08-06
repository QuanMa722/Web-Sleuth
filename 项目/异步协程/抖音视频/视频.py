# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import asyncio
import aiohttp
import time
import json
import re

with open(file='config.json', mode='r') as f:
    configs = json.load(f)


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime(int(time.time())))
    msgs = msg.split("\n")
    for word in msgs:
        print("[" + nowt + "] " + str(word))


class Task:
    def __init__(self, aweme_id, user_id, cookie):
        self.max_cursor = int(time.time() * 1000)
        self.time_start = time.time()
        self.aweme_id = aweme_id
        self.cookie = str(cookie)
        self.user_id = user_id
        self.nickname = "Null"
        self.has_more = True

        ua = UserAgent()
        self.headers = {
            'referer': f'https://www.douyin.com/user/{self.user_id}',
            'cookie': self.cookie,
            'User-Agent': ua.random,
        }

    async def run(self):
        async with aiohttp.ClientSession() as session:
            while self.has_more:
                if await self.task(session):
                    break

    async def task(self, session):
        form = f'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={self.user_id}&max_cursor={self.max_cursor}&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'

        try:
            async with session.get("http://xbogus.tom14.top/", params={"form": form}, timeout=3) as xb_resp:
                xb = await xb_resp.json()

            url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?{form}&X-Bogus={xb["data"]["X_Bogus"]}'
            async with session.get(url, headers=self.headers, timeout=3) as resp:
                resp_data = await resp.json()

            self.nickname = resp_data["aweme_list"][0]["author"]["nickname"]
            await self.save_data(resp_data, self.cookie)

            if not resp_data["has_more"]:
                self.has_more = False

            self.max_cursor = resp_data["max_cursor"]

        except Exception as e:
            print(f"An error occurred: {e}")

    async def save_data(self, data, cookie):
        for aweme in data["aweme_list"]:
            desc = aweme["statistics"]
            if aweme["aweme_id"] == str(self.aweme_id):
                desc['作者'] = self.nickname
                desc['标题'] = aweme['desc']
                desc['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(aweme["create_time"])))
                desc['点赞'] = desc.pop('digg_count')
                desc['评论'] = desc.pop('comment_count')
                desc['收藏'] = desc.pop('collect_count')
                desc['分享'] = desc.pop('share_count')
                desc['作品id'] = aweme["aweme_id"]

                del desc['play_count']
                del desc['admire_count']

                if aweme['images'] is None:
                    desc['格式'] = "video"
                    titles = ""
                    titles_list = ["作者", "标题", "作品id", "时间", "点赞", "评论", "格式", "收藏", "分享"]
                    for title in titles_list:
                        titles = titles + title + ":" + str(desc[title]) + "\n"

                    printt(titles)

                    video_url = aweme["video"]["play_addr"]["url_list"][0]
                    video = requests.get(url=video_url, headers=self.headers)
                    with open(file="video.mp4", mode='wb') as f:
                        f.write(video.content)

                    printt("已完成视频的下载。")

                else:
                    desc['格式'] = "picture"
                    count = 0
                    for image in aweme["images"]:
                        count += 1
                        image_url = image["url_list"][-1]
                        video = requests.get(url=image_url, headers=self.headers)
                        with open(file=f"picture_{count}.jpeg", mode='wb') as f:
                            f.write(video.content)

                    printt("已完成图片的下载。")

            else:
                continue


async def main():
    url = configs['url']
    cookie = configs['cookie']
    aweme_id = configs['aweme_id']

    user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]
    task = Task(aweme_id, user_id, cookie)
    await task.run()


if __name__ == '__main__':
    asyncio.run(main())
