
# -*- coding: utf-8 -*-
# https://www.yt1998.com/priceInfo.html

from fake_useragent import UserAgent
import requests
import json
import re


def get_infor():

    url = "https://www.yt1998.com/price/nowDayPriceQ!getPriceList.do"

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    params = {
        'random': '0.35934104418089574',
        'ycnam': '',
        'market': '1',
        'leibie': '',
        'istoday': '0',
        'spices': '',
        'tea': '',
        'logo_flg': '',
        'paramName': '',
        'paramValue': '',
        'pageIndex': 0,
        'pageSize': '20',
    }

    response = requests.get(url=url, headers=headers, params=params)

    resp_dict = json.loads(response.text)["data"]
    item = resp_dict[0]

    data_dict = {
        "品名": item["ycnam"],
        "规格": item["guige"],
        "产地": item["chandi"],
        "价格（元/kg）": item["pri"],
        "走势": item["zoushi"],
        "昨日对比": re.search(r'>(.*?)<', item["yesterday"]).group(1),
        "周对比": re.search(r'>(.*?)<', item["zhouduibi"]).group(1),
        "月对比": re.search(r'>(.*?)<', item["yueduibi"]).group(1),
        "季度对比": re.search(r'>(.*?)<', item["jiduibi"]).group(1),
        "年对比": re.search(r'>(.*?)<', item["nianduibi"]).group(1),
        "日期": item["dtm"],
    }

    return data_dict


if __name__ == '__main__':

    data_dict = get_infor()
    print(data_dict)








