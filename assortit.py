import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys
import random

def graphfeatures (feats, name, allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names):
    
    print "Computing " + name 
    #    triangles = [nx.triangles(g) for g in allccs]
    outputs = list()
    for i in range(len(allccs)):
        l = list()
        for node in feats[i]:
            l.append(feats[i][node])
        med = np.median(l)
        #fh.write("\t%f" % med)
        outputs.append((names[i], med))
        print ("%s: %f" % (names[i], med))
        

    for i in range(len(all_in_whole)):
       l = list()
       for node in all_in_whole[i]:
            l.append (feats[0][node])
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
ccs = [nx.connected_component_subgraphs(graph) for graph in graphs]
gccs = [cc[0] for cc in ccs]

data2 = data[:,PHQ9]
data_high = data[:,PHQ9_high]
data_low = data[:,PHQ9_low]
#data_high = list(data[:,PHQ9_high])
#data_low = list(data[:,PHQ9_low])

phqs = list(data2["PHQ9_score"])



resp = [gcc.subgraph(data2['hashed_id']) for gcc in gccs]
resp = [nx.connected_component_subgraphs(graph) for graph in resp]
resp = [cc[0] for cc in resp]



deg_med = list()
triangle_med = list()
clustering_med = list()
core_number_med = list()
lcc = list()

names = [ "union-full",  "union-all-induced", "union-high-induced", "union-low-induced"]
all_in_whole_names = [ "union-all-full", "union-high-full", "union-low-full"]

all_in_resp_names = [ "union-high-all", "union-low-all"]

high = [gcc.subgraph(data_high['hashed_id']) for gcc in resp]
high = [nx.connected_component_subgraphs(graph) for graph in high]
high = [cc[0] for cc in high]

low = [gcc.subgraph(data_low['hashed_id']) for gcc in resp]
low = [nx.connected_component_subgraphs(graph) for graph in low]
low = [cc[0] for cc in low]
allccs = gccs + resp + high + low
all_in_whole = resp + high + low
all_in_resp = high + low

# =============
# ASSORTATIVITY
# -------------
#print "degree_assortativity_coefficient"
#for i in range(0, len(allccs)):
#    print "%s & %f \\\\ \hline" % (names[i],nx.degree_assortativity_coefficient(allccs[i]))


for datum in data:
    #   print datum
    for gr in all_in_whole:
        if gr.has_node(datum[0]):
            for i in range(1,len(datum)):
              if data.dtype.names[i].find("SURVEY") != 0:
                gr.node[datum[0]][data.dtype.names[i]] = datum[i]                


print ("\\begin{tabular}{l|r|r|r}")
print ("population & resp & high & low\\\\")
sys.stdout.write ("graph")
for nm in all_in_whole_names:
    sys.stdout.write (" & " +  nm.split("-")[0])
sys.stdout.write (" \\\\ \hline\n")
j = 1

assorts=["al attracted females","Comment on pictures","m Flirt with someone","et other than online","watching television","n touch with friends","ng things Play games","l shortcoming for me","restless fidgety","ced any of the above","e of a family member","idence hall director","year Missed a class","sibling Halfsibling","following ADD ADHD","x birth assigned sex","ose you used Twitter","Compulsive Disorder","hem Find old friends","ing emotional issues","Comment on statuses","would accept chance","ou consider yourself","ose you used MySpace","following Depression","alcohol last 30 days"]
for name in types:
    if j % 40 == 0:
        print ("\\end{tabular}") 
        print ("\\begin{tabular}{l|r|r|r}") 
        print ("population & resp & high & low\\\\")
        sys.stdout.write ("graph")
        for nm in all_in_whole_names:
            sys.stdout.write (" & " + nm.split("-")[0])
        sys.stdout.write (" \\\\ \hline\n")

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
             if val > .2:
                 sys.stdout.write (" & {\\bf%.2f}" % val)
             else:
                 sys.stdout.write (" & %.2f" % val)
          sys.stdout.write ("\\\\ \hline \n")
          j += 1

print ("\\end{tabular}")

