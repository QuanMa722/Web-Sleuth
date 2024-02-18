
# -*- coding: utf-8 -*-
# https://www.biqg.cc

from selenium.webdriver.common.by import By
from selenium import webdriver

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


edge_driver_path = r"D:\APP\edgedriver_win64\msedgedriver.exe"
driver = webdriver.Edge(executable_path=edge_driver_path, capabilities=edge_none)


def get_infor(book_id, page_num):

    url = f"https://www.biqg.cc/book/{book_id}/{page_num}.html"
    driver.get(url)

    find_title = driver.find_element(By.XPATH, '//*[@id="read"]/div[2]/span').text
    print(find_title)

    find_text = driver.find_element(By.XPATH, '//*[@id="chaptercontent"]')
    text_lines = find_text.text.split('\n')[:-4]
    updated_text = '\n'.join(text_lines)

    print(updated_text)

    driver.quit()


if __name__ == '__main__':
    try:
        book_id = int(input("id:"))
        page_num = int(input("page:"))
        get_infor(book_id, page_num)
    except Exception as e:
        print(f"An error occurred: {e}")



