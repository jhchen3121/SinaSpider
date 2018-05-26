#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from lxml import etree

import re
import requests

def msg_get(session, user_id):
    '''
    用户自己发表的内容抓取
        入口参数：
            session：session对象
            user_id：用户id号

    '''

    url = 'https://weibo.cn/{user_id}/profile?page={pageNum}'.format(user_id=user_id, pageNum=1)

    resp = session.get(url).content
    selector = etree.HTML(resp)

    #页数获取
    try:
        pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
    except:
        pageNum = 1

    for i in range(1, pageNum+1):
        url = 'https://weibo.cn/{user_id}/profile?page={pageNum}'.format(user_id=user_id, pageNum=i)

        resp = session.get(url).content
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
