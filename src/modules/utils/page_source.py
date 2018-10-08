#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import time
import sys
import os

from utils.webdriver import WeiboDriver
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger(__name__)

class PageSource(WeiboDriver):
    """
    继承微博驱动类，有自动登陆等模块
    主要实现页面解析
    """

    def get_user_detail(self):
        ''' 获取用户基本信息 '''

        url = 'https://weibo.cn/'
        self.driver.get(url)

        time.sleep(1)

        # 获取详细资料按钮
        detail_button = self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/a[2]')
        detail_button.click()

        time.sleep(1)

        html = etree.HTML(self.driver.page_source)

        # 用户id
        user_id = html.xpath('/html/body/div[11]/text()[1]')[0]
        user_id = user_id.split('/')[-1]
        print user_id

        user_name = html.xpath('/html/body/div[9]/text()[1]')[0].replace(':', '')
        sex = html.xpath('/html/body/div[9]/text()[2]')[0].replace(':', '')
        user_address = html.xpath('/html/body/div[9]/text()[3]')[0].replace(':', '')
        # 星座
        constellation = html.xpath('/html/body/div[9]/text()[4]')[0].replace(':', '')
        # 性取向
        sexual_orientation = html.xpath('/html/body/div[9]/text()[5]')[0].replace(':', '')
        # 情感状况
        relationship = html.xpath('/html/body/div[9]/text()[6]')[0].replace(':', '')

        user_detail_dict = dict(
            user_id=user_id,
            user_name=user_name,
            sex=sex,
            user_address=user_address,
            constellation=constellation,
            sexual_orientation=sexual_orientation,
            relationship=relationship
        )

        return user_detail_dict

    def get_user_weibo(self, user_detail):
        '''
        获取用户发表微博
        '''

        user_id = user_detail.get('user_id')

        url = 'https://weibo.cn/{user_id}/profile?page={pageNum}'.format(user_id=user_id, pageNum=1)

        self.driver.get(url)

        time.sleep(1)
        resp = self.driver.page_source

        selector = etree.HTML(resp)

        #页数获取
        try:
            pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
        except:
            pageNum = 1

        for i in range(1, pageNum+1):
            url = 'https://weibo.cn/{user_id}/profile?page={pageNum}'.format(user_id=user_id, pageNum=i)

            self.driver.get(url)

            time.sleep(1)
            resp = self.driver.page_source

            selector = etree.HTML(resp)

            for each_dom in selector.xpath(r'//div[@class="c"]'):
                #是否为转发
                forward = each_dom.xpath(r'.//span[@class="cmt"]')
                if forward:
                    forward = forward[0]
                    print forward.xpath('string(.)')

                    content = each_dom.xpath(r'.//span[@class="ctt"]/text()')

                    if content:
                        print content[0]
                else:
                    content = each_dom.xpath(r'.//span[@class="ctt"]/text()')

                    if content:
                        print '用户自己发表：' + content[0]

if __name__ == '__main__':
    with PageSource() as ps:
        ps.run('13587703727', 'cjhcjh19961996')
        user_detail = ps.get_user_detail()
        ps.get_user_weibo(user_detail)

