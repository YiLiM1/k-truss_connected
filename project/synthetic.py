import networkx as nx

C_G = nx.erdos_renyi_graph(1000,0.1)
P_G = nx.erdos_renyi_graph(1000,0.01)

print("Concept顶点:", C_G.number_of_nodes())
print("Concept边数:", C_G.number_of_edges())

print("Physical顶点:", P_G.number_of_nodes())
print("Physical边数:", P_G.number_of_edges())

''''''
f=open("数据集/synthetic2_node.text",'w',encoding='utf-8')
for node in C_G.nodes():
    f.writelines(str(node)+'\n') #将边信息存入text中，概念图构建完毕
f.close()

f=open("数据集/synthetic2_concept_edge.text",'w',encoding='utf-8')
for edge in C_G.edges():
    f.writelines(str(edge[0])+'*'+str(edge[1])+'\n') #将边信息存入text中，概念图构建完毕
f.close()

f=open("数据集/synthetic2_physical_edge.text",'w',encoding='utf-8')
for edge in P_G.edges():
    f.writelines(str(edge[0])+'*'+str(edge[1])+'\n') #将边信息存入text中，概念图构建完毕
f.close()
