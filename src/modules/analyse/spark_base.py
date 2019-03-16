#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from pyspark import SparkConf, SparkContext

"""
封装spark类, 进行方法调用
"""

class Spark(object):

    def __init__(self):
        self.conf = SparkConf().setMaster('local').setAppName('my app')
        self.sc = SparkContext(conf=self.conf)

    def get_spark_context(self):

        return self.sc
