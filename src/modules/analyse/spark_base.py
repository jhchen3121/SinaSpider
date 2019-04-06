#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

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
封装spark类, 进行方法调用
"""

class Spark(object):

    def __init__(self):
        self.conf = SparkConf().setMaster('local').setAppName('my app')
        self.sc = SparkContext(conf=self.conf)
        # 训练集路径
        self.training_words_dir = os.path.join(settings.DATA_DIR, 'traning_result/tranining_words')
        self.NBmodel = os.path.join(settings.DATA_DIR, 'traning_result/NBmodel')

        self.create_bayes()

    def get_spark_context(self):
        return self.sc

    def _check_traning_exists(self):
        """ 
        检查本地是否已经存在训练集
        """

        return True if os.path.isfile(self.NBmodel) and os.path.exists(self.training_words_dir) else False

    def create_bayes(self):
        """ 创建贝叶斯训练模型 """

        if self._check_traning_exists():
            return

        # 获取积极文本构造rdd
        positive_file = os.path.join(settings.DATA_DIR, '分类词库/positive.txt')
        positive_data = self.sc.textFile(positive_file)
        # 数据去重
        positive_data = positive_data.distinct()
        positive_data = positive_data.map(lambda line : line.split('###')).filter(lambda line : len(line)==2)

        # 获取消极文本构造rdd
        negative_file = os.path.join(settings.DATA_DIR, '分类词库/negative.txt')
        negative_data = self.sc.textFile(negative_file)
        negative_data = negative_data.distinct()
        negative_data = negative_data.map(lambda line : line.split('###')).filter(lambda line : len(line)==2)

        # 合并训练集
        all_data = negative_data.union(positive_data)
        all_data.repartition(1)
        # 评分已经提前进行处理只有-1与1
        rate = all_data.map(lambda s : s[0])
        document = all_data.map(lambda s: s[1])

        words = document.map(lambda w:"/".\
                join(jieba.cut_for_search(w))).\
                map(lambda line: line.split("/"))

        # 训练词频矩阵
        hashingTF = HashingTF()
        tf = hashingTF.transform(words)

        # 计算TF-IDF矩阵
        idfModel = IDF().fit(tf)
        tfidf = idfModel.transform(tf)
        tf.cache()

        # 生成训练集和测试集
        zipped = rate.zip(tfidf)
        data = zipped.map(lambda line:LabeledPoint(line[0],line[1]))
        training, test = data.randomSplit([0.6, 0.4], seed = 0)

        # 训练贝叶斯分类模型
        NBmodel = NaiveBayes.train(training, 1.0)
        predictionAndLabel = test.map(lambda p : (NBmodel.predict(p.features), p.label))
        accuracy = 1.0 * predictionAndLabel.filter(lambda x: 1.0 \
                if x[0] == x[1] else 0.0).count() / test.count()

        # 存储rdd
        words.repartition(1).saveAsTextFile(self.training_words_dir)
        # 贝叶斯分类模型以pickle存储
        with open(self.NBmodel, 'w') as f:
            pickle.dump(NBmodel, f)

if __name__ == '__main__':
    s = Spark()
