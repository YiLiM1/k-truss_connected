# -*- coding: UTF-8 -*-
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def cos_compare(s1,s2):
    porter_stemmer = PorterStemmer()
    s1_cut = [i for i in nltk.tokenize.word_tokenize(s1)] #语句分解
    s2_cut = [i for i in nltk.tokenize.word_tokenize(s2)]

    stopword = stopwords.words('english') #停词过滤
    filtered_sentence1 = [w for w in s1_cut if not w in stopword]
    filtered_sentence2 = [w for w in s2_cut if not w in stopword]
    #print(filtered_sentence1)
    #print(filtered_sentence2)
    s1_cut = [porter_stemmer.stem(w) for w in filtered_sentence1] #词根过滤
    s2_cut = [porter_stemmer.stem(w) for w in filtered_sentence2]

    # print(s1_cut)
    # print(s2_cut)
    word_set = set(s1_cut).union(set(s2_cut))  #余弦算法比较文本
    #print(word_set)

    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1
    #print(word_dict)

    s1_cut_code = [word_dict[word] for word in s1_cut]
    #print(s1_cut_code)
    s1_cut_code = [0]*len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]]+=1
    #print(s1_cut_code)

    s2_cut_code = [word_dict[word] for word in s2_cut]
    #print(s2_cut_code)
    s2_cut_code = [0]*len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]]+=1
    #print(s2_cut_code)

    # 计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(s1_cut_code)):
        sum += s1_cut_code[i] * s2_cut_code[i]
        sq1 += pow(s1_cut_code[i], 2)
        sq2 += pow(s2_cut_code[i], 2)

    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
    except ZeroDivisionError:
        result = 0.0
    print("相似度：",result)
    return result