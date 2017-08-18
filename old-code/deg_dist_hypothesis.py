import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys
import random
import copy
import Queue


def countedges (subgraph, graph):
    dist = dict()
    for node in subgraph.nodes():
        count = 0.0
        for n in subgraph.neighbors(node):
            count += 1.0/(len(subgraph.neighbors(n)))
        if node in graph:
            lastarg = len(graph.neighbors(node))
        else:
            lastarg = 0
        dist[node] = (count, lastarg)
    return dist

#-------------------------------
# Test the sample against a probablistic model.
#
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
        #        print ("%s: %f" % (names[i], med))
        

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

def swapper (graph):
    nodes = set()
    othernodes = set()
    while (len(nodes) < count):
        seed = random.choice(graph.nodes())
        q = Queue.Queue()
        q.put(seed)
        othernodes.add(seed)
        while not q.empty():
            current = q.get()
            for nextnode in graph.neighbors(current):
                if nextnode not in othernodes:
                    roll = random.random()
                    if roll < percent:
                        q.put(nextnode)
                        othernodes.add(nextnode)
            nodes.add(current)
            if len(nodes) == count:
                break
    return graph.subgraph(nodes)


#-----------------------------
# Read Trevorspace survey data into a numpy data structure
#
data = np.genfromtxt('trevorspace_responses.csv',delimiter='^',dtype=None, autostrip=True, names=True)
types = defaultdict(np.dtype)
for i in range(1,len(data.dtype.names)):
    if data.dtype.names[i].find("SURVEY") != 0:
        types[data.dtype.names[i]] = data.dtype[i]

#-----------------------------
# Load two snapshots of the trevorspace graph and decorate the nodes of
# each with survey data.
#       
g = nx.read_edgelist('edges_encrypted_3-21-12.txt.mac', create_using=nx.Graph(), delimiter=',')
h = nx.read_edgelist('edges_encrypted_4-20-12.txt.mac', create_using=nx.Graph(), delimiter=',')

for datum in data:
    #    print datum
    for gr in (g, h):
        if gr.has_node(datum[0]):
            for i in range(1,len(datum)):
              if data.dtype.names[i].find("SURVEY") != 0:
                gr.node[datum[0]][data.dtype.names[i]] = datum[i]

#----------------------------
# Construct the union graph.
#
u = nx.compose(g,h)

#---------------------------------------
# Slice up the survey data to remove those who failed to answer
# all PHQ9 questions and to create sets of high and low
# PHQ9 respondents
#
PHQ9 = data['PHQ9_questions_answered'] >= 9
median_PHQ9_score = np.median (data['PHQ9_score'])
PHQ9_high = data['PHQ9_score'] >= 9
PHQ9_low = data['PHQ9_score'] < 9

data2 = data[:,PHQ9]
data_high = data[:,PHQ9_high]
data_low = data[:,PHQ9_low]
phqs = list(data2["PHQ9_score"])



# ------------------------------
# Get subgraphs and connectivity
#
graphs = [u]  # currently we are just using the union graph
ccs = graphs
gccs = ccs

resp = [gcc.subgraph(data2['hashed_id']) for gcc in gccs] # subgraph of just the respondents
respsize = len(resp[0].node)
resp_original = copy.copy(resp[0].node.keys())


deg_med = list()
triangle_med = list()
clustering_med = list()
core_number_med = list()
closeness_centrality_med = list()
betweenness_centrality_med = list()
degree_centrality_med = list()
lcc = list()

names = [ "union-full",  "union-all-induced"]
all_in_whole_names = [ "union-all-full"]

all_in_resp_names = [ "union-high-all", "union-low-all"]

#exit (0)

for r in range(10001):
    if r > 0:
        #resp = [snowball(gcc, .00337, 185) for gcc in gccs]
        resp = [swapper(res) for res in resp]

    allccs = gccs + resp 
    all_in_whole = resp
    all_in_resp = []

    # ============
    # CONNECTIVITY
    # ------------

    l = list()
    l.append(("cc", len(nx.connected_component_subgraphs(resp[0])[0].node)))
    l.append(("size", len(resp[0].node)))
    l.append(("overlap", len(np.intersect1d(resp_original, resp[0].node))))
    l.append(("clique", nx.graph_clique_number(resp[0])))
    l.append(("bicc", len(list(nx.biconnected_component_subgraphs(resp[0]))[0].node)))
    lcc.append(dict(l))
 
    if r == 0:
        degs = [dict([(node, len(cc.neighbors(node))) for node in cc]) for cc in allccs]
    else:
        for l in [1]:
            degs[l] = dict([(node, len(allccs[l].neighbors(node))) for node in allccs[l]])


    deg_med.append(graphfeatures (degs, "degs", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))

    """
    # ============
    # TRANSITIVITY
    # ------------
    print "Computing transitivity"
    # transitivity = [nx.transitivity(g) for g in allccs]
    #print "transitivity"
    #for i in range(len(allccs)):
    #    print "%s & %f \\\\ \hline" % (names[i],transitivity[i])
    if r == 0:
        closeness_centrality = [nx.closeness_centrality(g) for g in allccs]
    else:
        closeness_centrality[1] = nx.closeness_centrality(allcss[1])
    closeness_centrality_med.append(graphfeatures (closeness_centrality, "closeness-centrality", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))
    exit(0)
    
    if r == 0:
        betweenness_centrality = [nx.betweenness_centrality(g) for g in allccs]
    else:
        betweenness_centrality[1] = nx.betweenness_centrality(allcss[1])
    betweenness_centrality_med.append(graphfeatures (betweenness_centrality, "betweenness-centrality", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))

    if r == 0:
        degree_centrality = [nx.degree_centrality(g) for g in allccs]
    else:
        degree_centrality[1] = nx.degree_centrality(allccs[1])
    degree_centrality_med.append(graphfeatures (degree_centrality, "degree-centrality", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))

    """

    # =========
    # TRIANGLES
    # ---------


    if r == 0:
        triangles = [nx.triangles(g) for g in allccs]
    else:
        triangles[1] = nx.triangles(allccs[1])

    triangle_med.append(graphfeatures (triangles, "triangles", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))


    # ============
    # CLUSTERING
    # ------------
    print "Clustering..."
    if r == 0:
        clustering = [nx.clustering(g) for g in allccs]
    else:
        clustering[1] = nx.clustering(allccs[1])
    clustering_med.append(graphfeatures (clustering, "clustering", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))

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
        core_number[1] = nx.core_number(allccs[1])

    core_number_med.append(graphfeatures (core_number, "core_number", allccs, names, all_in_whole, all_in_whole_names, all_in_resp, all_in_resp_names))

    #  data_hi
    random.shuffle(data2['PHQ9_score'])
    PHQ9_high = data2['PHQ9_score'] >= 9
    PHQ9_low = data2['PHQ9_score'] < 9
    data_high = data2[:,PHQ9_high]
    data_low = data2[:,PHQ9_low]
    
    the_ids = list(u.node)
    samp = random.sample(the_ids, respsize)


files = [(lambda x: open(x, 'w'))(nm) for nm in ["degrees_snow_all.json", "triangles_snow_all.json", "clustering_snow_all.json", "core_number_snow_all.json", "lccs_snow.json","closeness_centrality_snow_all.json", "betweenness_centrality_snow_all.json", "degree_centrality_snow_all.json"]]

files[0].write (json.dumps(deg_med) + "\n")
files[1].write (json.dumps(triangle_med) + "\n")
files[2].write (json.dumps(clustering_med) + "\n")
files[3].write (json.dumps(core_number_med) + "\n")
files[4].write (json.dumps(lcc) + "\n")
files[2].write (json.dumps(closeness_centrality_med) + "\n")
files[3].write (json.dumps(betweenness_centrality_med) + "\n")
files[4].write (json.dumps(degree_centrality_med) + "\n")

files[0].close()
files[1].close()
files[2].close()
files[3].close()
files[4].close()
files[5].close()
files[6].close()
files[7].close()
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
