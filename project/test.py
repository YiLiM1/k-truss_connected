# -*- coding: UTF-8 -*-
import xml.sax
import networkx as nx
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os
class MovieHandler(xml.sax.ContentHandler):
    global G
    def __init__(self):      #类属性定义
            self.G=nx.Graph()
            self.CurrentData = ""
            self.author = ""
            self.title = ""
            self.data = "" #中间变量
            self.key = ""
            self.tag = ""
            self.list = []
            self.year = ""

    # 元素开始调用
    def startElement(self, tag, attributes):
            self.CurrentData = tag
            #if tag == "phdthesis"and attributes["key"].find(r"dk") != -1:
            if tag == "inproceedings" and (   attributes["key"].find(r"conf/kdd")!= -1 #检测符合的tag开始执行
                                           or attributes["key"].find(r"conf/icdm")!=-1
                                           or attributes["key"].find(r"conf/sdm")!=-1
                                           or attributes["key"].find(r"conf/wsdm")!=-1
                                           or attributes["key"].find(r"conf/pakdd")!=-1):
                self.key=attributes["key"]
                self.tag=tag
                print ("key",attributes["key"])

    # 元素结束调用
    def endElement(self, tag):          #循环tag执行，遇到title标题continue
        #if self.tag == "phdthesis" and self.key.find(r"dk") != -1:
        if self.tag == "inproceedings" and  (  self.key.find(r"conf/kdd") != -1
                                            or self.key.find(r"conf/icdm") != -1
                                            or self.key.find(r"conf/sdm") != -1
                                            or self.key.find(r"conf/wsdm") != -1
                                            or self.key.find(r"conf/pakdd") != -1):
            #print self.key
            if self.CurrentData == "author":
                #print ("author:", self.author)
                self.list.append(self.author)  #用列表存储一篇文章的共同作


            elif self.CurrentData == "title":
                self.data=self.title
                #print("title:", self.title)

            elif self.CurrentData == "year":
                print ("title:", self.data)
                print("year:", self.year)
                if self.year>"2013":
                    # print(self.list)
                    for i in self.list:
                        self.G.add_node(i, title=(),cut=())
                        print("author:",i)
                        #print("Node数目：", self.G.number_of_nodes())
                        t = (self.data,)
                        self.G.nodes[i]['title'] = self.G.nodes[i]['title'] + t
                        print(self.G.nodes[i]['title'])
                    for i in self.list:  # 作者之间相互加边，如已存在边weight++
                        for j in self.list:
                            self.G.add_edge(i, j)
                self.list.clear()              #结束后值要清零
                self.CurrentData = ""
                self.key=""
                self.data=""
                self.tag=""
    # 读取字符时调用
    def characters(self, content):
        if self.CurrentData == "author":
            self.author = content
        elif self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "year":
            self.year = content

def cos_compare(i,j):
    s1_cut = i
    s2_cut = j
    #print("比较:\n", s1_cut, "\n", s2_cut)

    word_set = set(s1_cut).union(set(s2_cut))  #余弦算法比较文本
    print(word_set)
    word_dict = dict()
    k = 0
    for word in word_set:
        word_dict[word] = k
        k += 1
    #print(word_dict)

    s1_cut_code = [word_dict[word] for word in s1_cut]
    s1_cut_code = [0]*len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]]+=1

    s2_cut_code = [word_dict[word] for word in s2_cut]
    s2_cut_code = [0]*len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]]+=1
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
    return  result



if (__name__ == "__main__"):
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
    G=nx.Graph(Handler.G)

    print("点数：", G.number_of_nodes())
    print("边数：", G.number_of_edges())

    porter_stemmer = PorterStemmer()
    stopword = stopwords.words('english')  # 停词过滤


    for i in G.nodes:
        s1 = ""
        for k in G.nodes[i]['title']:
            s1 = s1 + k + " "
        s1_cut = [i for i in nltk.tokenize.word_tokenize(s1)]  # 语句分解
        filtered_sentence1 = [w for w in s1_cut if not w in stopword]
        # print(filtered_sentence1)
        s1_cut = [porter_stemmer.stem(w) for w in filtered_sentence1]  # 词根过滤
        G.nodes[i]['cut']+=tuple(s1_cut)
        print(G.nodes[i]['cut'])
    flag=0
    edge=0
    for i in G.nodes:

        for j in G.nodes:
            #print("作者:",i,j)
            if i==j:continue
            if G.has_edge(i, j): continue
            flag+=1
            #print("flag:",flag)
            if cos_compare(list(G.nodes[i]['cut']),list(G.nodes[j]['cut']))>=0.3:
                G.add_edge(i, j)
                edge+=1
                print("边数:", edge)
            else:
                print("边数:", edge)

    Concept_G=nx.convert_node_labels_to_integers(G)      #将原图转换成全int型图
    f=open("Concept_G.text_0.3.text",'w')
    print( "边数：",Concept_G.number_of_edges())
    for edge in  Concept_G.edges():
        f.writelines(str(edge[0])+' '+str(edge[1])+'\n') #将边信息存入text中，概念图构建完毕
    f.close()


