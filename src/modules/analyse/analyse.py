#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from modules.analyse.spark_base import Spark
from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF, IDF, LabeledPoint
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel, SVMWithSGD
from pyspark.mllib.util import MLUtils

import cPickle as pickle
import os
import jieba
import settings
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

"""
继承spark类, 用于数据分析
"""

class Analyse(Spark):

    def __init__(self):
        super(Analyse, self).__init__()

    def analyse_data(self, data):
        """
        针对入口数据进行合适的分析
        param data: file, unicode, str
        """
        words = self.sc.textFile(self.training_words_dir)
        # 训练词频矩阵
        hashingTF = HashingTF()
        tf = hashingTF.transform(words)

        # 计算TF-IDF矩阵
        idfModel = IDF().fit(tf)
        tfidf = idfModel.transform(tf)
        tf.cache()

        with open(self.NBmodel, 'r') as f:
            NBmodel = pickle.load(f)

        # 先分词后分析
        yourwords = set("/".join(jieba.cut_for_search(data)).split("/"))
        print '分词结果：{}'.format(yourwords)
        yourtf = hashingTF.transform(yourwords)
        yourtfidf = idfModel.transform(yourtf)

        return NBmodel.predict(yourtfidf), data

if __name__ == '__main__':

    from core.database import get_session
    from domain.models import Analyse_result

    s = Analyse()
    session = get_session(settings.DB_URL)
    for r in session.execute('select * from traning_collection').fetchall():
        user_id = r[1]
        user_name = r[2]
        content = r[3]
        rate, _ = s.analyse_data(content)

        obj = Analyse_result(user_id=user_id,user_name=user_name,rate=rate,content=content)
        
        session.add(obj)
        session.commit()
