import networkx as nx
import k_truss_connected as kcct
import matplotlib.pyplot as plt
import read_file
import time
import random
import os
i=0
G=[]
path1=''
def find_kcct(k,C_G,P_G):
    global G
    global i
    for set in nx.connected_components(P_G):
        print("连通分量size：",len(set),"连通分量点集：",set)
        sub_graph1 = C_G.subgraph(set).copy() # 生成概念图对应点集的子图
        sub_graph2 = C_G.subgraph(set).copy()
        while True:
            flag = 0
            for edge in sub_graph2.edges:
                #print("边:",edge,"tri:",len(list(nx.common_neighbors(sub_graph2,edge[0],edge[1]))))
                if len(list(nx.common_neighbors(sub_graph2,edge[0],edge[1]))) <k - 2:
                    try:
                        sub_graph1.remove_edge(*edge)
                    except:
                        print("已去除此边")
                    flag = 1
            sub_graph2=nx.Graph(sub_graph1)
            if flag == 0:
                break

        for node in sub_graph2.nodes: #去除度为0的节点
            if sub_graph2.degree(node)==0:
                print("去除顶点：",node)
                sub_graph1.remove_node(node)
        sub_graph2= nx.Graph(sub_graph1)

        p_sub=P_G.subgraph(sub_graph1.nodes).copy()

        if len(sub_graph2) and len(p_sub) and nx.is_connected(sub_graph2) and nx.is_connected(p_sub):
            i+=1
            print("添加物理图：",p_sub.nodes)
            print("添加概念图：",sub_graph2.nodes)
            G.append(k)

            #print("kcct序号:",i )
            print("概念图点数:", sub_graph2.number_of_nodes(), "概念图边数:",sub_graph2.number_of_edges())
            #nx.draw(sub_graph2, with_labels=True, font_size=12, node_size=0, )
            #plt.savefig(os.path.join(path1, "pic_uptodown\\%s-truss_%s_c.png") % (str(k), str(i)))
            #plt.show()

            print("物理图点数:",p_sub.number_of_nodes(), "物理图边数:", p_sub.number_of_edges())
            #nx.draw(p_sub, with_labels=True, font_size=12, node_size=0, )
            #plt.savefig(os.path.join(path1, "pic_uptodown\\%s-truss_%s_p.png") % (str(k), str(i)))
            #plt.show()
        else:
            for sub in nx.connected_component_subgraphs(sub_graph2):
                find_kcct(k,sub,p_sub)
if __name__ == '__main__':
    Concept_G=nx.Graph()
    Physical_G=nx.Graph()

    #read_file.read_synthetic1(Concept_G, Physical_G)#读取合成数据集1
    read_file.read_synthetic2(Concept_G,Physical_G)#读取合成数据集2
    #read_file.read_dblp(Concept_G,Physical_G)#读取DBLP数据集
    #read_file.read_protein(Concept_G,Physical_G)#读取蛋白质双网络
    #read_file.read_email(Concept_G, Physical_G) # 读取邮件双网络
    #read_file.read_facebook(Concept_G,Physical_G)# 读取facebook双网络

    print(nx.core_number(Concept_G).values())
    k = max(nx.core_number(Concept_G).values())  # k-core分解，k得最大值边界为k-core的最大值
    k=k+1
    ''''''
    start=time.time()
    print("k值上边界：", k)



    while True:
        C_G = nx.Graph(Concept_G)
        P_G = nx.Graph(Physical_G)
        for node in Concept_G:  # 初步去除
            # print(node," ", Concept_G.degree(node))
            if Concept_G.degree(node) < k - 1:
                C_G.remove_node(node)
                P_G.remove_node(node)


        find_kcct(k, C_G, P_G)
        if len(G) != 0:
            print("Kmax为：", k)
            break
        k -= 1
        print("k:",k)
        G.clear()
    end=time.time()
    print(end-start)