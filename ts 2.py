import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys

def graphfeatures (feats, name, allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names):
    
    print "Computing " + name 
    #    triangles = [nx.triangles(g) for g in allccs]
    for i in range(len(allccs)):
        filename = names[i] + "-" + name + ".json"
        print filename
        f = open (filename, 'w')
        l = list()
        for node in allccs[i]:
            l.append({"hash_id": node, name: feats[i][node]})
            allccs[i].node[node][name + ".full"] = feats[0][node]
            #   print ("%d, %s, %s, %s" % (i, node, name + ".full", feats[0][node]))
        f.write (json.dumps(l) + "\n")
        f.close ()

    for i in range(len(all_in_whole)):
        f = open (all_in_whole_names[i] + "-" + name + ".json", 'w')
        l = list()
        for node in all_in_whole[i]:
            l.append ({"hash_id": node, name: feats[0][node]})
            all_in_whole[i].node[node][name + ".all"] = feats[1][node]
        f.write (json.dumps(l) + "\n") 
        f.close ()

    for i in range(len(all_in_resp)):
        f = open (all_in_resp_names[i] + "-" + name + ".json", 'w')
        l = list()
        for node in all_in_resp[i]:
            l.append ({"hash_id": node, name: feats[1][node]})
            all_in_resp[i].node[node][name + ".phq"] = feats[i+2][node]
        f.write (json.dumps(l) + "\n") 
        f.close ()

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
"""
for node in g.nodes_iter():
    u.add_node(node)
    for v in g.neighbors (node):
        u.add_edge(node,v)
for node in h.nodes_iter():
    u.add_node(node)
    for v in h.neighbors (node):
        u.add_edge(node,v)
"""

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
data2 = data[:,PHQ9]


resp = [gcc.subgraph(data2['hashed_id']) for gcc in gccs]
good_dats = np.array([id in resp[0].node.keys() for id in data2['hashed_id']])

data2 = data2[:,good_dats]
medi = np.median(data2['PHQ9_score'])
PHQ9_low = data2['PHQ9_score'] <= medi
PHQ9_high = data2['PHQ9_score'] > medi
data_high = data2[:,PHQ9_high]
data_low = data2[:,PHQ9_low]

high = [gcc.subgraph(data_high['hashed_id']) for gcc in resp]

low = [gcc.subgraph(data_low['hashed_id']) for gcc in resp]

allccs = gccs + resp + high + low

names = [ "union-full", "union-all-induced", "union-high-induced", "union-low-induced"]
all_in_whole = resp + high + low
all_in_whole_names = [ "union-all-full",  "union-high-full","union-low-full"]

all_in_resp = high + low
all_in_resp_names = [ "union-high-all", "union-low-all"]


# ------------
# Get connected components
#
degs = [dict([(node, len(cc.neighbors(node))) for node in cc]) for cc in allccs]
graphfeatures (degs, "degs", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names)



# ============
# TRANSITIVITY
# ------------print "Computing transitivity"
transitivity = [nx.transitivity(g) for g in allccs]
print "transitivity"
for i in range(len(allccs)):
    print "%s & %f \\\\ \hline" % (names[i],transitivity[i])

exit(0)

# =========
# TRIANGLES
# ---------
print "Triangles"
triangles = [nx.triangles(g) for g in allccs]
graphfeatures (triangles, "triangles", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names)


"""
#print "Closenness"
#closeness_centrality = [nx.closeness_centrality(g) for g in allccs]
#graphfeatures (closeness_centrality, "closeness-centrality", allccs, names, all_in_whole, all_in_whole_names, a#ll_in_resp, all_in_resp_names)


#print "Betweenness"
#betweenness_centrality = [nx.betweenness_centrality(g) for g in allccs]
#graphfeatures (betweenness_centrality, "betweenness-centrality", allccs, names, all_in_whole, all_in_whole_name#s, all_in_resp, all_in_resp_names)

#print "Degree"
#degree_centrality = [nx.degree_centrality(g) for g in allccs]
#graphfeatures (degree_centrality, "degree-centrality", allccs, names, all_in_whole, all_in_whole_names, all_in_#resp, all_in_resp_names)
"""


# ============
# CLUSTERING
# ------------
print "Clustering..."
clustering = [nx.clustering(g) for g in allccs]
graphfeatures (clustering, "clustering", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names)

transitivity = [nx.transitivity(g) for g in allccs]
print "Finding clique numbers"
for i in range(4, len(allccs)):
    print "%s & %d \\\\ \hline" % (names[i],nx.graph_clique_number(allccs[i]))
    
# ============
# CORE_NUMBER
# ------------
print "Core_number..."
core_number = [nx.core_number(g) for g in allccs]
graphfeatures (core_number, "core_number", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names)

"""
# =============
# ASSORTATIVITY
# -------------
print "degree_assortativity_coefficient"
for i in range(0, len(allccs)):
    print "%s & %f \\\\ \hline" % (names[i],nx.degree_assortativity_coefficient(allccs[i]))


for datum in data:
    #    print datum
    for gr in all_in_whole:
        if gr.has_node(datum[0]):
            for i in range(1,len(datum)):
              if data.dtype.names[i].find("SURVEY") != 0:
                gr.node[datum[0]][data.dtype.names[i]] = datum[i]                


print ("\\begin{tabular}{l|r|r|r|r|r|r|r|r|r|r|r|r}")
print ("population & resp &&&& high &&&& low &&&&\\\\")
sys.stdout.write ("graph")
for nm in all_in_whole_names:
    sys.stdout.write (" & " +  nm.split("-")[0])
sys.stdout.write (" \\\\ \hline\n")
j = 1
for name in types:
    if j % 40 == 0:
        print ("\\end{tabular}") 
        print ("\\begin{tabular}{l|r|r|r|r|r|r|r|r|r|r|r|r}") 
        print ("population & resp &&&& high &&&& low &&&\\\\")
        sys.stdout.write ("graph")
        for nm in all_in_whole_names:
            sys.stdout.write (" & " + nm.split("-")[0])
        sys.stdout.write (" \\\\ \hline\n")

    if types[name] != np.float:
          st = name.split("_")
          print_name = " ".join(st)
          if len(name) > 20:
              print_name = print_name[len(name)-20:len(name)]
          sys.stdout.write (print_name)
          for i in range(len(all_in_whole)):
             val = nx.attribute_assortativity_coefficient(all_in_whole[i], name)
             if val > .2:
                 sys.stdout.write (" & {\\bf%.2f}" % val)
             else:
                 sys.stdout.write (" & %.2f" % val)
          sys.stdout.write ("\\\\ \hline \n")
          j += 1

print ("\\end{tabular}") 
"""

for i in range(len(allccs)):
    g = allccs[i]
    l = list()
    for node in g:
        g.node[node]["hashed_id"] = node
        
        l.append(g.node[node])
    f = open (names[i] + "-attr.json", 'w')
    f.write (json.dumps(l) + "\n")
    f.close()
