import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys
import random
import copy
import Queue
import math


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

for datum in data:
    #    print datum
    for gr in (g, h):
        if gr.has_node(datum[0]):
            for i in range(1,len(datum)):
              if data.dtype.names[i].find("SURVEY") != 0:
                gr.node[datum[0]][data.dtype.names[i]] = datum[i]                

                 
u = nx.compose(g,h) # the union graph
for node in g.nodes_iter():
    u.add_node(node)
    for v in g.neighbors (node):
        u.add_edge(node,v)
for node in h.nodes_iter():
    u.add_node(node)
    for v in h.neighbors (node):
        u.add_edge(node,v)

data2 = data[PHQ9]
data_high = data[PHQ9_high]
data_low = data[PHQ9_low]
#data_high = list(data[:,PHQ9_high])
#data_low = list(data[:,PHQ9_low])

phqs = list(data2["PHQ9_score"])

degs = [len(u.neighbors(node)) for node in u]

med_degs = np.median(degs)

giant_cc = len(nx.connected_component_subgraphs(u)[0].node)

giant_bicc = len(list(nx.biconnected_component_subgraphs(u))[0].node)

triangles = nx.triangles(u)

np.median(triangles.values())

clustering = nx.clustering(u)
the_ids = list(u.node)

core_number = nx.core_number(u)
resp = u.subgraph(data2['hashed_id'])


for i in range(5000):
    samp = set(random.sample(the_ids,185))
    samp_feats =[(abs(np.median([len(u.neighbors(node)) for node in samp])-66))/66, (abs(np.median([triangles[node] for node in samp])-700))/700, (abs(np.median([clustering[node] for node in samp])-0.3485))/.3485, (abs(np.median([core_number[node] for node in samp])-57))/57,(abs(float(len(nx.connected_component_subgraphs(u.subgraph(samp))[0].node))-162))/162, (abs(float(len(list(nx.biconnected_component_subgraphs(u.subgraph(samp)))[0].node))-126))/126]

    for j in range (1000):
        samp_new = random.sample(the_ids,185)
        
        #samp_feats_new = [abs(np.median([len(u.neighbors(node)) for node in samp_new]),np.median([triangles[node] for node in samp]), np.median([clustering[node] for node in samp]),np.median([core_number[node] for node in samp]),len(nx.connected_component_subgraphs(u.subgraph(samp))[0].node)]
        samp_feats_new =[(abs(np.median([len(u.neighbors(node)) for node in samp_new])-66))/66, (abs(np.median([triangles[node] for node in samp_new])-700))/700, (abs(np.median([clustering[node] for node in samp_new])-0.3485))/.3485, (abs(np.median([core_number[node] for node in samp_new])-57))/57,(abs(float(len(nx.connected_component_subgraphs(u.subgraph(samp_new))[0].node))-162))/162, (abs(float(len(list(nx.biconnected_component_subgraphs(u.subgraph(samp_new)))[0].node))-126))/126]
        frac = math.exp(np.sum(samp_feats)-np.sum(samp_feats_new))
        choice = random.random()
        if (frac >= 1 or choice <= frac):
            samp = samp_new
            samp_feats = samp_feats_new
    print len(set(samp).intersection(resp.nodes()))
    print samp_feats
        
