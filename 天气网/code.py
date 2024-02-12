
# -*- coding: utf-8 -*-
# 采集天气网历史天气数据
# selenium

from selenium.webdriver.common.by import By  # 用于定位元素
from selenium import webdriver  # 实例化webdriver
import datetime  # 获取当前时间
import random  # 设置随机数
import time  # 休息几秒


# 设置 Edge 驱动参数，不显示页面
edge_none = {
    "browserName": "MicrosoftEdge",
    "version": "121.0.2277.112",
    "platform": "WINDOWS",
    "ms:edgeOptions": {
        'extensions': [],
        'args': [
            '--headless',
            '--disable-gpu'
        ]}
}

# Edge 驱动路径
edge_driver_path = r"D:\APP\edgedriver_win64\msedgedriver.exe"

# 初始化 WebDriver 对象
driver = webdriver.Edge(executable_path=edge_driver_path, capabilities=edge_none)


def get_date():
    """
    获取当前年份和月份的函数
    :return: month_day_dict, current_year, current_month
    """
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
    """
    获取单个月份数据的函数
    :param city: 城市名
    :param year: 年份
    :param month: 月份
    :param month_day_dict: 包含每月天数的字典
    """

    try:
        # 初始url
        url = f"https://lishi.tianqi.com/{city}/{year}{month}.html"

        driver.get(url)
        # 定位按钮并点击按钮
        button = driver.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[4]/ul/div")
        button.click()

        # 循环对应月的天数
        for days in range(1, int(month_day_dict[month]) + 1):
            # 定位温度数据
            text_origin = driver.find_element(By.XPATH, f"/html/body/div[7]/div[1]/div[4]/ul/li[{days}]").text
            # 构建一个列表
            text_list = text_origin.split('\n')
            # 可选择打印是否有问题
            print(text_list)
            # 写入csv文件中，可根据需求自由修改
            get_txt(city, text_list)
        # 关闭浏览器
        driver.quit()
    except Exception as e:
        # 一般报错是因为缺失数据
        print("报错: 数据缺失，无法定位")
        print(e)


def get_data(city, year, month_day_dict):
    """
    获取全年数据的函数
    :param city: 城市名
    :param year: 年份
    :param month_day_dict: 包含每月天数的字典
    """
    try:
        # 循环全年的月
        for every_month in list(month_day_dict.keys()):
            # 初始url
            url = f"https://lishi.tianqi.com/{city}/{year}{every_month}.html"

            driver.get(url)
            # 寻找按钮并点击
            button = driver.find_element(By.XPATH, "/html/body/div[7]/div[1]/div[4]/ul/div")
            button.click()
            # 循环天数
            for days in range(1, int(month_day_dict[every_month]) + 1):
                text_origin = driver.find_element(By.XPATH, f"/html/body/div[7]/div[1]/div[4]/ul/li[{days}]").text

                text_list = text_origin.split('\n')
                # 打印数据
                print(text_list)
                # 根据需求写入文件中
                get_txt(city, text_list)
            # 休息的秒数
            num_break = random.randint(1, 3)
            print(f"第{every_month}月已采集完毕，休息{num_break}秒。")
            time.sleep(num_break)

    except Exception as e:
        # 一般报错是因为缺失数据
        print("报错: 数据缺失，无法定位")
        print(e)
    driver.quit()


def get_txt(city, text_list):
    """
    将数据写入文件的函数
    :param city: 城市名
    :param text_list: 文本列表
    """
    with open(f"{city}.txt", "a") as f:
        f.write(str(text_list) + "\n")

    return None


def main():
    """
    主函数，用于获取用户输入并调用相应函数
    """
    # 获取相关数据
    month_day_dict, current_year, current_month = get_date()
    # 获取正确的输入
    while True:
        try:
            print("eg: wuhan")
            city = input("请输入城市:")

            print("eg: 2023")
            year = input("请输入年份:")

            print("eg: 07")
            month = input("请输入月份(默认为全年数据):")
            # 判断是否超出时间线
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

    # 如何month不为空
    if month:
        get_single_data(city, year, month, month_day_dict)
    else:
        # 由于今年的数据还没有更新，故采用循环单月获取数据
        if year == current_year:
            # 获取对于月的字符串
            month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            for month in month_list[0: current_month]:
                get_single_data(city, year, month, month_day_dict)
        else:
            get_data(city, year, month_day_dict)


if __name__ == '__main__':
    # 运行主函数
    main()