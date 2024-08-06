# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait  #
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib import request
import random
import time
import cv2
import re

driver = webdriver.Edge()


def get_image() -> str:

    url = "https://accounts.douban.com"

    driver.get(url)

    time.sleep(1)

    # click on "Password Login"
    button_switch_password = driver.find_element(By.XPATH, "//*[@id='account']/div[2]/div[2]/div/div[1]/ul[1]/li[2]")
    button_switch_password.click()

    time.sleep(1)

    # enter email and password (random)
    button_mail_input = driver.find_element(By.XPATH, "//*[@id='username']")
    button_mail_input.send_keys("88888888@qq.com")

    time.sleep(1)

    button_password_input = driver.find_element(By.XPATH, "//*[@id='password']")
    button_password_input.send_keys("88888888")

    time.sleep(1)

    # click to login
    button_click = driver.find_element(By.XPATH, "//*[@id='account']/div[2]/div[2]/div/div[2]/div[1]/div[4]/a")
    button_click.click()
    driver.implicitly_wait(5000)

    time.sleep(1)

    # getting the image and positioning it
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="tcaptcha_iframe_dy"]'))
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "slideBg")))

    image_src = driver.find_element(By.ID, 'slideBg')
    image_src_new = image_src.get_attribute('style')

    find_src_re = r'background-image: url\(\"(.*?)\"\);'
    image_src_last = re.findall(find_src_re, image_src_new, re.S)[0]

    if image_src_last.find("https") == -1:
        image_src_last = "https://t.captcha.qq.com" + image_src_last

    image_path = "origin.png"

    request.urlretrieve(image_src_last, image_path)

    return image_path


def get_distance(image):

    image_process = cv2.imread(image)

    # 算法
    blurred = cv2.GaussianBlur(image_process, (5, 5), 0)
    canny = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)

        if 5025 < area < 7215 and 300 < perimeter < 380:
            cv2.rectangle(image_process, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite("output.jpg", image_process)
            return x


def get_move(distance):

    distance_process = int(int(distance) * 340 / 672)
    button_move = driver.find_element(By.XPATH, '//*[@id="tcOperation"]/div[6]')
    x_coordinate = button_move.location['x']

    print(f"the initial distance: {x_coordinate}")

    distance_gap = distance_process - x_coordinate
    driver.implicitly_wait(2000)
    ActionChains(driver).click_and_hold(button_move).perform()
    count_num = 1
    moved = 0
    while moved < distance_gap:
        move_x = random.randint(5, 10)
        moved += move_x
        time.sleep(1)
        ActionChains(driver).move_by_offset(xoffset=move_x, yoffset=0).perform()

        print(f"the {count_num}th move, with a distance of {move_x} and a position of {button_move.location['x']}/{distance_process}")
        count_num += 1

    ActionChains(driver).release().perform()

    button_click = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[5]/a")
    button_click.click()

    time.sleep(5)
    driver.quit()


if __name__ == '__main__':

    image = get_image()
    distance = get_distance(image)
    get_move(distance)









