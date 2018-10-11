#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from tasks import weibo_spider
from tasks import analysis

if __name__ == '__main__':
    weibo_spider.spider_msg_get.delay('13587703727', 'cjhcjh19961996')
    #analysis.analysis_test.delay()
