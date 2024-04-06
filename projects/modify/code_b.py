import time

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


def get_infor():
    url = "http://www.hxlib.cn/book/a519487a2ececa4eedee995d126c745b.html"
    driver.get(url)

    for i in range(0, 800):
        driver.switch_to.window(driver.window_handles[i])
        time.sleep(3)
        find_text1 = driver.find_element(By.XPATH, '//*[@id="Ls"]/div[2]/div/div/div[1]/ul/li[2]/p/font/b/span/a')
        find_text1.click()

        find_text = driver.find_element(By.XPATH, '//*[@id="Ls"]/div[2]/div/div/div[1]/div/font/div')

        new_txt1 = ""
        try:
            for i in find_text.text:
                try:
                    print(i)
                    new_txt1 += str(i)
                except Exception as error_word:
                    print(f"Error: {error_word}. Skipping this word.")
        except Exception as error:
            print(f"An error occurred: {error}")

        print(new_txt1)
        get_file(new_txt1)


def get_file(new_text):

    with open("book.txt", "a", encoding="utf-8") as f:
        f.write(new_text + "\n")

    return None


if __name__ == '__main__':
    try:
        get_infor()
    except Exception as e:
        print(f"An error occurred: {e}")



