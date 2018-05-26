#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from lxml import etree

import time
import re
import sys
import requests

def msg_get(session, user_id):
    '''
    用户关注微博发表内容获取
    入口参数：
        session：session对象，保存了登陆过后的cooike
        user_id：用户id，一一对应
    '''

    #这里的get请求不能随意加header
    login_index = session.get('http://weibo.cn/u/%d?filter=1&page=1'%user_id)
    selector = etree.HTML(login_index.content)
    pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
    result = ""
    urllist_set = set()
    #微博的数目
    word_count = 1
    print u'ready'
    print pageNum

    #获取用户名
    UserName = selector.xpath('//div[@class="ut"]/text()')[0]

    times = 5
    one_step = pageNum/times
    for step in range(times):
        if step < times - 1:
            i = step * one_step + 1
            j =(step + 1) * one_step + 1
        else:
            i = step * one_step + 1
            j =pageNum + 1
        for page in range(i, j):
            #获取lxml页面
            try:
                url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page)
                lxml = session.get(url).content
                #文字爬取
                selector = etree.HTML(lxml)
                content = selector.xpath('//span[@class="ctt"]')
                for each in content:
                    text = each.xpath('string(.)')
                    if word_count >= 3:
                        text = "%d: "%(word_count - 2) +text+"\n"
                    else :
                        text = text+"\n\n"
                    result = result + text
                    word_count += 1
                    print text
                print page,'word ok'
                sys.stdout.flush()
            except:
                print page,'error'
            print page, 'sleep'
            sys.stdout.flush()
            time.sleep(10)
        print u'正在进行第', step + 1, u'次停顿，防止访问次数过多'
        time.sleep(30)
    #try:
    #    fo = open(os.getcwd()+"/%s"%UserName, "wb")
    #    fo.write(result)
    #    word_path=os.getcwd()+'/%s'%UserName
    #    print u'文字微博爬取完毕'
    #except:
    #    print u'存放数据地址有误'
    #sys.stdout.flush()
    #print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count - 3,word_path)
    print u'原创微博爬取完毕，共%d条'%(word_count - 3)


