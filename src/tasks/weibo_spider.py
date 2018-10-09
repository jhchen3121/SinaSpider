#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from tasks import app
from datetime import datetime

import time

'''
微博爬虫分布式任务队列
'''

@app.task
def test():
    
    time.sleep(3)
    print '111'
