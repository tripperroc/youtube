import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys
import random
import copy

def graphfeatures (feats, name, allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names):
    
    print "Computing " + name 
    #    triangles = [nx.triangles(g) for g in allccs]
    outputs = list()
    for i in range(len(allccs)):
        l = list()
        for node in feats[i]:
            l.append(feats[i][node])
            #   l.sort()
        med = np.median(l)
        #fh.write("\t%f" % med)
        outputs.append((names[i], med))
        #      print ("%s: %f" % (names[i], med))
        

    for i in range(len(all_in_whole)):
       l = list()
       for node in all_in_whole[i]:
            l.append (feats[0][node])
            #   l.sort()
       med = np.median(l)
       outputs.append((all_in_whole_names[i], med))
                      #       fh.write("\t%f" % np.median(l))

    for i in range(len(all_in_resp)):
        l = list()
        for node in all_in_resp[i]:
            l.append (feats[1][node])
        med = np.median(l)
        outputs.append((all_in_resp_names[i], med))
        #       fh.write("\t%f" % np.median(l))
    return dict(outputs)

data = np.genfromtxt('trevorspace_responses.csv',delimiter='^',dtype=None, autostrip=True, names=True)
types = defaultdict(np.dtype)
for i in range(1,len(data.dtype.names)):
    if data.dtype.names[i].find("SURVEY") != 0:
        types[data.dtype.names[i]] = data.dtype[i]

graphnum = 0
funnygraphs = list()


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
ccs = [nx.connected_component_subgraphs(graph) for graph in graphs]
gccs = [cc[0] for cc in ccs]

data2 = data[:,PHQ9]
#data_high = data[:,PHQ9_high]
#data_low = data[:,PHQ9_low]
#data_high = list(data[:,PHQ9_high])
#data_low = list(data[:,PHQ9_low])

#phqs = list(data2["PHQ9_score"])

numgraphs = 0

resp = [gcc.subgraph(data2['hashed_id']) for gcc in gccs]
#resp = [nx.connected_component_subgraphs(graph) for graph in resp]
#resp = [cc[0] for cc in resp]

#data2 = np.intersect1d(data2['hashed_id'], resp[0].node.keys())
good_dats = np.array([id in resp[0].node.keys() for id in data2['hashed_id']])

data2 = data2[:,good_dats]
medi = np.median(data2['PHQ9_score'])
PHQ9_low = data2['PHQ9_score'] < medi
PHQ9_high = data2['PHQ9_score'] > medi
data_high = data2[:,PHQ9_high]
data_low = data2[:,PHQ9_low]

low_original = copy.copy(data_low)
high_original = copy.copy(data_high)

deg_med = list()
triangle_med = list()
clustering_med = list()
core_number_med = list()
lcc = list()

names = [ "union-full",  "union-all-induced",  "union-high-induced",  "union-low-induced"]
all_in_whole_names = [ "union-all-full",  "union-high-full", "union-low-full"]

all_in_resp_names = [ "union-high-all", "union-low-all"]

for r in range(100001):
        
    high = [gcc.subgraph(data_high['hashed_id']) for gcc in resp]
    #    high = [nx.connected_component_subgraphs(graph) for graph in high]
    #high = [cc[0] for cc in high]

    low = [gcc.subgraph(data_low['hashed_id']) for gcc in resp]
    #low = [nx.connected_component_subgraphs(graph) for graph in low]
    #low = [cc[0] for cc in low]
    allccs = gccs + resp + high + low
    all_in_whole = resp + high + low
    all_in_resp = high + low

    # ============
    # CONNECTIVITY
    # ------------

    #print "Size of largest connected components"
    # for i in range(len(allccs)):
    #    print "%s & %d \\\\ \hline" % (names[i],len(allccs[i].node))
    l = list()
    cchi = len(nx.connected_component_subgraphs(high[0])[0].node)
    cclow = len(nx.connected_component_subgraphs(low[0])[0].node)
    l.append(("cc.high", cchi))
    l.append(("cc.low", cclow))
    l.append(("size.high", len(high[0].node)))
    l.append(("size.low", len(low[0].node)))
    l.append(("overlap.high", len(np.intersect1d(high_original["hashed_id"], high[0].node.keys()))))
    l.append(("overlap.low", len(np.intersect1d(low_original["hashed_id"], low[0].node.keys()))))
    l.append(("clique.high", nx.graph_clique_number(high[0])))
    l.append(("clique.low", nx.graph_clique_number(low[0])))
    l.append(("bicc.high", len(list(nx.biconnected_component_subgraphs(high[0]))[0].node)))
    l.append(("bicc.low", len(list(nx.biconnected_component_subgraphs(low[0]))[0].node)))
    lcc.append(dict(l))

    
    if r == 0:
        degs = [dict([(node, len(cc.neighbors(node))) for node in cc]) for cc in allccs]
    else:
        for l in [2,3]:
            degs[l] = dict([(node, len(allccs[l].neighbors(node))) for node in allccs[l]])


    deg_med.append(graphfeatures (degs, "degs", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))
    if r > 0:
        if deg_med[-1][all_in_whole_names[2]] - deg_med[-1][all_in_whole_names[1]] > 23:
            for node in allccs[3].node.keys():
                d = {"feature" : "deg_number", "graphnum" : graphnum, "node": node}
                funnygraphs.append(d)
            graphnum += 1

    # ============
    # TRANSITIVITY
    # ------------
    print "Computing transitivity"
    # transitivity = [nx.transitivity(g) for g in allccs]
    #print "transitivity"
    #for i in range(len(allccs)):
    #    print "%s & %f \\\\ \hline" % (names[i],transitivity[i])



    # =========
    # TRIANGLES
    # ---------

    if r == 0:
        triangles = [nx.triangles(g) for g in allccs]
    else:
        for l in [2,3]:
            triangles[l] = nx.triangles(allccs[l])
    triangle_med.append(graphfeatures (triangles, "triangles", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))
    if r > 0:
        if triangle_med[-1][all_in_whole_names[2]] - triangle_med[-1][all_in_whole_names[1]] > 419.5:
            for node in allccs[3].node.keys():
                d = {"feature" : "triangle", "graphnum" : graphnum, "node": node}
                funnygraphs.append(d)
            graphnum += 1
        

    # ============
    # CLUSTERING
    # ------------
    print "Clustering..."
    if r == 0:
        clustering = [nx.clustering(g) for g in allccs]
    else:
        for l in [2,3]:
            clustering[l] = nx.clustering(allccs[l])
    clustering_med.append(graphfeatures (clustering, "clustering", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))
    if r > 0:
        if clustering_med[-1][all_in_whole_names[2]] - clustering_med[-1][all_in_whole_names[1]] < -.05:
            for node in allccs[3].node.keys():
                d = {"feature" : "clustering", "graphnum" : graphnum, "node": node}
                funnygraphs.append(d)
            graphnum += 1

    #    transitivity = [nx.transitivity(g) for g in allccs]
    #print "Finding clique numbers"
    #for i in range(4, len(allccs)):
    #    print "%s & %d \\\\ \hline" % (names[i],nx.graph_clique_number(allccs[i]))

    # ============
    # CORE_NUMBER
    # ------------
    print "Core_number..."
    #core_number = [nx.core_number(g) for g in allccs]

    if r == 0:
        core_number = [nx.core_number(g) for g in allccs]
    else:
        for l in [2,3]:
            core_number[l] = nx.core_number(allccs[l])

    core_number_med.append(graphfeatures (core_number, "core_number", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))
    if r > 0:
        if core_number_med[-1][all_in_whole_names[2]] - core_number_med[-1][all_in_whole_names[1]] > 17.5:
            for node in allccs[3].node.keys():
                d = {"feature" : "core_number", "graphnum" : graphnum, "node": node}
                funnygraphs.append(d)
            graphnum += 1


    #  data_hi
    random.shuffle(data2['PHQ9_score'])
    PHQ9_high = data2['PHQ9_score'] > medi
    PHQ9_low = data2['PHQ9_score'] < medi
    data_high = data2[:,PHQ9_high]
    data_low = data2[:,PHQ9_low]
    
    the_ids = list(u.node)

    outs = open("funnygraphs.json", "w")
    outs.write(json.dumps(funnygraphs) + "\n")
    
"""
files = [(lambda x: open(x, 'w'))(nm) for nm in ["degrees_nomed.json", "triangles_nomed.json", "clustering_nomed.json", "core_number_nomed.json", "lccsno.json"]]

files[0].write (json.dumps(deg_med) + "\n")
files[1].write (json.dumps(triangle_med) + "\n")
files[2].write (json.dumps(clustering_med) + "\n")
files[3].write (json.dumps(core_number_med) + "\n")
files[4].write (json.dumps(lcc) + "\n")
files[0].close()
files[1].close()
files[2].close()
files[3].close()
files[4].close()

# =============
# ASSORTATIVITY
# -------------
for datum in data:
    #   print datum
    for gr in all_in_whole:
        if gr.has_node(datum[0]):
            for i in range(1,len(datum)):
              if data.dtype.names[i].find("SURVEY") != 0:
                gr.node[datum[0]][data.dtype.names[i]] = datum[i]                



assorts=["al attracted females","Comment on pictures","m Flirt with someone","et other than online","watching television","n touch with friends","ng things Play games","l shortcoming for me","restless fidgety","ced any of the above","e of a family member","idence hall director","year Missed a class","sibling Halfsibling","following ADD ADHD","x birth assigned sex","ose you used Twitter","Compulsive Disorder","hem Find old friends","ing emotional issues","Comment on statuses","would accept chance","ou consider yourself","ose you used MySpace","following Depression","alcohol last 30 days"]
for name in types:
    if types[name] != np.float:
          st = name.split("_")
          print_name = " ".join(st)
          found = False
          for end in assorts:
              if print_name.endswith(end):
                  found = True
                  break
          if not found:
              continue
          sys.stdout.write (print_name)
          for i in range(len(all_in_whole)):
             val = nx.attribute_assortativity_coefficient(all_in_whole[i], name)
             
"""
