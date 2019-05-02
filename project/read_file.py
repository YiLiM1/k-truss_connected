import networkx as nx
import os
def read_dblp(Concept_G,Physical_G):
    path1=os.getcwd()  #表示当前所处的文件夹的绝对路径

    with open(os.path.join(path1, "数据集\\G_node.text"), 'r') as file_to_read:
      while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
          break
        list1=lines.split("\n")
        #list1[1] = list1[1][0:len(list1[1])-1]
        Concept_G.add_node(list1[0])
        Physical_G.add_node(list1[0])
        #print(list1[0])
    file_to_read.close()

    with open(os.path.join(path1, "数据集\\Concept_G.text_edge_0.55.text"), 'r') as file_to_read:
      while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
          break
        list1=lines.split("*")
        list1[1] = list1[1][0:len(list1[1])-1]
        #print(list1[0],list1[1])
        if list1[1] != list1[0]:
            Concept_G.add_edge(list1[0],list1[1])
    file_to_read.close()

    with open(os.path.join(path1, "数据集\\Physical_G_edge.text"), 'r') as file_to_read:
      while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
          break
        list1 = lines.split("*")
        list1[1]=list1[1][0:len(list1[1])-1]
        #print(list1[0], list1[1])
        if list1[1] != list1[0]:
            Physical_G.add_edge(list1[0], list1[1])
    file_to_read.close()

def read_protein(Concept_G,Physical_G):
    path1 = os.getcwd()  # 表示当前所处的文件夹的绝对路径
    dict_C={}
    dict_P={}
    list_C=[]
    list_P=[]

    with open(os.path.join(path1, "数据集\\Protein_Physical_Nodes.txt"), 'r') as file_to_read:
        i=0
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
            list1=lines.split("\n")
            dict_P[str(i)] = list1[0]
            list_P.append(list1[0])
            print(str(i), ":", list1[0])
            i+=1
    file_to_read.close()

    with open(os.path.join(path1, "数据集\\Protein_Concept_Nodes.txt"), 'r') as file_to_read:
        i=0
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
            list1=lines.split(" ")
            dict_C[str(i)] =list1[0]
            list_C.append(list1[0])
            print(str(i),":",list1[0])
            i += 1

    file_to_read.close()


    list_same=[n for n in list_C if n in list_P]  #双网络的公共节点
    #print(len(list_same))

    print(dict_C)
    print(dict_P)

    with open(os.path.join(path1, "数据集\\Protein_Physical_Edges.txt"), 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
              break
            list1 = lines.split(" ")
            list1[1]=list1[1][0:len(list1[1])-1]
            print(list1[0], list1[1])
            print(dict_P[list1[0]],dict_P[list1[1]])
            if dict_P[list1[0]] in list_same and dict_P[list1[1]] in list_same:
                Physical_G.add_edge(dict_P[list1[0]], dict_P[list1[1]])
    file_to_read.close()

    with open(os.path.join(path1, "数据集\\Protein_Concept_Edges.txt"), 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
              break
            list1 = lines.split(" ")
            print(list1[0], list1[1])
            print(dict_C[list1[0]], dict_C[list1[1]])
            if dict_C[list1[0]] in list_same and dict_C[list1[1]] in list_same:
               Concept_G.add_edge(dict_C[list1[0]], dict_C[list1[1]])
    file_to_read.close()

    Concept_G.add_nodes_from(list_same)
    Physical_G.add_nodes_from(list_same)