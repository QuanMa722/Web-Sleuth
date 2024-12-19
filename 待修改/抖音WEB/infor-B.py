# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import datetime
import logging
import json
import time
import os
import re

# 设置日志信息
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)


class Task:

    def __init__(self, user_id, cookie):
        self.max_cursor = 10000000000000
        self.user_id = user_id
        self.cookie = cookie
        self.has_more = True

    def run(self):
        while self.has_more:
            self.fetch()

    def fetch(self):

        ua = UserAgent()
        headers = {
            'referer': f'https://www.douyin.com/user/{self.user_id}',
            'cookie': self.cookie,
            'User-Agent': ua.random,
        }

        form = f'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={self.user_id}&max_cursor={self.max_cursor}&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'
        url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?{form}'

        try:
            # 降低风险
            time.sleep(5)
            response = requests.get(url=url, headers=headers, timeout=3)
            resp_data = response.json()

            self.parse(resp_data)
            if not resp_data["has_more"]:
                self.has_more = False

            self.max_cursor = resp_data["max_cursor"]

        except Exception as e:
            logging.error(f"Failed for {e}.")

    def parse(self, data):
        try:
            for aweme in data["aweme_list"]:
                aweme_id = aweme['aweme_id']
                logging.info(f'Fetched {aweme_id}')
                desc = aweme['desc']
                create_time = str(datetime.datetime.fromtimestamp(aweme['create_time']))
                author = aweme['author']['nickname']
                sec_uid = aweme['author']['sec_uid']
                cover_url = aweme["video"]["cover"]["url_list"][0]

                statistics = aweme['statistics']
                comment_count = statistics['comment_count']
                digg_count = statistics['digg_count']
                share_count = statistics['share_count']
                collect_count = statistics['collect_count']

                video_infor = {
                    'video_id': aweme_id,  # 视频ID
                    'video_title': desc,  # 视频标题
                    'video_release_date': create_time,  # 视频发布时间
                    'video_author': author,  # 视频作者
                    'video_author_page_id': sec_uid,  # 视频作者主页ID
                    'video_cover_url': cover_url,  # 视频封面URL
                    'video_likes': digg_count,  # 视频点赞数
                    'video_comments': comment_count,  # 视频评论数
                    'video_favorites': collect_count,  # 视频收藏数
                    'video_shares': share_count,  # 视频分享数
                }

                if aweme['images']:
                    video_infor['video_music'] = aweme['video']['play_addr']['uri']

                    images = []  # 存储提取的图片链接
                    for img in aweme["images"]:
                        url_list = img.get("url_list")
                        if isinstance(url_list, list) and url_list and url_list[0]:
                            images.append(url_list[0])

                    video_infor['video_images'] = images
                    self.pipline(video_infor)

                else:
                    video_infor['video_music'] = aweme['music']['play_url']['url_list'][0]
                    video_infor['video_url'] = aweme["video"]["play_addr"]["url_list"][0].replace("playwm",
                                                                                                  "play").replace(
                        "720", "1080")
                    self.pipline(video_infor)

        except Exception as e:
            logging.error(f"Failed for {e}.")
            pass

    @staticmethod
    def pipline(video_infor):
        video_id = video_infor['video_id']
        filename = f'{video_id}.json'
        os.makedirs('VIDEO', exist_ok=True)

        with open(f'VIDEO/{filename}', mode='w', encoding='utf-8') as output_file:
            json.dump(video_infor, output_file, ensure_ascii=False, indent=4)


def main():
    url = ''
    cookie = ''
    user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]
    task = Task(user_id, cookie)
    task.run()


if __name__ == '__main__':
    # 计算采集时间
    start_time = time.time()
    try:
        main()
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")

    except Exception as error:
        logging.error(f"An error occurred: {error}.")
