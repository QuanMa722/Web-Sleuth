# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import time
import json
import re


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime(int(time.time())))
    msgs = msg.split("\n")
    for word in msgs:
        print("[" + nowt + "] " + str(word))


def get_resp():
    max_cursor = int(time.time() * 1000)

    form = f'device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={user_id}&max_cursor={max_cursor}&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'
    xb_resp = requests.get("http://xbogus.tom14.top/", params={"form": form}, timeout=3)
    xb = xb_resp.json()

    url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?{form}&X-Bogus={xb["data"]["X_Bogus"]}'
    resp = requests.get(url, headers=headers, timeout=3)
    resp_json = resp.json()

    return resp_json


def get_video(resp_json, aweme_id):
    for aweme in resp_json["aweme_list"]:
        desc = aweme["statistics"]
        if aweme["aweme_id"] == str(aweme_id):

            desc['作者'] = resp_json["aweme_list"][0]["author"]["nickname"]
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
                video = requests.get(url=video_url, headers=headers)
                with open(file="video.mp4", mode='wb') as f:
                    f.write(video.content)

                printt("已完成视频的下载。")
                break
            else:
                desc['格式'] = "picture"
                titles = ""
                titles_list = ["标题", "作品id", "时间", "点赞", "评论", "格式", "收藏", "分享"]
                for title in titles_list:
                    titles = titles + title + ":" + str(desc[title]) + "\n"

                printt(titles)
                count = 0
                for image in aweme["images"]:
                    count += 1
                    image_url = image["url_list"][-1]
                    video = requests.get(url=image_url, headers=headers)
                    with open(file=f"picture_{count}.jpeg", mode='wb') as f:
                        f.write(video.content)

                printt("已完成图片的下载。")
                break
        else:
            continue


if __name__ == '__main__':

    with open(file='config.json', mode='r') as f:
        configs = json.load(f)

    url = configs['url']
    cookie = configs['cookie']
    aweme_id = configs['aweme_id']

    user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]

    ua = UserAgent()
    headers = {
        'referer': f'https://www.douyin.com/user/{user_id}',
        'cookie': cookie,
        'User-Agent': ua.random,
    }
    
    resp_json = get_resp()
    get_video(resp_json, aweme_id)
