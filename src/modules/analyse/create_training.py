#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from analyse.spark_base import Spark

from pyspark.mllib.feature import HashingTF, IDF, LabeledPoint
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel, SVMWithSGD
from pyspark.mllib.util import MLUtils

import cPickle as pickle
import jieba
import sys
import settings
import os

reload(sys)
sys.setdefaultencoding('utf8')

"""
创建训练集
方法参考：https://www.ibm.com/developerworks/cn/cognitive/library/cc-1606-spark-seniment-analysis/index.html
"""

def init_tranining_set(sc):
    """
    合并积极/消极的词性
    param: sc spark对象的context
    """

    # 获取积极文本构造rdd
    positive_file1 = os.path.join(settings.DATA_DIR, '分类词库/positive.txt')
    positive_data1 = sc.textFile(positive_file1)
    # 数据去重
    positive_data1 = positive_data1.distinct()
    positive_data1 = positive_data1.map(lambda line : line.split('###')).filter(lambda line : len(line)==2)

    #positive_file2 = os.path.join(settings.DATA_DIR, 'new_post.txt')
    #positive_data2 = sc.textFile(positive_file2)
    ## 数据去重
    #positive_data2 = positive_data2.distinct()
    #positive_data2 = positive_data2.map(lambda line : line.split('###')).filter(lambda line : len(line)==2)

    #positive_data = positive_data1.union(positive_data2)
    #positive_data.repartition(1)

    # 获取消极文本构造rdd
    negative_file1 = os.path.join(settings.DATA_DIR, '分类词库/negative.txt')
    negative_data1 = sc.textFile(negative_file1)
    negative_data1 = negative_data1.distinct()
    # 取两列
    negative_data1 = negative_data1.map(lambda line : line.split('###')).filter(lambda line : len(line)==2)
    #negative_file2 = os.path.join(settings.DATA_DIR, 'new_negi.txt')
    #negative_data2 = sc.textFile(negative_file2)
    #negative_data2 = negative_data2.distinct()
    ## 取两列
    #negative_data2 = negative_data2.map(lambda line : line.split('###')).filter(lambda line : len(line)==2)

    #negative_data = negative_data1.union(negative_data2)
    #negative_data.repartition(1)


    positive_data = positive_data1
    negative_data = negative_data1
    print negative_data.count()
    print positive_data.count()

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

    # 文本按照csv格式存储
    words.repartition(1).saveAsTextFile("traning_words")
    # 贝叶斯分类模型以pickle存储
    with open('NBmodel.pkl', 'w') as f:
        pickle.dump(NBmodel, f)

    #SVMmodel = SVMWithSGD.train(training, iterations=100)
    #predictionAndLabel = test.map(lambda p : (SVMmodel.predict(p.features), p.label))
    #accuracy = 1.0 * predictionAndLabel.filter(lambda x: 1.0 if x[0] == x[1] else 0.0).count() / test.count()

    #yourDocument="太精彩了讲了一个关于梦想的故事剧情很反转制作也很精良"
    #yourwords="/".join(jieba.cut_for_search(yourDocument)).split("/")
    #yourtf = hashingTF.transform(yourwords)
    #yourtfidf=idfModel.transform(yourtf)
    #print('NaiveBayes Model Predict:', NBmodel.predict(yourtfidf))

    #yourwords="/".join(jieba.cut_for_search(yourDocument)).split("/")
    #yourtf = hashingTF.transform(yourwords)
    #yourtfidf=idfModel.transform(yourtf)
    #print('SVM Model Predict:', SVMmodel.predict(yourtfidf))

if __name__ == '__main__':
    sp = Spark()
    sc = sp.get_spark_context()

    init_tranining_set(sc)
