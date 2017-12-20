import networkx as nx
from collections import defaultdict
import random
import itertools
import networkx as nx
from collections import Counter
from collections import OrderedDict
import math
import numpy as np
import powerlaw #to install in linux use easy_install powerlaw
    


##Edge Clustering Coefficient
def ecc(e):
    return G[e[0]][e[1]]['ecc']

def ecc_single(G,e):
    numerator = len(list(nx.common_neighbors(G,e[0],e[1]))) + 1
    denominator = min(G.degree(e[0]), G.degree(e[1]))
    return (numerator / (denominator * 1.0))

#import numpy as np
#np.seterr(divide='ignore', invalid='ignore')
#import gzip
from optparse import OptionParser
usage="Usage: %prog -f <filename>"

parser = OptionParser(usage)

parser.add_option("-f", "--file", dest="stringFilename", help="File containing STRING interactions")
(options,args)=parser.parse_args()


if 'stringFilename' not in locals():
    options.stringFilename='158879'

G=nx.Graph()
datafile=open("ppi/%s.ppi" % (options.stringFilename))
for line in datafile:
    g=line.split(" ")
    if(int(g[15])>700):
        G.add_edges_from([(g[0],g[1])],weight=int(g[15]))
        print('%s %s with %s' % (g[0],g[1],g[15]))

ess_file = open('ess/%s.ess' % (options.stringFilename))
ess_proteins = []
for line in ess_file:
    ess_proteins.append(line.strip()) 
    print(ess_proteins[-1])

####2.ANALYZING THE NETWORK####
print("ANALYZING NETWORK")
centrality_measures = {}
#a)Degree
degreenew=nx.degree_centrality(G)
centrality_measures['Degree centrality']=degreenew

#b)The closeness centrality
closeness=Counter(nx.algorithms.centrality.closeness_centrality(G))
centrality_measures['Closeness Centrality']=closeness

#c)The betweenness centrality
betweenness=Counter(nx.algorithms.centrality.betweenness_centrality(G))
centrality_measures['Betweenness Centrality']=betweenness

#d)The clustering coefficient
clust_coeff=Counter(nx.clustering(G))
centrality_measures['Clustering Co-efficient']=clust_coeff
#e)eigenvector centrality
eigenc = nx.eigenvector_centrality(G)
centrality_measures['Eigenvector Centrality']=eigenc
#f)subgraph centrality
#subc=nx.communicability_centrality(G)

#g)information centrality
#inc=nx.current_flow_closeness_centrality(G)
cliq={}

#i)cliquenumber
for i in G.nodes():
   cliq[i]=nx.node_clique_number(G,i)

#j)edge clustering coefficient
for e in G.edges():
    G[e[0]][e[1]]['ecc'] = ecc_single(G,e)

edge_clus_coeff={}
for i in G.nodes():
    edge_clus_coeff[i]=sum(map(ecc,G.edges(i)))
centrality_measures['Edge Clustering Coefficient']=edge_clus_coeff

#pg
pg=nx.pagerank(G)
centrality_measures['Page Rank']=pg

for name, values in centrality_measures.items():
	ess_protein_measures = []
	non_ess_protein_measures = []
	
	for node, measure in values.items():
	    if node in ess_proteins:
	        ess_protein_measures.append(measure)
	        #print(measure)
	    else:
	        non_ess_protein_measures.append(measure)
	ess_protein_measures = np.array(ess_protein_measures)
	non_ess_protein_measures = np.array(non_ess_protein_measures)
	print(ess_protein_measures.mean())
	print(name)
	print("Ess:     %f %f \nNon_ess: %f %f" % (ess_protein_measures.mean(), ess_protein_measures.std(), non_ess_protein_measures.mean(), non_ess_protein_measures.std()))


#for i in degreenew.keys():
#i = ess_proteins[0]
#print(i,degreenew[i],closeness[i],betweenness[i],clust_coeff[i],eigenc[i],(cliq[i]/max(cliq.values())),(edge_clus_coeff[i]/max(edge_clus_coeff.values())),pg[i])


#def measuring_measures(centrality):
    
