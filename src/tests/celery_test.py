#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from tasks import weibo_spider

if __name__ == '__main__':
    weibo_spider.test.delay()
