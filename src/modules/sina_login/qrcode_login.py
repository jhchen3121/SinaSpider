#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import time
import sys
import os

from selenium import webdriver
from pyvirtualdisplay import Display

from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger(__name__)

class WebDriver(object):
    """
    浏览器驱动，selenium自动化
    """

    def __init__(self):
        self.dri_path = os.path.join(os.environ['PROJ_DIR'], 'server/webdriver/geckodriver')
        self.driver = None

    def __enter__(self):
        try:
            # 打开虚拟窗口
            display = Display(visible=0, size=(800, 600))
            display.start()

            #设置文件下载路径
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

    def get_url(self, url):
        ''' 初始化url '''
        self.driver.get(url)

        time.sleep(2)

        print self.driver.page_source 

if __name__ == '__main__':

    with WebDriver() as wd:
        wd.get_url('https://weibo.com/')
