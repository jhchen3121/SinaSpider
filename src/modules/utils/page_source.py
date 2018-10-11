#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import time
import sys
import os
import requests

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

        # 获取微博发表数目，粉丝数以及关注
        resp = etree.HTML(self.driver.page_source)
        weibo_publish_count = resp.xpath('/html/body/div[5]/div[2]/a[1]/text()')[0].split('[')[1].split(']')[0]
        concern_count = resp.xpath('/html/body/div[5]/div[2]/a[2]/text()')[0].split('[')[1].split(']')[0]
        fans_count = resp.xpath('/html/body/div[5]/div[2]/a[3]/text()')[0].split('[')[1].split(']')[0]

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
            relationship=relationship,
            weibo_publish_count=weibo_publish_count,
            concern_count=concern_count,
            fans_count=fans_count
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
                # 获取发表时间

                try:
                    publish_date = each_dom.xpath(r'.//span[@class="ct"]/text()')[0][:19]

                    #是否为转发
                    forward = each_dom.xpath(r'.//span[@class="cmt"]')
                    if forward:
                        forward = forward[0]
                        #print forward.xpath('string(.)')
                        content = each_dom.xpath(r'.//span[@class="ctt"]/text()')

                        if content:
                            #print publish_date, content[0]
                            yield {'publish_date': publish_date, 'content': '转发:' + content[0]}
                    else:
                        content = each_dom.xpath(r'.//span[@class="ctt"]/text()')

                        if content:
                            #print publish_date, '用户自己发表:' + content[0]
                            yield {'publish_date': publish_date, 'content': '用户自己发表:' + content[0]}
                except Exception, e:
                    continue

    def get_ohter_peoples_mesg(self):
        ''' 获取他人所发表的微博 '''
        pass

    def get_concern_list(self, user_detail):
        ''' 获取用户关注列表 '''
        user_id = user_detail.get('user_id')

        # 关注列表键值对，存放关注列表以及对应的url
        concern_list = []

        # 拼接请求url,提高效率不去模拟点击操作, 可能存在多页的情况
        try:
            url = 'https://weibo.cn/{user_id}/follow?page={pageNum}'.format(user_id=user_id, pageNum=1)

            self.driver.get(url)
            time.sleep(1)

            resp = self.driver.page_source
            selector = etree.HTML(resp)

            pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
        except:
            pageNum = 1 

        for i in range(1, pageNum+1):
            url = 'https://weibo.cn/{user_id}/follow?page={pageNum}'.format(user_id=user_id, pageNum=i)

            self.driver.get(url)
            time.sleep(1)

            resp = self.driver.page_source
            select = etree.HTML(resp)

            dom_tree = select.xpath(r'//td[@valign="top"]')

            for each_dom in dom_tree:
                try:
                    each_name = each_dom.xpath(r'.//a/text()')[0]
                    each_url = each_dom.xpath(r'.//a/@href')[0]
                    #concern_dict[each_name] = each_url
                    concern_list.append(each_url)
                except Exception, e:
                    continue

        # 用户关注的人对应的id
        concern_id_list = []
        for i in concern_list:
            concern_id = i.split('/')[-1]
            concern_id_list.append(concern_id)

        return concern_id_list

if __name__ == '__main__':
    with PageSource() as ps:
        ps.run('13587703727', 'cjhcjh19961996')
        user_detail = ps.get_user_detail()

        for i in ps.get_user_weibo(user_detail):
            print i
        #ps.get_concern_list(user_detail)

