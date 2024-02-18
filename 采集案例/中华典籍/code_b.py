
# -*- coding: utf-8 -*-
# 采集中华典籍网书籍(https://www.zhonghuadiancang.com/lishizhuanji/mingshi)
# 多线程

# 导入需要的第三方库
from bs4 import BeautifulSoup  # 定位元素
from urllib import request  # 发送请求
import concurrent.futures  # 多线程


def get_process(num: int) -> None:
    """
    多线程的目标函数，用于获取文本信息

    :param num: int 章节的数字
    :return: None
    """

    try:
        # 定义初始url,根据需求调整采集的url
        # https://www.zhonghuadiancang.com/ + lishizhuanji  / + mingshi  / + num  .html
        url = f"https://www.zhonghuadiancang.com/lishizhuanji/mingshi/{num}.html"

        # 发送请求，获得回应
        response = request.urlopen(url)

        # 使用bs4解析并定位信息
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')

        # 获取标题文本并去除空行
        title = soup.find('h1').get_text().strip()
        # 获取正文文本并去除空行
        text = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()

        print(f"{title}已采集完毕。")  # 可选择打印，检验是否出现问题

        # 根据需求存储数据
        get_file(title, text)

    # 根据报错信息修改代码
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def get_file(title: str, text: str) -> None:
    """
    将数据存储到文件中

    :param title: str 标题
    :param text: str 正文
    :return:
    """

    # \表示转义
    with open("E:\\Book\\" + title + ".txt", "w", encoding="utf-8") as f:
        f.write(text)

    return None


def main() -> None:
    """
    主函数，用于控制整个程序流程
    """
    while True:
        # 输入开始章节和结束章节
        try:
            start_num = int(input("start_num:"))
            end_num = int(input("end_num:"))
            # 构建多线程
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(get_process, range(start_num, end_num + 1))
                break  # 输入合法，跳出循环
        # 根据报错信息修改代码
        except Exception as e:
            print(f"An error occurred: {e}")

    return None


if __name__ == '__main__':
    main()
















