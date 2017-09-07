# usage: python time_series_analyze.py interval
# e.g. python time_series_analyze.py 9
# will run over all graph file w/ the name, e.g.,
# 9_digraph_2013-07-24_2013-09-29.gexf
import time
import networkx as nx
import pickle
import sys
import os
import operator
import pdb
import nltk
import ntpath
import pandas as pd
import numpy as np
import matplotlib
import csv
import sys
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import liwc.categories
#import concurrent
#from concurrent.futures import ProcessPoolExecutor
#from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool, Process, Manager

# pool_size = 3  # your "parallelness"
# pool = Pool(pool_size)


labels = ["first_person", "second_person", "third_person", "posemo", "negemo", "cognitive", "sensory", "time", "past", "present", "future", "work", "leisure", "swear", "social", "family", "friend", "humans", "anx", "anger",
          "sad", "body", "health", "sexual", "space", "time", "achieve", "home", "money", "relig", "Affect", "cause", "Quant", "Numb", "inhib", "ingest", "motion", "nonfl", "filler", "number_classified_words", "number_words"]

ListOfDicts = []

listOfDicts = []
listOfLIWCDictsPosts = []
listOfLIWCDictsComments = []


def order(frame, var):
    varlist = [w for w in frame.columns if w not in var]
    frame = frame[var + varlist]
    return frame


def get_graph_measures(g):
    retdic = dict()

    u = g.to_undirected()
    ccs = nx.weakly_connected_components(g)
    ccs = list(ccs)
    # pdb.set_trace()
    max_ccsl = max([len(x) for x in ccs])
    max_cc = [x for x in ccs if len(x) == max_ccsl][0]
    c = nx.core_number(g)
    max_subgraph = g.subgraph(max_cc).to_undirected()
    centrality = list(nx.closeness_centrality(g).values())
    max_cent = max(centrality)

    # pdb.set_trace()
    return {'ave. shortest path': nx.average_shortest_path_length(max_subgraph),
            'cluster coefficient': nx.average_clustering(u),
            'lcc': max_ccsl,
            'ncc': len(ccs),
            'triangles': np.mean(nx.triangles(u).values()),
            'degree': np.mean(nx.average_neighbor_degree(g).values()),
            'core': np.mean(list(nx.core_number(g).values())),
            'diameter': nx.diameter(max_subgraph),
            'centrality': np.mean(centrality),
            'centralization': np.mean([max_cent - x for x in centrality]) / len(centrality)}


def getLIWCDictForText(text):
    global labels

    d = dict()
    vals = liwc.categories.classify(text)
    for i in range(0, len(vals)):
        d[labels[i]] = 100 * vals[i] / float(vals[40])
    return d


def getLIWC(g):
    postsText = " ".join([g.node[x]['text'] for x in g])
    commentsText = " ".join([g.edge[x][y]['text'] for x, y in g.edges()])
    return (getLIWCDictForText(postsText), getLIWCDictForText(commentsText))


def drawMe(thisList, fileName, window):
    df = pd.DataFrame(thisList)

    dp = df.plot(subplots=True, figsize=(6, 25), fontsize=6,
                 yticks=(0.00, 1.00, 2.00, 3.00, 4.00))

    plt.savefig('LIWC_DATA/LIWC_OUTPUT/' + window +
                "-" + fileName + '-measures.pdf')

    plt.clf()
    file('LIWC_DATA/LIWC_OUTPUT/%s-graph-%s.html' %
         (window, fileName), 'w').write(df.to_html())
    file('LIWC_DATA/LIWC_OUTPUT/%s-graph-%s.csv' %
         (window, fileName), 'w').write(df.to_csv())


def tryMultiThread(filepath, que): 
    file = ntpath.basename(filepath)
    if not file.startswith("%s_di" % sys.argv[1]):
        return
    print "Processing %s" % file
    g = nx.read_gexf(filepath)  # HACK for top dir
    (posts, comments) = getLIWC(g)
    
    g.remove_edges_from(g.selfloop_edges())
    graph =  get_graph_measures(g)

    threadData = {filepath + "_graph":graph,filepath + "_posts":posts,filepath + "_comments":comments}
    que.put(threadData)
    print 'Done %s' % file
    return threadData

def log_result(result):
    for k,v in result.items():
        data = k.split("/")
        newname = data[2].replace('.gexf','')
        file = open('LIWC_DATA/CSV/out_'+newname+'.csv','w')
        for key,value in v.items():
            file.write(key+','+str(value)+'\n')
        file.close()

def joinFiles():
    graphFileList = []
    postsFileList = []
    commentFileList = []
    for filename in os.listdir("LIWC_DATA/CSV/"):
        if 'posts' in filename: postsFileList.append(filename)
        elif 'comments' in filename: commentFileList.append(filename)
        elif 'graph' in filename: graphFileList.append(filename)
    graphFileList = sorted(graphFileList)
    postsFileList = sorted(postsFileList)
    commentFileList = sorted(commentFileList)
    
    for file in graphFileList:
        with open('LIWC_DATA/CSV/'+file) as f:
            d = {}
            for line in f:
                (key, val) = line.split(',')
                d[key] = float(val)
            listOfDicts.append(d)
    for file in postsFileList:
        with open('LIWC_DATA/CSV/'+file) as f:
            d = {}
            for line in f:
                (key, val) = line.split(',')
                d[key] = float(val)
            listOfLIWCDictsPosts.append(d)
    for file in commentFileList:
        with open('LIWC_DATA/CSV/'+file) as f:
            d = {}
            for line in f:
                (key, val) = line.split(',')
                d[key] = float(val)
            listOfLIWCDictsComments.append(d)   



if __name__ == '__main__':
    pool = Pool(processes=4)
    manager = Manager()
    que = manager.Queue()
    fileList = []
    count = 0
    for filename in os.listdir("LIWC_DATA/utility_graphs/"):

        count += 1
        print filename, count
        D = {}
        if not filename.startswith("%s_di" % sys.argv[1]):
            continue
        fileList.append(filename) 

        g = nx.read_gexf('LIWC_DATA/utility_graphs/' +
                         filename)  # HACK for top dir

        # this is where we hadnle selfloop edges
        g.remove_edges_from(g.selfloop_edges())
        D['numNodes/10'] = len(g.nodes()) / 10

        # find elements with highest core number
        sorted_by_core_number = sorted(nx.core_number(g).items(), key=operator.itemgetter(1))
        max_core_number = sorted_by_core_number[-1][1]
        
        # report on strongly connected components
        size_of_sccs = [len(x) for x in nx.strongly_connected_components(g)]
        #print (filename)
        D['filename'] = filename[10:-5]

        #print ("max_core_number: %d" % max_core_number)
        D['max_core_number'] = max_core_number

        #print ("nontrivial sccs:")
        #print ([x for x in size_of_sccs if x > 1])
        D['nontrivial sccs'] = ([x for x in size_of_sccs if x > 1])
        D['len NT sccs'] = len(D['nontrivial sccs'])

        g.remove_nodes_from([x for x, y in nx.core_number(g).items() if y == max_core_number])

        sorted_by_core_number = sorted(nx.core_number(g).items(), key=operator.itemgetter(1))
        
        max_core_number = sorted_by_core_number[-1][1]

        # report on strongly connected components
        size_of_sccs = [len(x) for x in nx.strongly_connected_components(g)]

        #print ("max_core_number: %d" % max_core_number)
        D['NT max_core_number'] = max_core_number

        #print ("nontrivial sccs:")
        #print ([x for x in size_of_sccs if x > 1])
        D['NT nontrivial sccs'] = ([x for x in size_of_sccs if x > 1])
        D['len NT nontrivial sccs'] = len(D['NT nontrivial sccs'])

        #print ("")
        ListOfDicts.append(D)
        print "Read files"
        # pdb.set_trace()
    df = pd.DataFrame(ListOfDicts)
    df = order(df, ['filename', 'max_core_number',  'nontrivial sccs',
                    'NT nontrivial sccs', 'NT max_core_number'])
    dp = df.plot()
    dp.legend(loc='upper left', fontsize=7)

    fileList = sorted(fileList)

    # run in parallel utilizing the processors
    for filename in fileList:
        pool.apply_async(
            tryMultiThread, ('LIWC_DATA/utility_graphs/' + filename, que), callback = log_result)

    pool.close()
    # wait for all the threads to finish
    pool.join()

    joinFiles()

    drawMe(listOfDicts, "graph", sys.argv[1])
    drawMe(listOfLIWCDictsPosts, "LIWC-posts", sys.argv[1])
    drawMe(listOfLIWCDictsComments, "LIWC-comments", sys.argv[1])
