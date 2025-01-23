# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import logging
import time
import re

# 设置日志信息
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
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
            for video in data["aweme_list"]:
                video_id = video['aweme_id']
                logging.info(f'Fetched {video_id}')
                self.pipline(video_id)

        except Exception as e:
            logging.error(f"Failed for {e}.")
            pass

    @staticmethod
    def pipline(video_id):
        with open(f'video-id.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{video_id}\n')


def main():
    url = input('url: ')
    cookie = input('cookie: ')
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
