#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from tasks import app
from datetime import datetime

import time

'''
数据分析celery
'''

@app.task
def analysis_test():
    time.sleep(3)
    print 'analysis 111'
