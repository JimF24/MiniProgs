#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018/7/12

@author: fengjiayi

A NLP program using TFIDF algorithm
"""

import math
import jieba
import jieba.analyse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re

def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords

def readFile(file_name):
    f = open(file_name, 'rb')
    content = f.read()
    #Cleaning data
    content = content.decode('utf-8')
    content = content.replace('\\n','')
    content = content.replace('-','')
    content = content.split('\n')
    return content

def fenci(strName):
    for i in range(len(strName)):
        paragraph = strName[i]
        strName[i] = ''
        seglist = jieba.cut(paragraph,cut_all=False)
        for segs in seglist:
            seg = segs.lower()
            if seg not in Chinese_stopwords and seg not in stopwords.words('english') : #delete stopping words
                if len(seg)>1: #delete words with length = 1
                    strName[i] += seg
                    strName[i] += ' '


#calculate tf value
def countword(content):
    word_dic={}
    for word in content:
        if word not in word_dic:
            word_dic[word] = 1
        else:
            word_dic[word] = word_dic[word]+1
    return word_dic

def tfidf(word_dic,corpusfile1,corpusfile2):
    word_idf = {}
    word_tfidf= {}
    num_files = len(corpusfile1)+len(corpusfile2)
    #calculate idf value
    for word in word_dic:
        for words in corpusfile1:
            if (word in words) :
                if word not in word_idf:
                    word_idf[word] = 1
                else: word_idf[word] = word_idf[word]+1
        for words2 in corpusfile2:
            if (word in words2) :
                if word not in word_idf:
                    word_idf[word] = 1
                else: word_idf[word] = word_idf[word]+1
    #calculate tf-idf value
    for key,value in word_dic.items():
        if key not in word_idf.keys():
            word_idf[key] = 0
        word_tfidf[key] = value * math.log(num_files/(word_idf[key]+1))
    #order in descending
    keyword_list = sorted(word_tfidf.items(),key = lambda item:item[1],reverse=True)
    return keyword_list               
            


yuanwenPath = "/Users/fengjiayi/Desktop/算法实习生/原文.txt"
corpusPath = "/Users/fengjiayi/Desktop/算法实习生/corpus.txt"
encorpusPath = "/Users/fengjiayi/Desktop/算法实习生/en_corpus.txt"
stopwords_path = "/Users/fengjiayi/Desktop/stopwords.txt"
Chinese_stopwords = stopwordslist(stopwords_path)   
yuanwen = readFile(yuanwenPath)
corpus  = readFile(corpusPath)
encorpus = readFile(encorpusPath)
punc = '[,.!\']()'
for i in range(len(encorpus)):
    encorpus[i] = encorpus[i].replace('\xa0','')
    encorpus[i] = re.sub(punc, '', encorpus[i])
    encorpus[i] = nltk.word_tokenize(encorpus[i])
    encorpus[i] = [w for w in encorpus[i] if(w not in stopwords.words('english'))]

    

fenci(yuanwen)
words_dic = []
#calculate tf
for paragraph in yuanwen:
    paragraph = paragraph.split(' ')
    words_dic.append(countword(paragraph))
    
result_list = []
for worddic in words_dic:
    result_list.append(tfidf(worddic,corpus,encorpus))

result = ''
text_file = open("/Users/fengjiayi/Desktop/冯家翼算法面试题答案.txt",'wb')
for i in range(len(result_list)-1):
    for j in range(10):
        result+='\"'
        result+=result_list[i][j][0]
        result+='\"'
        result+=', '
    result+='\n'
text_file.write(result.encode('utf-8'))
text_file.close()














