# -*- coding: utf-8 -*-

from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

opt = Options()
opt.add_argument('--headless')
driver = webdriver.Edge(options=opt)


def get_data():
    url = "http://www.hxlib.cn/book/a519487a2ececa4eedee995d126c745b.html"
    driver.get(url)

    for index in range(0, 800):
        driver.switch_to.window(driver.window_handles[index])

        time.sleep(3)

        find_text = driver.find_element(By.XPATH, '//*[@id="Ls"]/div[2]/div/div/div[1]/ul/li[2]/p/font/b/span/a')
        find_text.click()

        find_text = driver.find_element(By.XPATH, '//*[@id="Ls"]/div[2]/div/div/div[1]/div/font/div')

        new_txt = ""

        for item in find_text.text:
            try:
                new_txt += str(item)
            except Exception as error_word:
                print(f"Error: {error_word}. Skipping this word.")

        print(new_txt)


if __name__ == '__main__':
    try:
        get_data()
    except Exception as e:
        print(f"An error occurred: {e}")



