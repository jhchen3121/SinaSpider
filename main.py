#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys
import os
import requests
import time
from lxml import etree
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf-8')

def Spider_1(username,password):
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Mobile Safari/537.36'
    referer = 'https://passport.weibo.cn/signin/login'
    headers = {
        'User-Agent' : user_agent,
        'Host' : 'passport.weibo.cn',
        'Origin' : 'https://passport.weibo.cn',
        'Referer' : referer
    }
    session = requests.session()
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
    index_url = "https://passport.weibo.cn/signin/login"
    headers["Host"] = "passport.weibo.cn"
    headers["Reference"] = index_url
    headers["Origin"] = "https://passport.weibo.cn"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    post_url = "https://passport.weibo.cn/sso/login"
    #发送post请求
    login = session.post(post_url, data=form_data, headers=headers)
    print(login.cookies)
    print(login.status_code)
    print (login.content.decode('gbk'))
    #获取个人用户的id
    uuid = login.text
    uuid_pa = r'"uid":"(.*?)"'
    user_id = re.findall(uuid_pa, uuid, re.S)[0]
    user_id = int(user_id)
    print user_id
    #登陆成功后利用cookie登陆
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
                print page,'word ok'
                sys.stdout.flush()
            except:
                print page,'error'
            print page, 'sleep'
            sys.stdout.flush()
            time.sleep(10)
        print u'正在进行第', step + 1, u'次停顿，防止访问次数过多'
        time.sleep(30)
    try:
        fo = open(os.getcwd()+"/%s"%UserName, "wb")
        fo.write(result)
        word_path=os.getcwd()+'/%s'%UserName
        print u'文字微博爬取完毕'
    except:
        print u'存放数据地址有误'
    sys.stdout.flush()
    print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count - 3,word_path)

if __name__ == "__main__":
    #多进程，参数是用户的帐号密码
    p1 = multiprocessing.Process(target = Spider_1, args = ('13587703727','cjhcjh19961996',))
    p2 = multiprocessing.Process(target = Spider_1, args = ('18483619375','13419497653',))

    p1.start()
    p2.start()



