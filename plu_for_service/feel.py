#coding=utf8
from collections import defaultdict
import os
import re
import jieba
import codecs
import sys
import chardet
import matplotlib.pyplot as plt


def sent2word(sentence):
    #调用jieba进行分词
    segList = jieba.cut(sentence)
    #分词后的结果存为segResult 为list类型
    segResult = []
    for w in segList:
        segResult.append(w)

    #调用 readLines 读取停用词
    stopwords = readLines('stop_words.txt')

    #如果是停用词 就不保存到newSent
    newSent = []
    for word in segResult:
        if word+'\n' in stopwords:
            continue
        else:
            newSent.append(word)
    #返回newSent
    return newSent
    #直接对 sentence 进行分词  不使用停用词 并返回（主要是根据word需要这个操作）

def returnsegResult(sentence):
    segResult = []
    segList = jieba.cut(sentence)
    for w in segList:
        segResult.append(w)
    return segResult
    #获取 filepath 目录下的所有文件目录并返回

def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    child=[]
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child
    #读取 filename路径 的每一行数据 并返回 转换为GBK

def readLines(filename):
    fopen = open(filename, 'r')
    data=[]
    for x in fopen.readlines():
        if x.strip() != '':
                data.append(unicode(x.strip(),"GBK"))

    fopen.close()
    return data



    #读取 filename路径 的每一行数据 并返回
def readLines2(filename):
    fopen = open(filename, 'r')
    data=[]
    for x in fopen.readlines():
        if x.strip() != '':
                data.append(x.strip())
    fopen.close()
    return data
    #主要为情感定位  见程序文件相关代码 这里是为了速度 提取了部分代码 本来应该在classifyWords 里边  貌似对速度影响不大

def words():
    #情感词
    senList = readLines2('BosonNLP_sentiment_score.txt')
    senDict = defaultdict()
    for s in senList:
        senDict[s.split(' ')[0]] = s.split(' ')[1]
    #否定词
    notList = readLines2('notDict.txt')
    #程度副词
    degreeList = readLines2('degreeDict.txt')
    degreeDict = defaultdict()
    for d in degreeList:
        degreeDict[d.split(' ')[0]] = d.split(' ')[1]

    return senDict,notList,degreeDict
    # 见文本文档  根据情感定位  获得句子相关得分




def classifyWords(wordDict,senDict,notList,degreeDict):

    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()
    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord
    #计算句子得分  见程序文档

def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    # notloc = -1
    # degreeloc = -1
    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            # print "score = %f" % score
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(senLoc[senloc], senLoc[senloc + 1]):
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
        # i定位至下一个情感词
        if senloc < len(senLoc) - 1:
            i = senLoc[senloc + 1]
    return score
    #列表 转 字典



def listToDist(wordlist):
    data={}
    for x in range(0, len(wordlist)):
        data[wordlist[x]]=x
    return data
    #绘图相关  自行百度下


def runplt():
    plt.figure()
    plt.title('test')
    plt.xlabel('x')
    plt.ylabel('y')
    #这里定义了  图的长度 比如 2000条数据 就要 写 0,2000  
    plt.axis([0,1000,-10,10])
    plt.grid(True)
    return plt




#主题从这里开始 上边全是方法


#获取 test/neg 下所有文件 路径






#获取 本地的情感词 否定词 程度副词
words_vaule=words()

#循环 读取 filepwd  （也就是test/neg目录下所有文件全部跑一下）
def findout_feel(voice):
    #读目录下文件的内容
    data=readLines(voice)
    #对data内容进行分词
    datafen=sent2word(data[0])
    #列表转字典
    datafen_dist=listToDist(datafen)
    #通过classifyWords函数 获取句子的 情感词 否定词 程度副词 相关分值
    data_1=classifyWords(datafen_dist,words_vaule[0],words_vaule[1],words_vaule[2])
    # 通过scoreSent 计算 最后句子得分
    data_2=scoreSent(data_1[0],data_1[1],data_1[2],returnsegResult(data[0]))
    # 将得分保存在score_var 以列表的形式
    score=data_2
    #打印句子得分
    print data_2,voice

def start_find():
    print findout_feel("你好，我是王蛟，很高兴遇到你")
