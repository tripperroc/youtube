import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys


data = np.genfromtxt('trevorspace_responses.csv',delimiter='^',dtype=None, autostrip=True, names=True)
types = defaultdict(np.dtype)
for i in range(1,len(data.dtype.names)):
    if data.dtype.names[i].find("SURVEY") != 0:
        types[data.dtype.names[i]] = data.dtype[i]




# use data.dtype.names to get field names
#print data.dtype.names
PHQ9 = data['PHQ9_questions_answered'] >= 9
median_PHQ9_score = np.median (data['PHQ9_score'])
PHQ9_high = data['PHQ9_score'] >= 9
PHQ9_low = data['PHQ9_score'] < 9

g = nx.read_edgelist('edges_encrypted_3-21-12.txt.mac', create_using=nx.Graph(), delimiter=',')
h = nx.read_edgelist('edges_encrypted_4-20-12.txt.mac', create_using=nx.Graph(), delimiter=',')

# add data to graphs
for datum in data:
    #    print datum
    for gr in (g, h):
        if gr.has_node(datum[0]):
            for i in range(1,len(datum)):
              if data.dtype.names[i].find("SURVEY") != 0:
                gr.node[datum[0]][data.dtype.names[i]] = ("%s" % datum[i])                
                 
u = nx.compose(g,h) # the union graph

i = nx.Graph() # the intersection graph
for node in g.nodes_iter():
    if h.has_node (node):
        i.add_node(node)
    for v in g.neighbors (node):
        if h.has_edge (node, v):
            i.add_edge(node,v)

# ==============================
# Get subgraphs and CONNECTIVITY
# ------------------------------
graphs = [u]
gccs = graphs
data2 = data[PHQ9]


resp = [gcc.subgraph(data2['hashed_id']) for gcc in gccs]
good_dats = np.array([id in resp[0].node.keys() for id in data2['hashed_id']])

data2 = data2[good_dats]
medi = np.median(data2['PHQ9_score'])
PHQ9_low = data2['PHQ9_score'] <= medi
PHQ9_high = data2['PHQ9_score'] > medi
data_high = data2[PHQ9_high]
data_low = data2[PHQ9_low]

# find duplicate values
x = data2['hashed_id']
m = np.zeros_like(x, dtype=bool)
m[np.unique(x, return_index=True)[1]] = True
x[~m]
