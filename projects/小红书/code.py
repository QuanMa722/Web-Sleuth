# -*- coding: utf-8 -*-

import requests
import execjs
import json
import time

js_code = open('xhs.js', encoding='utf-8').read()
ctx = execjs.compile(js_code)


def get_data(cookie_input, pid, cursor):
    global ctx

    url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={pid}&cursor={cursor}"

    x_t = int((time.time() + 8) * 1000)
    x_s = ctx.call('get_x',
                   str(x_t) + 'test/api/sns/web/v2/comment/page?note_id=' + str(pid) + '&cursor=' + str(cursor))

    headers = {
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/108.0.0.0 "
                      "Safari/537.36",
        "cookie": cookie_input,
        "accept": "application/json",
        "content-type": "application/json;charset=utf-8",
        "x-s": x_s,
        "x-t": str(x_t),
    }

    try:
        response = requests.get(headers=headers, url=url)
        resp_json = json.loads(response.text, strict=False)

        datas = resp_json['ming']
        cur = datas['cursor']

        for data in datas['comments']:
            comment_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['create_time'] // 1000)))

            comment_dict = {
                '用户id': data['id'],
                '用户名': data['user_info']["nickname"],
                '评论时间': comment_time,
                '评论内容': data['content']
            }

            print(comment_dict)

        get_data(cookie_input, pid, cur)

    except Exception as error:
        print(f"An error occurred: {error}.")
        print(f"Data collection complete.")


if __name__ == '__main__':
    note_pid: str = input("note_pid:")
    cookie: str = input("cookie:")
    get_data(cookie, note_pid, '')
