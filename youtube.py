import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pdb
import random
import traceback
import networkx as nx
import json as json
#import plotly.plotly as py
from collections import defaultdict, OrderedDict
import sys
import json

#names = [ "union-full",  "union-all-induced",  "union-high-induced",  "union-low-induced"]
all_in_whole_names = ["", "hirisk", "lorisk"]

#all_in_resp_names = ["hirisk", "lorisk"]

def graphfeatures (feats, name, allccs, all_in_whole_names):
    
    #global all_in_whole_names
    #global all_in_resp_names
    print "Computing " + name 
    #    triangles = [nx.triangles(g) for g in allccs]

    outputs = list()
    for i in [1,2]:
    	l = list()
    	for node in allccs[i]:
    		l.append (feats[0][node])
    		#   l.sort()
	        med = np.mean(l)
	        outputs.append((all_in_whole_names[i], med))
                      #       fh.write("\t%f" % np.median(l))
    return dict(outputs)


def main ():
    global all_in_whole_names
    global all_in_resp_names
    name = sys.argv[1]


    g = nx.read_graphml(name).to_undirected(reciprocal=False)
    g = nx.Graph(g)
    g.remove_edges_from(g.selfloop_edges())
    hirisk = g.subgraph([x for x in g.nodes() if g.node[x]["hasrisk"] != "0"])
    lorisk = g.subgraph([x for x in g.nodes() if g.node[x]["hasrisk"] == "0"])

    oldsize = len(hirisk)

    lcc = list()
    deg_med = list()
    triangle_med = list()
    clustering_med = list()
    core_number_med = list()
    sze = list()
    clique = list()
    bicc = list ()
    path_len = list()
    for r in range(1001):
    
        try: 
	    

		    allccs = [g] + [hirisk] + [lorisk]
		    #allccs = [x.to_undirected() for x in allccs]
		    #allcss = [nx.Graph(x) for x in allccs]

		    # ============
		    # CONNECTIVITY
		    # ------------

		    #print "Size of largest connected components"
		    # for i in range(len(allccs)):
		    #    print "%s & %d \\\\ \hline" % (names[i],len(allccs[i].node))
		    l = dict()

		    cchi = sorted(nx.connected_component_subgraphs(hirisk.to_undirected()), key=lambda x: -len(x))[0]
		    cclow = sorted(nx.connected_component_subgraphs(lorisk.to_undirected()), key=lambda x: -len(x))[0]
		    #pdb.set_trace()
		    lcc.append({"hirisk" : len(cchi.node), "lorisk": len(cclow.node)})
		    sze.append({"hirisk": hirisk.node, "lorisk":lorisk.node})
		    #l.append(("overlap.hirisk", len(np.intersect1d(hirisk_original["hashed_id"], hirisk.node.keys()))))
		    #l.append(("overlap.lorisk", len(np.intersect1d(lorisk_original["hashed_id"], lorisk.node.keys()))))
		    clique.append({"hirisk":nx.graph_clique_number(hirisk.to_undirected()), "lorisk": nx.graph_clique_number(lorisk.to_undirected())})
		    bicc.append({"hirisk" : len(sorted(nx.biconnected_component_subgraphs(hirisk.to_undirected()), key=lambda x: -len(x))[0].node), "lorisk" :len(sorted(nx.biconnected_component_subgraphs(lorisk.to_undirected()), key=lambda x: -len(x))[0].node)})
		    
		    path_len.append({"hirisk":nx.average_shortest_path_length(cchi), "lorisk": nx.average_shortest_path_length(cclow)})
		    
		    if r == 0:
		        degs = [dict([(node, len(cc.neighbors(node))) for node in cc]) for cc in allccs]
		    else:
		        for l in [1,2]:
		            degs[l] = dict([(node, len(allccs[l].neighbors(node))) for node in allccs[l]])


		    deg_med.append(graphfeatures (degs, "degs", allccs, all_in_whole_names))
		    '''
		    if r > 0:
		        if deg_med[-1][all_in_whole_names[1]] - deg_med[-1][all_in_whole_names[0]] > deg_med[0][all_in_whole_names[1]] - deg_med[0][all_in_whole_names[0]]:
		            for node in allccs[3].node.keys():
		                d = {"feature" : "deg_number", "graphnum" : graphnum, "node": node}
		                funnygraphs.append(d)
		            graphnum += 1
		    '''

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
		        for l in [1,2]:
		            triangles[l] = nx.triangles(allccs[l])
		    triangle_med.append(graphfeatures (triangles, "triangles", allccs, all_in_whole_names))
		    '''
		    if r > 0:
		        if triangle_med[-1][all_in_whole_names[2]] - triangle_med[-1][all_in_whole_names[1]] > triangle_med[0][all_in_whole_names[2]] - triangle_med[0][all_in_whole_names[1]]:
		            for node in allccs[3].node.keys():
		                d = {"feature" : "triangle", "graphnum" : graphnum, "node": node}
		                funnygraphs.append(d)
		            graphnum += 1
		    '''

		    # ============
		    # CLUSTERING
		    # ------------
		    print "Clustering..."
		    if r == 0:
		        clustering = [nx.clustering(g) for g in allccs]
		    else:
		        for l in [1,2]:
		            clustering[l] = nx.clustering(allccs[l])
		    clustering_med.append(graphfeatures (clustering, "clustering", allccs, all_in_whole_names))
		    '''
		    if r > 0:
		        if clustering_med[-1][all_in_whole_names[2]] - clustering_med[-1][all_in_whole_names[1]] < clustering_med[0][all_in_whole_names[2]] - clustering_med[0][all_in_whole_names[1]]:
		            for node in allccs[3].node.keys():
		                d = {"feature" : "clustering", "graphnum" : graphnum, "node": node}
		                funnygraphs.append(d)
		            graphnum += 1
		    '''

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
		        for l in [1,2]:
		            core_number[l] = nx.core_number(allccs[l])

		    core_number_med.append(graphfeatures (core_number, "core_number", allccs, all_in_whole_names))
		    '''
		    if r > 0:
		        if core_number_med[-1][all_in_whole_names[2]] - core_number_med[-1][all_in_whole_names[1]] > core_number_med[0][all_in_whole_names[2]] - core_number_med[0][all_in_whole_names[1]] :
		            for node in allccs[3].node.keys():
		                d = {"feature" : "core_number", "graphnum" : graphnum, "node": node}
		                funnygraphs.append(d)
		            graphnum += 1
		    '''

		    

        except IndexError:
            #ex.printStackTrace(sys.stdout)
            traceback.print_exc(file=sys.stdout)
            print (set(hirisk.nodes()))

        hirisk = g.subgraph(random.sample(g.nodes(), oldsize))
        lorisk = g.subgraph(set(g.nodes()) - set(hirisk.nodes()))

    for (name, data) in [('ave_path_len', path_len), ('core_number', core_number_med), ('triangles', triangle_med), ('clustering', clustering_med), ('lccs', lcc), ('degrees', deg_med),  ("clique", clique), ("biconnected size", bicc)]:
        f = open(name + "_med.json", "wo")
        # ("size", size),
        json.dump(data, f)
        f.close()

        print "Computing " + name
        nums = [x["lorisk"] - x["hirisk"] for x in data]
        plt.hist(nums, bins=20)
        plt.title(name)
        plt.xlabel("Value") 
        plt.ylabel("Frequency")
        plt.axvline(x=nums[0], color='r', linestyle='dashed', linewidth=10)
        plt.savefig(name + "_med.pdf")
        #fig = plt.gcf()

        #plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
        plt.clf()


    #pdb.set_trace()


if __name__ == "__main__":
        main()
