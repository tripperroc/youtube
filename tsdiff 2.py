import numpy as np
import scipy as sp
import networkx as nx
import json as json
from collections import defaultdict, OrderedDict
import sys

"""
getting data into R
d <- fromJSON(file="union-full-core_number.json", method="C")
e <- unlist(lapply(d, function(x) return (x[[1]])))
summary(e)
"""

data = np.genfromtxt('trevorspace_responses.csv',delimiter='^',dtype=None, autostrip=True, names=True)
types = defaultdict(np.dtype)
for i in range(1,len(data.dtype.names)):
    if data.dtype.names[i].find("SURVEY") != 0:
        types[data.dtype.names[i]] = data.dtype[i]




# use data.dtype.names to get field names
#print data.dtype.names
PHQ9 = data['PHQ9_questions_answered'] >= 9
median_PHQ9_score = np.median (data['PHQ9_score'])
PHQ9_high = data['PHQ9_score'] > median_PHQ9_score
PHQ9_low = data['PHQ9_score'] <= median_PHQ9_score

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

inter = nx.Graph() # the intersection graph
for node in g.nodes_iter():
    if h.has_node (node):
        inter.add_node(node)
    for v in g.neighbors (node):
        if h.has_edge (node, v):
            inter.add_edge(node,v)

            #o = nx.Graph () # the old ed
# ==============================
# Get subgraphs and CONNECTIVITY
# ------------------------------
graphs = [g,h,u,inter]
ccs = [nx.connected_component_subgraphs(graph) for graph in graphs]
gccs = [cc[0] for cc in ccs]

data2 = data[:,PHQ9]
data_high = data[:,PHQ9_high]
data_low = data[:,PHQ9_low]


resp = [gcc.subgraph(data2['hashed_id']) for gcc in gccs]
resp = [nx.connected_component_subgraphs(graph) for graph in resp]
resp = [cc[0] for cc in resp]

high = [gcc.subgraph(data_high['hashed_id']) for gcc in resp]
high = [nx.connected_component_subgraphs(graph) for graph in high]
high = [cc[0] for cc in high]

low = [gcc.subgraph(data_low['hashed_id']) for gcc in resp]
low = [nx.connected_component_subgraphs(graph) for graph in low]
low = [cc[0] for cc in low]



#allccs = gccs + resp + high + low

#names = ["mar-full", "apr-full", "union-full", "inter-full", "mar-phq", "apr-phq", "union-phq", "inter-phq", "mar-high", "apr-high", "union-high", "inter-high", "mar-low", "apr-low", "union-low", "inter-low"]
names = ["diff-full", "diff-all-induced", "diff-high-induced", "diff-low-induced"]
allccs = [ gccs, resp, high, low]
all_in_whole = resp + high + low
#all_in_whole_names = ["mar-resp-all", "apr-resp-all", "union-resp-all", "inter-resp-all","mar-high-all", "apr-high-all", "union-high-all", "inter-high-all","mar-low-all", "apr-low-all", "union-low-all", "inter-low-all"]
all_in_whole_names = ["diff-all-full", "diff-high-full", "diff-low-full"]

all_in_whole = [resp, high, low]
all_in_resp = high + low

all_in_resp_names = ["mar-high-all", "apr-high-all", "union-high-all", "inter-high-all","mar-low-resp", "apr-low-resp", "union-low-resp", "inter-low-resp"]
all_in_resp_names = ["diff-high-all", "diff-low-all"]

all_in_resp = [high, low]

val = [0.0,0.0]


"""

# ============
# CONNECTIVITY
# ------------

print "Size of largest connected components"
for i in range(len(allccs)):
    print "%s & %d \\\\ \hline" % (names[i],len(allccs[i].node))

#degs = [((node, len(cc.neighbors(node))) for node in cc.node) for cc in allccs]
"""

# ===================
# DEGREE DISTRIBUTION
# -------------------
print "Computing degree distribution"
for i in range(len(allccs)):
    f = open (names[i] + "-degs.json", 'w')
    l = list()
    for node in allccs[i][2]:
      for j in [0,1]:
        if allccs[i][j].has_node(node):
          val[j] = len(allccs[i][j].neighbors(node))
        else:
          val[j] = 0
        l.append({"hash_id": node, "degree": val[0]-val[1]})
    f.write (json.dumps(l) + "\n") 
    f.close ()


for i in range(len(all_in_whole)):
  f = open (all_in_whole_names[i] + "-degs.json", 'w')
  l = list()
  for node in all_in_whole[i][2]:
      for j in [0,1]:
        if gccs[j].has_node(node):
          val[j] = len(gccs[j].neighbors(node))
        else:
          val[j] = 0
      l.append ({"hash_id": node, "degree": val[1]-val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()
  
for i in range(len(all_in_resp)):
  f = open (all_in_resp_names[i] + "-degs.json", 'w')
  l = list()
  for node in all_in_resp[i][2]:
      for j in [0,1]:
        if resp[j].has_node(node):
          val[j] = len(resp[j].neighbors(node))
        else:
          val[j] = 0
      l.append ({"hash_id": node, "degree": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()




# =========
# TRIANGLES
# ---------
print "Computing triangles"
triangles = [nx.triangles(g) for g in [gccs[0],gccs[1],resp[0], resp[1],high[0], high[1], low[0], low[1]]]
for i in range(len(allccs)):
    filename = names[i] + "-triangles.json"
    print filename
    f = open (filename, 'w')
    l = list()
    for node in allccs[i][2]:
      for j in [0,1]:
        if node in triangles[2*i+j]:
          val[j] = triangles[2*i+j][node]
        else:
          val[j] = 0
      l.append ({"hash_id": node, "triangles": val[1]- val[0]})
    f.write (json.dumps(l) + "\n")
    f.close ()

for i in range(len(all_in_whole)):
  f = open (all_in_whole_names[i] + "-triangles.json", 'w')
  l = list()
  for node in all_in_whole[i][2]:
    for j in [0,1]:
      if node in triangles[j]:
        val[j] = triangles[j][node]
      else:
        val[j] = 0
    l.append ({"hash_id": node, "triangles": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()

for i in range(len(all_in_resp)):
  f = open (all_in_resp_names[i] + "-triangles.json", 'w')
  l = list()
  for node in all_in_resp[i][2]:
    for j in [0,1]:
      if node in triangles[j+2]:
        val[j] = triangles[j+2][node]
      else:
        val[j] = 0
    l.append ({"hash_id": node, "triangles": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()


# ============
# CLUSTERING
# ------------
print "Clustering..."
clustering = [nx.clustering(g) for g in [gccs[0],gccs[1],resp[0], resp[1],high[0], high[1], low[0], low[1]]]
for i in range(len(allccs)):
    f = open (names[i] + "-clustering.json", 'w')
    l = list()
    for node in allccs[i][2]:
      for j in [0,1]:
        if node in clustering[2*i+j]:
          val[j] = clustering[2*i+j][node]
        else:
          val[j] = 0
      l.append ({"hash_id": node, "clustering": val[1]- val[0]})
    f.write (json.dumps(l) + "\n") 
    f.close ()

for i in range(len(all_in_whole)):
  f = open (all_in_whole_names[i] + "-clustering.json", 'w')
  l = list()
  for node in all_in_whole[i][2]:
    for j in [0,1]:
      if node in clustering[j]:
        val[j] = clustering[j][node]
      else:
        val[j] = 0
    l.append ({"hash_id": node, "clustering": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()

for i in range(len(all_in_resp)):
  f = open (all_in_resp_names[i] + "-clustering.json", 'w')
  l = list()
  for node in all_in_resp[i][2]:
    for j in [0,1]:
      if node in clustering[j+2]:
        val[j] = clustering[j+2][node]
      else:
        val[j] = 0
    l.append ({"hash_id": node, "clustering": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()


# ============
# CORE_NUMBER
# ------------
print "Core_number..."
core_number = [nx.core_number(g) for g in [gccs[0],gccs[1],resp[0], resp[1],high[0], high[1], low[0], low[1]]]
for i in range(len(allccs)):
    f = open (names[i] + "-core_number.json", 'w')
    l = list()
    for node in allccs[i][2]:
      for j in [0,1]:
        if node in core_number[2*i+j]:
          val[j] = core_number[2*i+j][node]
        else:
          val[j] = 0
      l.append ({"hash_id": node, "core_number": val[1]- val[0]})
    f.write (json.dumps(l) + "\n") 
    f.close ()

for i in range(len(all_in_whole)):
  f = open (all_in_whole_names[i] + "-core_number.json", 'w')
  l = list()
  for node in all_in_whole[i][2]:
    for j in [0,1]:
      if node in core_number[j]:
        val[j] = core_number[j][node]
      else:
        val[j] = 0
    l.append ({"hash_id": node, "core_number": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()

for i in range(len(all_in_resp)):
  f = open (all_in_resp_names[i] + "-core_number.json", 'w')
  l = list()
  for node in all_in_resp[i][2]:
    for j in [0,1]:
      if node in core_number[j+2]:
        val[j] = core_number[j+2][node]
      else:
        val[j] = 0
    l.append ({"hash_id": node, "core_number": val[1]- val[0]})
  f.write (json.dumps(l) + "\n") 
  f.close ()

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
