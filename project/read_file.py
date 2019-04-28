import networkx as nx
def read_dblp(Concept_G,Physical_G):
    with open('../数据集/G_node.text', 'r') as file_to_read:
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

    with open('../数据集/Concept_G.text_edge_0.55.text', 'r') as file_to_read:
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

    with open('../数据集/Physical_G_edge.text', 'r') as file_to_read:
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
    dict_C={}
    dict_P={}
    list_C=[]
    list_P=[]
    list_same=[]
    with open('../数据集/高血压_物理图_Nodes.text', 'r') as file_to_read:
        i=0
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
            list1=lines.split("\n")
            dict_C[str(i)] = list1[0]
            list_P.append(list1[0])
            i+=1
    file_to_read.close()

    with open('../数据集/高血压_概念图_Nodes.text', 'r') as file_to_read:
        i=0
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
            list1=lines.split("\n")
            dict_C[str(i)] =list1[0]
            list_C.append(list1[0])
            i += 1
    file_to_read.close()

    list_same=[n for n in list_C if n in list_P]  #双网络的公共节点

    C_G = nx.Graph()
    P_G = nx.Graph()


    with open('../数据集/高血压_物理图_Edges', 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
              break
            list1 = lines.split(" ")
            print(list1[0], list1[1])
            if dict_P[list1[0]] in list_same and dict_P[list1[1]] in list_same:
                Physical_G.add_edge(dict_C[list1[0]], dict_C[list1[1]])
    file_to_read.close()

    with open('../数据集/高血压_概念图_Edges', 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
              break
            list1 = lines.split(" ")
            print(list1[0], list1[1])
            if dict_C[list1[0]] in list_same and dict_C[list1[1]] in list_same:
               Concept_G.add_edge(dict_C[list1[0]], dict_C[list1[1]])
    file_to_read.close()
