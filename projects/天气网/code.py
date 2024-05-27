# -*- coding: utf-8 -*-

from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
import random
import time

opt = Options()
opt.add_argument('--headless')
driver = webdriver.Edge(options=opt)


def get_date():
    month_day_dict = {
        "01": "31",
        "02": "28",
        "03": "31",
        "04": "30",
        "05": "31",
        "06": "30",
        "07": "31",
        "08": "31",
        "09": "30",
        "10": "31",
        "11": "30",
        "12": "31",
    }

    current = datetime.datetime.now()
    current_year = current.year
    current_month = current.month

    return month_day_dict, current_year, current_month


def get_single_data(city, year, month, month_day_dict):
    try:
        url = f"https://lishi.tianqi.com/{city}/{year}{month}.html"
        driver.get(url)
        button = driver.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[4]/ul/div")
        button.click()

        for days in range(1, int(month_day_dict[month]) + 1):
            text_origin = driver.find_element(By.XPATH, f"/html/body/div[7]/div[1]/div[4]/ul/li[{days}]").text
            text_list = text_origin.split('\n')

            print(text_list)

            get_txt(city, text_list)
        driver.quit()
    except Exception as error:
        print("报错: 数据缺失，无法定位")
        print(error)


def get_data(city, year, month_day_dict):
    try:

        for every_month in list(month_day_dict.keys()):
            url = f"https://lishi.tianqi.com/{city}/{year}{every_month}.html"

            driver.get(url)

            button = driver.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[4]/ul/div")
            button.click()

            for days in range(1, int(month_day_dict[every_month]) + 1):
                text_origin = driver.find_element(By.XPATH, f"/html/body/div[7]/div[1]/div[4]/ul/li[{days}]").text

                text_list = text_origin.split('\n')
                print(text_list)
                get_txt(city, text_list)

            num_break = random.randint(1, 3)
            print(f"第{every_month}月已采集完毕，休息{num_break}秒。")
            time.sleep(num_break)

    except Exception as error:
        print("报错: 数据缺失，无法定位")
        print(error)
    driver.quit()


def get_txt(city, text_list):
    with open(f"{city}.txt", "a") as f:
        f.write(str(text_list) + "\n")

    return None


def main():
    month_day_dict, current_year, current_month = get_date()

    while True:
        try:
            print("eg: wuhan")
            city = input("请输入城市:")

            print("eg: 2023")
            year = input("请输入年份:")

            print("eg: 07")
            month = input("请输入月份(默认为全年数据):")

            if month:
                if int(year) > current_year or (year == current_year and int(month) > current_month):
                    print("时间错误，请重新输入。")
                else:
                    year = int(year)
                    month = str(month)
                    break
            else:
                if int(year) > current_year:
                    print("时间错误，请重新输入。")
                else:
                    year = int(year)
                    month = str(month)
                    break
        except Exception as e:
            print(e)

    if month:
        get_single_data(city, year, month, month_day_dict)
    else:
        if year == current_year:
            month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            for month in month_list[0: current_month]:
                get_single_data(city, year, month, month_day_dict)
        else:
            get_data(city, year, month_day_dict)


if __name__ == '__main__':
    main()
