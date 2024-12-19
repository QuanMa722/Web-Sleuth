# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import time
import re


class Task:
    def __init__(self, user_id, cookie):
        self.max_cursor = 10000000000000
        self.user_id = user_id
        self.cookie = cookie
        self.has_more = True

    def run(self):
        while self.has_more:
            self.task()

    def task(self):
        form = f'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={self.user_id}&max_cursor={self.max_cursor}&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'

        ua = UserAgent()
        headers = {
            'referer': f'https://www.douyin.com/user/{self.user_id}',
            'cookie': self.cookie,
            'User-Agent': ua.random,
        }

        url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?{form}'

        try:
            response = requests.get(url=url, headers=headers, timeout=5)

            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                return

            # Try to parse the response as JSON
            try:
                resp_data = response.json()
            except Exception as e:
                print(f"Error: Failed to parse JSON - {str(e)}")
                return



            self.save_data(resp_data)

            if not resp_data["has_more"]:
                self.has_more = False

            self.max_cursor = resp_data["max_cursor"]

        except requests.exceptions.Timeout:
            print("Error: Request timed out.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def save_data(self, data):

        for aweme in data["aweme_list"]:

            print(data["aweme_list"])

            desc = aweme["statistics"]
            desc['标题'] = aweme['desc']
            desc['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(aweme["create_time"])))
            desc['点赞'] = desc.pop('digg_count')
            desc['评论'] = desc.pop('comment_count')
            desc['收藏'] = desc.pop('collect_count')
            desc['分享'] = desc.pop('share_count')
            desc['作品id'] = aweme["aweme_id"]

            del desc['play_count']
            del desc['admire_count']

            titles = ""
            titles_list = ["标题", "作品id", "时间", "点赞", "评论", "收藏", "分享"]
            for title in titles_list:
                titles = titles + title + ":" + str(desc[title]) + "\n"

            print(titles)

            with open('test.txt', mode='a', encoding='utf-8') as f:
                f.write(str(aweme['aweme_id']) + '\n')
                # print(aweme['aweme_id'])


def main():
    url = 'https://www.douyin.com/user/MS4wLjABAAAAxYcKrjJ4v-rc94zGwc4FJf9jC2dJw-lphcBBMRZP33o?from_tab_name=main&vid=7449991968697896243'
    cookie = 'ttwid=1%7CQSyuQr84dBFl_G4Yqd_V-1Wlc7IwZwfFqlsQcOWjF2w%7C1733235578%7C77d4ed24d393188ddb4f79cec35221a8b7fb418eafc8667fea8f4516744e734b; UIFID_TEMP=26198ff38959f773c63a6fc9b3542e2fdcfd2f10d2782124ed1adc24709862dfbd15a98532905ba2e8cb7e62d86be6954f0254493ce2aef54e62c2a44ea41fe7968bca68ec2e421929994f045f8efb3b; s_v_web_id=verify_m48jpokd_4xOaHe85_9Vth_4SdF_BLWp_78lAWJ0KKoWy; dy_swidth=1536; dy_sheight=864; hevc_supported=true; WebUgChannelId=%2230001%22; fpk1=U2FsdGVkX19TMJePN1V4foOrTnH1EdZR0tOYpQU8Laya4GoUikn0+svqBWg7owrkKNXoNp9C7LWTOLG/lRs3Rg==; fpk2=ffc3218438300d069a0fd5dfa5c6e851; xgplayer_user_id=931292163593; passport_csrf_token=90c97b2ba6f453ccbdd4087fc6d6d744; passport_csrf_token_default=90c97b2ba6f453ccbdd4087fc6d6d744; bd_ticket_guard_client_web_domain=2; passport_mfa_token=CjeOqpO%2FTO3pHtzeyYXV6oQ%2F%2F3p84Nektgg7QxMsnxPMywEikEZY1d6xzUABvy5p%2BcEj40UJKar6GkoKPCSuja7Bu3ZniYXCrNl%2F0JCTSmXYqE3HCucwK8D%2FK2plzHWNZF%2BSHTLd16xqkb3n62oAWVJdFSBdOuDD9RDAj%2BMNGPax0WwgAiIBA59YXZ4%3D; d_ticket=6ec488247d7213d843038f0169d8d4d5e8836; passport_assist_user=CkFE-wv4claDaVpAfTwlL0y_orKJD_YTqnFYYK1POqHwo4Mift2koJBjbDL9GYU3cV_gEGTV2hp9rwHenTpxAxGy4BpKCjzx_ORc36c93zI0xXf6ZlEuvjp5v371_7pzLmPyYr2KzbMcZDZRDkplV-ej013ME_fsyWvXsbFYaRVSh1gQzpHjDRiJr9ZUIAEiAQPCbhxH; n_mh=kOWdes8h5KwAB7ZYvlwBX3e-HzkC3ZMjB1jH9Pr98mk; sso_auth_status=6ffafbbc9d463891481d3bcd5038db28; sso_auth_status_ss=6ffafbbc9d463891481d3bcd5038db28; sso_uid_tt=07c2e9f20071f4a010effa6744eed021; sso_uid_tt_ss=07c2e9f20071f4a010effa6744eed021; toutiao_sso_user=2d69b9d989b65dad6be6f6edd4491652; toutiao_sso_user_ss=2d69b9d989b65dad6be6f6edd4491652; sid_ucp_sso_v1=1.0.0-KGFlNjEzNTM1MzBhY2YwYzE0ZjM0ZTkzOGY5MmE4NWQ4ZWYwOTYzY2UKIQiInMDkw8yABxCkp7y6BhjvMSAMMLmSj6IGOAJA8QdIBhoCbHEiIDJkNjliOWQ5ODliNjVkYWQ2YmU2ZjZlZGQ0NDkxNjUy; ssid_ucp_sso_v1=1.0.0-KGFlNjEzNTM1MzBhY2YwYzE0ZjM0ZTkzOGY5MmE4NWQ4ZWYwOTYzY2UKIQiInMDkw8yABxCkp7y6BhjvMSAMMLmSj6IGOAJA8QdIBhoCbHEiIDJkNjliOWQ5ODliNjVkYWQ2YmU2ZjZlZGQ0NDkxNjUy; login_time=1733235620055; passport_auth_status=a1cae1b0cea1319d2952bc84740480d2%2C65da45c54d70c04ab81dfc9f16d8d649; passport_auth_status_ss=a1cae1b0cea1319d2952bc84740480d2%2C65da45c54d70c04ab81dfc9f16d8d649; uid_tt=481829cb1fc1712cf8f87168c5503e42; uid_tt_ss=481829cb1fc1712cf8f87168c5503e42; sid_tt=bfd7bec4305ea1409caf35107eaa25a6; sessionid=bfd7bec4305ea1409caf35107eaa25a6; sessionid_ss=bfd7bec4305ea1409caf35107eaa25a6; is_staff_user=false; UIFID=26198ff38959f773c63a6fc9b3542e2fdcfd2f10d2782124ed1adc24709862dfbd15a98532905ba2e8cb7e62d86be6952b8c88e63be198afa7facf7ea91009e87e2ca9a9526fd9a33641753ae9a97f837a9c84943df70e73cb68507841ef5ee53036857f54c1b3e4f2f51b4fe79a7ab7c61cb21571e859436207fc9f1c2a19fa2ffe8ed0d16e43ea8b05b1cbf2cc8ee487a52f10c1bf6da9bffefe7dfca7c196; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=2bd2ed074cbfae4f04bdb29d56460975; SelfTabRedDotControl=%5B%5D; __security_server_data_status=1; sid_guard=bfd7bec4305ea1409caf35107eaa25a6%7C1733235624%7C5183998%7CSat%2C+01-Feb-2025+14%3A20%3A22+GMT; sid_ucp_v1=1.0.0-KDkyZTk2ZTUxYzBhNzJmMTZmZWMyOWJjNjk3NmQ0YTA0MDEwZGM1YzAKGwiInMDkw8yABxCop7y6BhjvMSAMOAJA8QdIBBoCbGYiIGJmZDdiZWM0MzA1ZWExNDA5Y2FmMzUxMDdlYWEyNWE2; ssid_ucp_v1=1.0.0-KDkyZTk2ZTUxYzBhNzJmMTZmZWMyOWJjNjk3NmQ0YTA0MDEwZGM1YzAKGwiInMDkw8yABxCop7y6BhjvMSAMOAJA8QdIBBoCbGYiIGJmZDdiZWM0MzA1ZWExNDA5Y2FmMzUxMDdlYWEyNWE2; is_dash_user=1; xgplayer_device_id=93540110003; store-region=cn-hb; store-region-src=uid; my_rd=2; publish_badge_show_info=%221%2C0%2C0%2C1734012871555%22; download_guide=%223%2F20241213%2F0%22; live_use_vvc=%22false%22; h265ErrorNum=-1; __live_version__=%221.1.2.6260%22; live_can_add_dy_2_desktop=%221%22; SEARCH_RESULT_LIST_TYPE=%22single%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; pwa2=%220%7C0%7C0%7C1%22; WallpaperGuide=%7B%22showTime%22%3A1734528627439%2C%22closeTime%22%3A0%2C%22showCount%22%3A5%2C%22cursor1%22%3A107%2C%22cursor2%22%3A34%2C%22hoverTime%22%3A1733236136137%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA_pPSY4citfPcMImtzzIOfhZ_QTMpTQPO6YxVtjsCS1mOBx4HrnycBCYPvmcChWUu%2F1734537600000%2F0%2F0%2F1734536712079%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA_pPSY4citfPcMImtzzIOfhZ_QTMpTQPO6YxVtjsCS1mOBx4HrnycBCYPvmcChWUu%2F1734537600000%2F0%2F1734536051001%2F0%22; strategyABtestKey=%221734583835.433%22; __ac_signature=_02B4Z6wo00f01Z944KgAAIDBqFwk9iMjTRGfWOQAAAC-91; douyin.com; xg_device_score=7.643364542677078; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; csrf_session_id=bee2ad4ebd55e111bbf493f56fce4d96; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQXRrZ2UzV01BckVNOXRXUzNCR0VpemhVVVdyZGlOdnpBY1lhK1VEMGN0NWV6dER4MmtHNWpYNktvVjRHVE42RHFZdXZoTXFoemJIN2ZtbGxJa0F2K2M9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; odin_tt=3353628763ee6ee50d249d338f5ac144fcf1ed8f610e5b669e668210d92718c0440134b8fad19ef5d6a86181a5bf208d; passport_fe_beating_status=true; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; IsDouyinActive=true; __ac_nonce=06763d4e300adce94b327'
    user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]

    task = Task(user_id, cookie)
    task.run()


if __name__ == '__main__':
    main()
