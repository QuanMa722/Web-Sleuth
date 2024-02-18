
# -*- coding: utf-8 -*-
# 采集笔趣阁小说(https://www.biqg.cc)
# selenium

# 导入需要的第三方库
from selenium.webdriver.common.by import By  # 用于定位元素
from selenium import webdriver  # 构建实例
import time  # 休息几秒

# 设置edge相关信息
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

# 指定msedgedriver路径
edge_driver_path = r"D:\APP\edgedriver_win64\msedgedriver.exe"
# 设置路径和无头信息
driver = webdriver.Edge(executable_path=edge_driver_path, capabilities=edge_none)


def get_infor(book_id: int, page_start: int, page_end: int) -> None:
    """
    获取小说文本

    :param book_id: int 小说id
    :param page_start: int 开始页面
    :param page_end: int 结束页面
    :return:
    """

    # 遍历页面
    for page in range(page_start, page_end + 1):

        time.sleep(1)  # 休息一秒，防止被限制

        url = f"https://www.biqg.cc/book/{book_id}/{page}.html"
        driver.get(url)

        # 获取标题
        find_title = driver.find_element(By.XPATH, '//*[@id="read"]/div[2]/span').text
        # 获取正文
        find_text = driver.find_element(By.XPATH, '//*[@id="chaptercontent"]')
        # 处理正文
        text_lines = find_text.text.split('\n')[:-4]
        updated_text = '\n'.join(text_lines)

        print(updated_text)

        # 写入文件中
        get_file(find_title, updated_text)
    # 关闭浏览器
    driver.quit()
    return None


def get_file(find_title: str, find_text: str) -> None:
    """
    将数据写入文件中

    :param find_title: str 标题
    :param find_text: str 正文
    :return: None
    """

    # 根据需求选择写入的文件
    with open("book.txt", "a", encoding="utf-8") as f:

        f.write(find_title + "\n")
        f.write(find_text + "\n")

    return None


def main():
    """
    主函数，用于控制整个程序流程
    """
    while True:
        try:
            # 输入小说的id
            book_id = int(input("id:"))
            # 获取url的开始数字
            page_start = int(input("起始章节:"))
            # 获取url的结束数字
            page_end = int(input("结束章节:"))

            # 获取数据
            get_infor(book_id, page_start, page_end)
            break  # 输入合法，跳出循环
        # 根据报错信息修改代码
        except Exception as e:
            print(f"An error occurred: {e}")

    print("数据采集完毕！")


if __name__ == '__main__':
    main()



