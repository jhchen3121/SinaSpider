#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from lxml import etree

import re
import requests

def detail_msg_get(session, user_id):
    '''
    用户详细信息抓取
    '''

    url = 'https://weibo.cn/{user_id}/info'.format(user_id=user_id)

    resp = session.get(url).content

    select = etree.HTML(resp)
    dom_tree = select.xpath(r'//div[@class="c"]')

    for each_dom in dom_tree:
        user_info = each_dom.xpath('string(.)')

        print user_info

def user_concern_get(session, user_id):
    '''
    用户的关注人
    '''

    #关注人的字典，微博名对应其主页url
    concern_dict = dict()

    #可能存在多页的情况
    try:
        url = 'https://weibo.cn/{user_id}/follow?page={pageNum}'.format(user_id=user_id, pageNum=1)

        resp = session.get(url).content
        selector = etree.HTML(resp)

        pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
    except:
        pageNum = 1

    print pageNum
    
    for i in range(1, pageNum+1):
        url = 'https://weibo.cn/{user_id}/follow?page={pageNum}'.format(user_id=user_id, pageNum=i)

        resp = session.get(url).content

        select = etree.HTML(resp)
        dom_tree = select.xpath(r'//td[@valign="top"]')

        for each_dom in dom_tree:
            try:
                each_name = each_dom.xpath(r'.//a/text()')[0]
                each_url = each_dom.xpath(r'.//a/@href')[0]

                concern_dict[each_name] = each_url

            except:
                continue

        print concern_dict

if __name__ == "__main__":

    session = requests.session()

    user_id = '2836479754'

    detail_msg_get(session, user_id)
