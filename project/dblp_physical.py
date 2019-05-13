# -*- coding: UTF-8 -*-
import xml.sax
import networkx as nx

class MovieHandler(xml.sax.ContentHandler):

    def __init__(self):      #类属性定义
            self.G=nx.Graph()
            self.CurrentData = ""
            self.author = ""
            self.title = ""
            self.mdate = ""
            self.key = ""
            self.tag = ""
            self.list=[]
            self.year = ""

    def startElement(self, tag, attributes):# 元素开始调用
            self.CurrentData = tag
            #if tag == "phdthesis"and attributes["key"].find(r"dk") != -1:
            if tag == "inproceedings" and (   attributes["key"].find(r"conf/kdd")!= -1 #检测符合的tag开始执行
                                           or attributes["key"].find(r"conf/icdm")!=-1
                                           or attributes["key"].find(r"conf/sdm")!=-1
                                           or attributes["key"].find(r"conf/wsdm")!=-1
                                           or attributes["key"].find(r"conf/pakdd")!=-1):
                self.mdate=attributes["mdate"]
                self.key=attributes["key"]
                self.tag=tag
                #print ("mdate:",attributes["mdate"])
                print ("key",attributes["key"])

            #inproceedings
    # 元素结束调用
    def endElement(self, tag):          #循环tag执行，遇到title标题continue
        #if self.tag == "phdthesis" and self.key.find(r"dk") != -1:
        if self.tag == "inproceedings" and (self.key.find(r"conf/kdd") != -1
                                            or self.key.find(r"conf/icdm") != -1
                                            or self.key.find(r"conf/sdm") != -1
                                            or self.key.find(r"conf/wsdm") != -1
                                            or self.key.find(r"conf/pakdd") != -1):
            # print self.key
            if self.CurrentData == "author":
                # print ("author:", self.author)
                self.list.append(self.author)  # 用列表存储一篇文章的共同作

            elif self.CurrentData == "title":
                self.data = self.title
                # print("title:", self.title)

            elif self.CurrentData == "year":
                print("title:", self.data)
                print("year:", self.year)
                if self.year > "2013":
                    # print(self.list)
                    for i in self.list:
                        self.G.add_node(i, title=(), cut=())
                        print("author:", i)
                        # print("Node数目：", self.G.number_of_nodes())
                        t = (self.data,)
                        self.G.nodes[i]['title'] = self.G.nodes[i]['title'] + t
                        print(self.G.nodes[i]['title'])
                    for i in self.list:  # 作者之间相互加边，如已存在边weight++
                        for j in self.list:
                            if i==j:
                                continue
                            if self.G.has_edge(i,j):
                                weight=self.G[i][j]['weight']+1
                                self.G.add_edge(i, j,weight=weight)
                            else:
                                self.G.add_edge(i, j, weight=1)
                self.list.clear()  # 结束后值要清零
                self.CurrentData = ""
                self.key = ""
                self.data = ""
                self.tag = ""

    # 读取字符时调用
    def characters(self, content):
        if self.CurrentData == "author":
            self.author = content
        elif self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "year":
            self.year = content

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
    #Physical_G=nx.convert_node_labels_to_integers(G)     #将原图转换成全int型图
    f = open("../数据集/G_node.text", 'w', encoding='UTF-8')
    for node in G.nodes():
        f.writelines(node+'\n')  # 将边信息存入text中，物理图构建完毕
    f.close()

    f=open("../数据集/Physical_G_edge.text",'w',encoding='UTF-8')
    flag=0
    for edge in G.edges():

        if G[edge[0]][edge[1]]['weight']>=3:
            flag+=1
            f.writelines(edge[0]+'*'+edge[1]+'\n') #将边信息存入text中，物理图构建完毕
    f.close()
    print(G.number_of_nodes())
    print(flag)