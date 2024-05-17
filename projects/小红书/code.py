# -*- coding: utf-8 -*-

import requests
import execjs
import json
import time

js_code = open('xhs.js', encoding='utf-8').read()
ctx = execjs.compile(js_code)

dits = []


def crawler(pid, cursor):
    global dits, ctx

    url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={pid}&cursor={cursor}"

    time.sleep(1)
    x_t = int((time.time() + 8) * 1000)
    x_s = ctx.call('get_x',
                   str(x_t) + 'test/api/sns/web/v2/comment/page?note_id=' + str(pid) + '&cursor=' + str(cursor))

    headers = {
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/108.0.0.0 "
                      "Safari/537.36",
        "cookie": "abRequestId=03094479-9d33-501e-a399-e8d008763acd; "
                  "a1=18ea945a65510lprn15giv3p8z78snya3qdr6u2gd50000397430; webId=19f1eb38bb76c6c7d9a9b433f1ddf400; "
                  "gid=yYd0j4204iqWyYd0j420KA7J22y81UFIy2k3fkfhqUYuWF28YMIv0K888qjW4q888JDKS2qY; "
                  "web_session=040069b278ff821a4abfc14c0f344b9896faaf; "
                  "acw_tc=01c981036bd0ee811f2639e6605991eb03f67770e6ee7f26663df052bacdf507; webBuild=4.16.0; unread={"
                  "%22ub%22:%2266457fed000000001e0325a7%22%2C%22ue%22:%22663f4f01000000001e02d6e2%22%2C%22uc%22:25}; "
                  "xsecappid=open-api; websectiga=cffd9dcea65962b05ab048ac76962acee933d26157113bb213105a116241fa6c; "
                  "sec_poison_id=e19050e8-88e7-4100-86c5-a1db36f7a290",
        "accept": "application/json",
        "content-type": "application/json;charset=utf-8",
        # "x-b3-traceid":"0fa5414ce957aa16",
        "x-s": x_s,
        "x-t": str(x_t),
    }

    try:
        response = requests.get(headers=headers, url=url)
        resp_json = json.loads(response.text, strict=False)

        datas = resp_json['data']
        cur = datas['cursor']

        for data in datas['comments']:

            comment_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['create_time'] // 1000)))
            dit = {
                '用户id': data['id'],
                '用户': data['user_info']["nickname"],
                '评论日期': comment_time,
                '评论内容': data['content']
            }
            if data['content'][0] == '@':
                continue
            else:
                dits.append(dit)
            print(dit)
        crawler(pid, cur)
    except Exception as e:
        print(e)
        return
    return

    # print(dit)


if __name__ == '__main__':
    note_pit: str = "662f3fa70000000001006207"
    crawler(note_pit, '')
