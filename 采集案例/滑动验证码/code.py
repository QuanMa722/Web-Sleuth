
# -*- coding: utf-8 -*-
# 豆瓣滑动验证码

# 导入需要的库
from selenium.webdriver.support import expected_conditions as ec  # 用于设置等待条件
from selenium.webdriver.common.action_chains import ActionChains  # 用于模拟鼠标操作
from selenium.webdriver.support.wait import WebDriverWait  # 用于设置显式等待
from selenium.webdriver.common.by import By  # 用于定位元素
from selenium import webdriver  # 用于控制浏览器
from urllib import request  # 用于下载验证码图片
import random  # 用于生成随机数
import time  # 用于添加延时
import cv2  # 用于图像处理
import re  # 用于正则表达式匹配


# 设置Edge WebDriver的路径
edge_driver_path = r"D:\APP\msedgedriver.exe"
# 创建Edge浏览器的WebDriver实例
driver = webdriver.Edge(executable_path=edge_driver_path)


def get_path():
    """
    获取验证码图片，并保存到本地
    """
    url = "https://accounts.douban.com"

    # 访问网页
    driver.get(url)
    # 点击密码登录按钮
    button_switch_password = driver.find_element(By.XPATH, "//*[@id='account']/div[2]/div[2]/div/div[1]/ul[1]/li[2]")
    button_switch_password.click()

    # 输入邮箱
    button_mail = driver.find_element(By.XPATH, "//*[@id='username']")
    button_mail.send_keys("88888888@qq.com")

    # 输入密码
    button_password = driver.find_element(By.XPATH, "//*[@id='password']")
    button_password.send_keys("88888888")

    # 点击登录
    button_click = driver.find_element(By.XPATH, "//*[@id='account']/div[2]/div[2]/div/div[2]/div[1]/div[4]/a")
    button_click.click()
    driver.implicitly_wait(5000)

    # 找到滑动验证码图片
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="tcaptcha_iframe_dy"]'))

    # 设置等待，直到找到条件为止
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "slideBg")))

    # 定位图片
    image_src = driver.find_element(By.ID, 'slideBg')

    image_src_new = image_src.get_attribute('style')

    find_src_re = r'background-image: url\(\"(.*?)\"\);'

    image_src_last = re.findall(find_src_re, image_src_new, re.S)[0]

    if image_src_last.find("https") == -1:
        image_src_last = "https://t.captcha.qq.com" + image_src_last

    image_path = "origin.png"
    # 保存图片
    request.urlretrieve(image_src_last, image_path)

    return image_path


def get_distance(image_path):
    """
    处理验证码图片，获取需要滑动的距离
    """
    image_process = cv2.imread(image_path)

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
            cv2.imwrite("output.jpg", image_process)  # 保存标记后的图像
            return x


def get_move(distance):
    """
    执行滑动验证码操作
    """
    distance_process = int(int(distance) * 340 / 672)
    button_move = driver.find_element(By.XPATH, '//*[@id="tcOperation"]/div[6]')
    x_coordinate = button_move.location['x']

    print(f"初始距离为:{x_coordinate}")

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

        print(f"第{count_num}次移动，移动距离为{move_x}，位置为{button_move.location['x']}/{distance_process}")
        count_num += 1

    ActionChains(driver).release().perform()

    time.sleep(5)
    # 关闭浏览器
    driver.quit()


def main():
    """
    主函数
    """
    image_path = get_path()
    distance = get_distance(image_path)
    get_move(distance)


if __name__ == '__main__':
    main()
