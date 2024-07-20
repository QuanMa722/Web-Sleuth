# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import asyncio
import aiohttp
import time
import csv
import os
import re


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime(int(time.time())))
    msgs = msg.split("\n")
    for word in msgs:
        print("[" + nowt + "] " + str(word))


class Task:
    def __init__(self, user_id, cookie):
        self.max_cursor = int(time.time() * 1000)
        self.time_start = time.time()
        self.user_id = user_id
        self.cookie = cookie
        self.nickname = "Null"
        self.has_more = True
        self.picture = 0
        self.video = 0

    async def run(self):
        async with aiohttp.ClientSession() as session:
            while self.has_more:
                if await self.task(session):
                    break

    async def task(self, session):
        form = f'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={self.user_id}&max_cursor={self.max_cursor}&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'

        ua = UserAgent()
        headers = {
            'referer': f'https://www.douyin.com/user/{self.user_id}',
            'cookie': self.cookie,
            'User-Agent': ua.random,
        }

        try:
            async with session.get("http://xbogus.tom14.top/", params={"form": form}, timeout=3) as xb_resp:
                xb = await xb_resp.json()

            url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?{form}&X-Bogus={xb["data"]["X_Bogus"]}'
            async with session.get(url, headers=headers, timeout=3) as resp:
                resp_data = await resp.json()

            self.nickname = resp_data["aweme_list"][0]["author"]["nickname"]
            await self.save_data(resp_data)

            if not resp_data["has_more"]:
                self.has_more = False

            self.max_cursor = resp_data["max_cursor"]

        except Exception as e:
            print(f"An error occurred: {e}")

    async def save_data(self, data):
        for aweme in data["aweme_list"]:
            desc = aweme["statistics"]
            desc['标题'] = aweme['desc']
            desc['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(aweme["create_time"])))
            desc['点赞'] = desc.pop('digg_count')
            desc['评论'] = desc.pop('comment_count')
            desc['收藏'] = desc.pop('collect_count')
            desc['分享'] = desc.pop('share_count')
            desc['作品id'] = aweme["aweme_id"]
            desc['分享链接'] = aweme["share_info"]['share_url']
            del desc['play_count']
            del desc['admire_count']

            if aweme['images'] is None:
                desc['格式'] = "video"
                self.video += 1
            else:
                desc['格式'] = "picture"
                self.picture += 1

            titles = ""
            titles_list = ["标题", "作品id", "时间", "点赞", "评论", "格式", "收藏", "分享"]
            for title in titles_list:
                titles = titles + title + ":" + str(desc[title]) + "\n"

            printt(titles)

            file_exists = os.path.isfile("infor.csv")
            with open(file="infor.csv", mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=desc.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(desc)

    def time_count(self):
        time_end = time.time()
        time_diff = int(time_end - self.time_start)
        printt(f"共采集{self.nickname}的{self.video}个视频和{self.picture}个图片,耗时{time_diff}秒。")


async def main():
    url = "https://www.douyin.com/user/MS4wLjABAAAAgEH-b4e_8LP7q0lZkj-Je6Hkz0ncLAssUjeA5b2XnP4iziZtRlLTuU5iO6qW7nfl"
    cookie = "UIFID_TEMP=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e385280c23c7c48242b468a0c726cc174229b6b54066759308ba931c0bf2c372460f7abd1e0d13e7e34d63c75c63641f4010366; s_v_web_id=verify_lxkjpugn_jiF35RSY_NL5v_4jZk_BWJC_85iGJznjc4fd; passport_csrf_token=ab189923b0a230c3769979c05b45d435; passport_csrf_token_default=ab189923b0a230c3769979c05b45d435; fpk1=U2FsdGVkX18+k4vGpmE48bOsUwHcnRO07qEIWDgS8Ps4NgSK4T0Ja+4Zeh5IXjmo5Q7tjl2BKC4+36MnW0siHg==; fpk2=5f4591689f71924dbd1e95e47aec4ed7; bd_ticket_guard_client_web_domain=2; passport_assist_user=CkHkyn6-1sUx2Fkm5OtccBRDZhsMQI6ss9GS8t8qg4LewMs7ZrxVEXCWrvPBvvX1uIKQWr5k7UvqQnhWr2uoLlftLRpKCjwLrH-2dQaDt1f4L9ozmxfWPmSPb69mdZb9ooU0v5NOGjiK8f2u1rk3YNwE_UAUHqujN9EzWo5DsDBE5aQQ3K_UDRiJr9ZUIAEiAQMVKkUY; n_mh=kOWdes8h5KwAB7ZYvlwBX3e-HzkC3ZMjB1jH9Pr98mk; sso_uid_tt=5118dc8498c45d09f8cc502676bd06af; sso_uid_tt_ss=5118dc8498c45d09f8cc502676bd06af; toutiao_sso_user=1b3d854db42c504a4cf573bbb9b4d622; toutiao_sso_user_ss=1b3d854db42c504a4cf573bbb9b4d622; sid_ucp_sso_v1=1.0.0-KDM3OGMzOWY0Y2MwY2JkZDI0N2Y3MWZlMmFjZDdjMzViYzQ5OTU2NTMKIQiInMDkw8yABxDMycazBhjvMSAMMLmSj6IGOAZA9AdIBhoCbGYiIDFiM2Q4NTRkYjQyYzUwNGE0Y2Y1NzNiYmI5YjRkNjIy; ssid_ucp_sso_v1=1.0.0-KDM3OGMzOWY0Y2MwY2JkZDI0N2Y3MWZlMmFjZDdjMzViYzQ5OTU2NTMKIQiInMDkw8yABxDMycazBhjvMSAMMLmSj6IGOAZA9AdIBhoCbGYiIDFiM2Q4NTRkYjQyYzUwNGE0Y2Y1NzNiYmI5YjRkNjIy; uid_tt=cece1755837351268adca7f928788120; uid_tt_ss=cece1755837351268adca7f928788120; sid_tt=ae5c52a849a842c6e93c0c6efb191776; sessionid=ae5c52a849a842c6e93c0c6efb191776; sessionid_ss=ae5c52a849a842c6e93c0c6efb191776; UIFID=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e3852806ca46e10a829e621a8ada38d61ccc4cc2dce3df217730c5f8c53aa954498b70a78c7174f17605389dcbba30a7642c10937662fda8214bfd0846ac61a938af76dd213a97ea393cf951446ac32bc1fc20ecb6b2c69afc63dd1fae666300bfef8031dcdee261ea595c0498e8ec27dc2790e5f892969734b1aea6b2c38793fe3f2ce; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=4ac4a9813bf6d6b2c87005b239dfb0b6; __security_server_data_status=1; store-region=cn-hb; store-region-src=uid; SEARCH_RESULT_LIST_TYPE=%22single%22; my_rd=2; ttwid=1%7C61et_3dCOXH3jXOGBBwQeY-xS8JRS8zDDyaK9cH_GmM%7C1718956217%7C518c0e1215719781f20a1592aba7986fc78d60fd64bb44081e7560fe86db347d; live_use_vvc=%22false%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.4%7D; __live_version__=%221.1.2.1736%22; sid_guard=ae5c52a849a842c6e93c0c6efb191776%7C1720790604%7C5184000%7CTue%2C+10-Sep-2024+13%3A23%3A24+GMT; sid_ucp_v1=1.0.0-KDJjNTViY2U2ODQxZjhiMzU2MjkzYTg3NDM0NjJjZmQ1NDE0NzdlMTUKGwiInMDkw8yABxDM3MS0BhjvMSAMOAZA9AdIBBoCbGYiIGFlNWM1MmE4NDlhODQyYzZlOTNjMGM2ZWZiMTkxNzc2; ssid_ucp_v1=1.0.0-KDJjNTViY2U2ODQxZjhiMzU2MjkzYTg3NDM0NjJjZmQ1NDE0NzdlMTUKGwiInMDkw8yABxDM3MS0BhjvMSAMOAZA9AdIBBoCbGYiIGFlNWM1MmE4NDlhODQyYzZlOTNjMGM2ZWZiMTkxNzc2; FRIEND_NUMBER_RED_POINT_INFO=%22MS4wLjABAAAA_pPSY4citfPcMImtzzIOfhZ_QTMpTQPO6YxVtjsCS1mOBx4HrnycBCYPvmcChWUu%2F1720972800000%2F1720947948133%2F0%2F0%22; publish_badge_show_info=%220%2C0%2C0%2C1721217811757%22; pwa2=%220%7C0%7C3%7C0%22; dy_swidth=1536; dy_sheight=864; strategyABtestKey=%221721443812.269%22; WallpaperGuide=%7B%22showTime%22%3A1720306856080%2C%22closeTime%22%3A0%2C%22showCount%22%3A6%2C%22cursor1%22%3A611%2C%22cursor2%22%3A0%2C%22hoverTime%22%3A1718869866779%7D; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; csrf_session_id=9393b95e1cde7720622d39139e81f496; xg_device_score=6.8949924004391745; __ac_nonce=0669bab7e00db83921c43; __ac_signature=_02B4Z6wo00f01eQiNOgAAIDB0wbwt2A-a4XkAjBAAB-V5c; passport_fe_beating_status=true; download_guide=%223%2F20240618%2F0%22; EnhanceDownloadGuide=%220_0_1_1721478218_0_0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A1%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRHprUGtTTDRNcVVKT0pVTWtIZExGUmhVblE1Wmt4bHNjTjJ0OFlTKzZqSlY5S1EyNGRqRUovTXY4OGdTcUVvZ1lVYWkvTFRJZEhrc2Y2dmtxS052SXM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; IsDouyinActive=true; odin_tt=7a382098a5a002424770f952acff42a159dbafdc328b29022d05928cf63a2f145836c0f26b435075a1ab3fc709d25f34"
    user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]

    task = Task(user_id, cookie)
    await task.run()
    task.time_count()


if __name__ == '__main__':
    asyncio.run(main())
