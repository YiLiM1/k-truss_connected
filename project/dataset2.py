import networkx as nx
import os
def email_Eu_core(Concept_G, Physical_G):
    list2 = []
    for i in range(42):
        list2.append([-1, ])
    print(list2)
    with open( "email-Eu-core-department-labels.txt", 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            list1 = lines.split(" ")
            list1[1] = list1[1][0:len(list1[1])-1]
            list2[int(list1[1])].append(int(list1[0]))
            #print( list2[int(list1[1])])
            Concept_G.add_node(int(list1[0]))
            Physical_G.add_node(int(list1[0]))
            # print(list1[0])
        for i in list2:
            for j in i:
                for k in i:
                    if k==-1 or j==-1 or i==j:
                        continue
                    Concept_G.add_edge(j,k)
    file_to_read.close()
    f = open("数据集/email_Concept_edge.text", 'w', encoding='utf-8')
    for edge in Concept_G.edges():
        f.writelines(str(edge[0]) + '*' + str(edge[1]) + '\n')  # 将边信息存入text中，概念图构建完毕
    f.close()

    with open( "email-Eu-core.txt", 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            list1 = lines.split(" ")
            list1[1] = list1[1][0:len(list1[1])-1]
            print(list1)
            Physical_G.add_edge(int(list1[0]),int(list1[1]))
    file_to_read.close()

    f = open("数据集/email_Physical_edge.text", 'w', encoding='utf-8')
    for edge in Physical_G.edges():
        f.writelines(str(edge[0]) + '*' + str(edge[1]) + '\n')  # 将边信息存入text中，物理图构建完毕
    f.close()
    f = open("数据集/emaill_node.text", 'w', encoding='utf-8')
    for node in Physical_G.nodes():
        f.writelines(str(node) + '\n')  # 将顶点信息存入text中
    f.close()

def music(Concept_G, Physical_G):

    Concept_G=nx.watts_strogatz_graph(4039,55,0.3)
    print( Concept_G.nodes())

    f = open("数据集/facebook_Concept_edge.txt", 'w', encoding='utf-8')
    for edge in Concept_G.edges():
        f.writelines(str(edge[0]) + '*' + str(edge[1]) + '\n')  # 将边信息存入text中，物理图构建完毕
    f.close()

    f = open("数据集/facebook_node.txt", 'w', encoding='utf-8')
    for node in Concept_G.nodes():
        f.writelines(str(node) + '\n')  # 将顶点信息存入text中
    f.close()

if __name__ == '__main__':
    Concept_G = nx.Graph()
    Physical_G = nx.Graph()
    #email_Eu_core(Concept_G, Physical_G)
    music(Concept_G,Physical_G)