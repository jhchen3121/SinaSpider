#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from tasks import app
from datetime import datetime
from utils.page_source import PageSource

import time

'''
微博爬虫分布式任务队列
'''

@app.task
def spider_msg_get(username, password):
    ''' 
    获取用户信息相关信息 
    :param: username 账号
    :param: password 密码
    '''
    with PageSource() as ps:
        ps.run('13587703727', 'cjhcjh19961996')
        user_detail = ps.get_user_detail()

        print user_detail

        # 获取用户发表的微博
        user_publish_list = [each for each in ps.get_user_weibo(user_detail)]
        print len(user_publish_list)

        # 获取用户关注人的id
        concern_id_list = ps.get_concern_list(user_detail)

        print concern_id_list
