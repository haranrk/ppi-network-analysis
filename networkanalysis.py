import networkx as nx
from collections import defaultdict
import random
import itertools
import networkx as nx
from collections import Counter
from collections import OrderedDict
import math
import numpy as np
#import powerlaw #to install in linux use easy_install powerlaw
import functions as f    
from optparse import OptionParser

usage="Usage: %prog -f <filename>"
parser = OptionParser(usage)
parser.add_option("-f", "--file", dest="org_name", help="Organism ID")
(options,args)=parser.parse_args()

if 'org_name' not in locals():
	G,ess_proteins = f.import_data()    
else:
	G,ess_proteins = f.import_data(org_name)

####2.ANALYZING THE NETWORK####
print("Analysing Network")
centrality_measures = {}

print("1. Degree Centrality")
degreenew=nx.degree_centrality(G)
centrality_measures['Degree centrality']=degreenew

print("2. Closeness centrality")
closeness=Counter(nx.algorithms.centrality.closeness_centrality(G))
centrality_measures['Closeness Centrality']=closeness

print("3. Betweenness centrality")
betweenness=Counter(nx.algorithms.centrality.betweenness_centrality(G))
centrality_measures['Betweenness Centrality']=betweenness

print("4. Clustering coefficient")
clust_coeff=Counter(nx.clustering(G))
centrality_measures['Clustering Co-efficient']=clust_coeff

print("5. Eigenvector centrality")
eigenc = nx.eigenvector_centrality(G)
centrality_measures['Eigenvector Centrality']=eigenc

print("6. Subgraph centrality")
subc=nx.subgraph_centrality(G)
centrality_measures["Subgraph"]=subc

print("7. Information centrality")
inc=nx.current_flow_closeness_centrality(f.trim_graph(G))
centrality_measures["Information Centrality"]=inc

print("8. Clique Number")
cliq={}
for i in G.nodes():
   cliq[i]=nx.node_clique_number(G,i)
centrality_measures["Clique Number"]=cliq

print("9. Edge clustering coefficient")
edge_clus_coeff={}
for n in G.nodes:
	edge_clus_coeff[n]=0
	for e in G.edges(n):
		num=len(list(nx.common_neighbors(G,e[0],e[1])))
		den=(min(G.degree(e[0]),G.degree(e[1]))-1)
		if den==0:
			den=1
		edge_clus_coeff[n]+=num/den
# for e in G.edges():
#     G[e[0]][e[1]]['ecc'] = f.ecc_single(G,e)

# for i in G.nodes():
#     edge_clus_coeff[i]=sum(map(f.ecc(G,e),G.edges(i)))
centrality_measures['Edge Clustering Coefficient']=edge_clus_coeff

print("10. Page Rank")
pg=nx.pagerank(G)
centrality_measures['Page Rank']=pg

print("11. Random Walk Betweenness Centrality")
rwbc=nx.current_flow_betweenness_centrality(f.trim_graph(G))
centrality_measures["Random Walk Betweenness Centrality"]=rwbc

print("12. Load Centrality")
load_cent=nx.load_centrality(G)
centrality_measures["Load Centrality"]=load_cent

print("13. Communicability Betweenness")
communicability_betweenness=nx.communicability_betweenness_centrality(f.trim_graph(G))
centrality_measures["Communicability Betweenness"]=communicability_betweenness

print("14. Harmonic Centrality")
harmonic_cent=nx.harmonic_centrality(G)
centrality_measures["Harmonic Centrality"]=harmonic_cent
	
print("15. Reaching Centrality")
reach_cent={}
for node in G.nodes:
	reach_cent[node] = nx.local_reaching_centrality(G,node)
centrality_measures["Reaching Centrality"]=reach_cent

print("16. Katz Centrality")
katz_cent=nx.katz_centrality(G)
centrality_measures["Katz Centrality"]

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
	print(name)
	print("Ess:     %f %f \nNon_ess: %f %f \n" % (ess_protein_measures.mean(), ess_protein_measures.std(), non_ess_protein_measures.mean(), non_ess_protein_measures.std()))





#for i in degreenew.keys():
#i = ess_proteins[0]
#print(i,degreenew[i],closeness[i],betweenness[i],clust_coeff[i],eigenc[i],(cliq[i]/max(cliq.values())),(edge_clus_coeff[i]/max(edge_clus_coeff.values())),pg[i])


#def measuring_measures(centrality):
    
