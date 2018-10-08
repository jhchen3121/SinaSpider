#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import time
import sys
import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from pyvirtualdisplay import Display
from lxml import etree
from PIL import Image
from io import BytesIO

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger(__name__)

class WeiboDriver(object):
    """
    selenium自动化,模拟登陆
    """

    def __init__(self):
        self.proj_dir = os.environ['PROJ_DIR']
        self.dri_path = os.path.join(self.proj_dir, 'server/webdriver/geckodriver')
        self.driver = None

    def __enter__(self):
        try:
            # 打开虚拟窗口
            display = Display(visible=0, size=(800, 600))
            display.start()

            # 设置文件下载路径
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.dir', '/home/jhchen/')
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.manager.showhenStarting', True)
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.ms-excel')

            self.driver = webdriver.Firefox(executable_path=self.dri_path, firefox_profile=profile)

        except Exception, e:
            logger.info(e)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.driver:
                self.driver.close()
                self.driver.quit()
        except Exception, e:
            logger.info(e)

    def submit_data(self, url, username, password):
        ''' 
        提交帐号密码获取手势截图 
        Params: url:登录网页的url, username:用户名, password: 密码
        '''
        
        self.driver.get(url)
        
        time.sleep(1)

        element_username = self.driver.find_element_by_id('loginName')
        element_password = self.driver.find_element_by_id('loginPassword')
        element_button = self.driver.find_element_by_id('loginAction')
        
        element_username.send_keys(username)
        element_password.send_keys(password)
        element_button.click()

        time.sleep(3)

        # 若出现了手势密码
        try:
            img = self.driver.find_element_by_class_name('patt-holder-body')
            return True
        except Exception, e:
            return False

    def get_position(self):
        ''' 获取验证码位置 '''
        img = self.driver.find_element_by_class_name('patt-holder-body')
        time.sleep(2)

        location = img.location
        size = img.size

        top, bottom, left, right = (
            location['y'],
            location['y'] + size['height'],
            location['x'],
            location['x'] + size['width']
        )

        return (top, bottom, left, right)

    def get_verify_image(self):
        ''' 获取验证码图片 '''

        # 获取图片位置
        top, bottom, left, right = self.get_position()

        # 截取整个页面
        screenshot = self.driver.get_screenshot_as_png()
        # 将页面存放至内存
        screenshot = Image.open(BytesIO(screenshot))
        # 截取手势验证码
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.show()
        #captcha.save('captcha.png')

        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        ''' 
        匹配两个像素是否相同 
        :Param image1: 图片1
        :Param image2: 图片2
        :Param x: x坐标
        :Param y: y坐标
        '''

        threshold = 20
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]

        if (
            abs(pixel1[0] - pixel2[0]) < threshold
            and abs(pixel1[1] - pixel2[1]) < threshold
            and abs(pixel1[2] - pixel2[1]) < threshold
            ):
            return True

        return False

    def same_image(self, image, template):
        '''
        识别相似验证码 
        :Params image: 截取图片
        :Params template: 本地模板
        '''

        # 相似度阈值
        threshold = 0.99
        count = 0

        for x in range(image.width):
            for y in range(image.height):
                if self.is_pixel_equal(image, template, x, y):
                    count += 1

        result = float(count) / (image.width * image.height)

        if result > threshold:
            print '匹配成功'
            return True
        else:
            return False

    def detect_image(self, image):
        '''
        匹配图片
        :Params iamge: 截图图片
        '''

        # 遍历本地模板是否存在相同图片
        captcha_temp_dir = os.path.join(self.proj_dir, '')
        for template_name in os.listdir(captcha_temp_dir):
            template = os.path.join(captcha_temp_dir, template_name)
            template = Image.open(template)
            if self.same_image(image, template):
                # 返回文件名即为对应顺序
                numbers = [int(number) for number in list(os.path.join(captcha_temp_dir, template_name).split('.')[0])]

                return numbers

    def move(self, numbers):
        ''' 拖动验证码 '''

        # 获取四个按点
        circles = self.driver.find_elements_by_css_selector('.patt-wrap .patt-circ')
        dx = dy = 0

        for index in range(4):
            # 获取对应按点
            circle = circles[numbers[index] - 1]

            # 如果是第一个按点
            if index == 0:
                # 点击不放
                ActionChains(self.driver).move_to_element_width_offset(circle, circle.size['width']/2, circle.size['height']/2).click_and_hold().perform()
            else:
                # 小幅度移动
                times = 30
                for i in range(times):
                    ActionChains(self.driver).move_by_offset(dx/times, dy/times).perform()
                    time.sleep(1/times)

            # 若为最后一个循环
            if index == 3:
                # 松开鼠标
                ActionChains(self.driver).release().perform()
            else:
                # 计算下一次偏移
                dx = (circles[numbers[index + 1] - 1].location['x'] - circle.location['x'])
                dy = (circles[numbers[index + 1] - 1].location['y'] - circle.location['y'])

        time.sleep(2)

    def run(self, username, password):
        ''' 自动化登录 '''

        login_url = 'https://passport.weibo.cn/signin/login'
        cord = self.submit_data(login_url, username, password)

        # 若无需验证
        if not cord:
            print '无需手势验证'
            return

        image = self.get_verify_image()
        numbers = self.detect_image(image)
        self.move(numbers)

    def save_verify_temp(self):
        ''' 保存24种可能存在的验证码至本地 '''

        # 需要手动筛选

        self.submit_data('https://passport.weibo.cn/signin/login', '13587703727', 'cjhcjh19961996')

        for i in range(1, 100):
            print i
            captcha = self.get_verify_image()

            captcha.svae('{}/{}.png'.format(self.proj_dir, i))

if __name__ == '__main__':
    with WeiboDriver() as wd:
        #wd.save_verify_temp()
        wd.run('13587703727', 'cjhcjh19961996')
