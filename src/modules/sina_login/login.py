#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from lxml import etree

import os
import re
import time
import requests

def user_login(username, password):
    '''
    用户模拟登陆新浪微博
        入口参数：账号密码
        返回值：
            session：session对象，保存了cookie
            user_id：用户唯一id号，通过登陆后方可获取
    '''

    #构造session对象
    session = requests.session()

    #构造header
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Mobile Safari/537.36'
    referer = 'https://passport.weibo.cn/signin/login'
    headers = {
        'User-Agent' : user_agent,
        'Host' : 'passport.weibo.cn',
        'Origin' : 'https://passport.weibo.cn',
        'Referer' : referer,
        'Content-Type' : 'application/x-www-form-urlencoded'
    }

    #构造登陆时提交的表单
    form_data = {
        'username':username,
        'password':password,
        'savestate':'1',
        'r':'',
        'ec':'0',
        'pagerefer':'',
        'entry':'mweibo',
        'wentry':'',
        'loginfrom':'',
        'client_id':'',
        'code':'',
        'qq':'',
        'mainpageflag':'1',
        'hff':'',
        'hfp':''
    }

    post_url = "https://passport.weibo.cn/sso/login"

    #发送post请求
    login = session.post(url=post_url, data=form_data, headers=headers)
    print login.cookies
    print login.status_code
    print login.content.decode('gbk')
    #获取个人用户的id
    uuid = login.text
    uuid_pa = r'"uid":"(.*?)"'
    user_id = re.findall(uuid_pa, uuid, re.S)[0]
    user_id = int(user_id)
    print user_id

    return session, user_id

