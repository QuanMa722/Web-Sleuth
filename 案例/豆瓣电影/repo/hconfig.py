# -*- coding: utf-8 -*-

from fake_useragent import UserAgent

class HeadCook:

    ua = UserAgent()

    cookies = {
        'bid': '1gMxgR_xU5U',
        'll': '"118282"',
        'Hm_lvt_19fc7b106453f97b6a84d64302f21a04': '1733372099',
        '_ga_PRH9EWN86K': 'GS1.2.1733372100.1.0.1733372100.0.0.0',
        '_pk_id.100001.4cf6': '024b110d1382e475.1733372159.',
        '__yadk_uid': 'qBGjSnLZknbXZA3ugKLSpQd9RbCSfoz1',
        '_vwo_uuid_v2': 'D8DB7696A3F6AD5AF442F89BBAA685C83|ba3269f7a883157ff71737fd00d2c8c0',
        'push_noty_num': '0',
        'push_doumail_num': '0',
        'dbcl2': '"224267170:dxEUEjAsXKc"',
        '_ga': 'GA1.1.857826835.1733372040',
        '_ga_Y4GN1R87RG': 'GS1.1.1735141304.2.1.1735141359.0.0.0',
        'ck': 'X8kM',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1735269501%2C%22https%3A%2F%2Fm.douban.com%2F%22%5D',
        '_pk_ses.100001.4cf6': '1',
        'ap_v': '0,6.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
    }
