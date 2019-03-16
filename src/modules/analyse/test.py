#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from analyse.spark_base import Spark

from pyspark.mllib.feature import HashingTF, IDF, LabeledPoint
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel, SVMWithSGD
from pyspark.mllib.util import MLUtils
from core.database import get_session

import cPickle as pickle
import jieba
import sys
import settings
import os

reload(sys)
sys.setdefaultencoding('utf8')

"""
创建训练集
"""

def init_tranining_set(sc):
    """
    合并积极/消极的词性
    param: sc spark对象的context
    """

    words = sc.textFile('traning_words.csv')
    # 训练词频矩阵
    hashingTF = HashingTF()
    tf = hashingTF.transform(words)

    # 计算TF-IDF矩阵
    idfModel = IDF().fit(tf)
    tfidf = idfModel.transform(tf)
    tf.cache()

    with open('NBmodel.pkl', 'r') as f:
        NBmodel = pickle.load(f)

    session = get_session(settings.DB_URL)
    for r in session.execute('select * from traning_collection').fetchall():
        yourDocument = r[3]
        print r[3]
        yourwords="/".join(jieba.cut_for_search(yourDocument)).split("/")
        yourtf = hashingTF.transform(yourwords)
        yourtfidf=idfModel.transform(yourtf)
        print('NaiveBayes Model Predict:', NBmodel.predict(yourtfidf))

    #yourwords="/".join(jieba.cut_for_search(yourDocument)).split("/")
    #yourtf = hashingTF.transform(yourwords)
    #yourtfidf=idfModel.transform(yourtf)
    #print('SVM Model Predict:', SVMmodel.predict(yourtfidf))

if __name__ == '__main__':
    sp = Spark()
    sc = sp.get_spark_context()

    init_tranining_set(sc)
