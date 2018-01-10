import networkx as nx
from collections import Counter
import functions as f
def import_data(org_name=272635):
	G=nx.Graph()
	datafile=open("ppi/%s.ppi" % (org_name))
	print("Importing PPI data")
	for line in datafile:
		g=line.split(" ")
		if(int(g[15])>700):
			G.add_edges_from([(g[0],g[1])],weight=int(g[15]))
			#print('%s %s with %s' % (g[0],g[1],g[15]))

	ess_file = open('ess/%s.ess' % (org_name))
	ess_proteins = []
	for line in ess_file:
		ess_proteins.append(line.strip()) 
		#print(ess_proteins[-1])

	return G,ess_proteins

def import_data_with_weights(org_name=272635):
	G=nx.Graph()
	datafile=open("ppi/%s.ppi" % (org_name))
	print("Importing PPI data")
	for line in datafile:
		g=line.split(" ")
		G.add_edges_from([(g[0],g[1])],weight=float(g[15])/1000)
	return G

#Edge Clustering Coefficient
def ecc(G,e):
    return G[e[0]][e[1]]['ecc']

def ecc_single(G,e):
    numerator = len(list(nx.common_neighbors(G,e[0],e[1]))) + 1
    denominator = min(G.degree(e[0]), G.degree(e[1]))
    return (numerator / (denominator * 1.0))

#Removes all subgraphs except the largest
def trim_graph(G):
	sub_graphs=nx.connected_component_subgraphs(G)
	main_graph=list(sub_graphs)[0]
	for s in sub_graphs:
		if(main_graph.number_of_nodes()<s.number_of_nodes()):
			main_graph=s
	return main_graph

def calc_centralities(G):
	
    print("Calculating centralities")
    centrality_measures = {}
    
    print("1. Degree Centrality")
    centrality_measures['Degree centrality']=nx.degree_centrality(G)
    
    # print("2. Closeness centrality")
    # centrality_measures['Closeness Centrality']=Counter(nx.algorithms.centrality.closeness_centrality(G))
    
    # print("3. Betweenness centrality")
    # centrality_measures['Betweenness Centrality']=Counter(nx.algorithms.centrality.betweenness_centrality(G))
    
    # print("4. Clustering coefficient")
    # centrality_measures['Clustering Co-efficient']=Counter(nx.clustering(G))
    
    # print("5. Eigenvector centrality")
    # centrality_measures['Eigenvector Centrality']= nx.eigenvector_centrality(G)
    
    # print("6. Subgraph centrality")
    # centrality_measures["Subgraph"]=nx.subgraph_centrality(G)
    
    # print("7. Information centrality")
    # centrality_measures["Information Centrality"]=nx.current_flow_closeness_centrality(f.trim_graph(G))
    
    # print("8. Clique Number")
    # cliq={}
    # for i in G.nodes():
    #    cliq[i]=nx.node_clique_number(G,i)
    # centrality_measures["Clique Number"]=cliq
    
    # print("9. Edge clustering coefficient")
    # edge_clus_coeff={}
    # for n in G.nodes:
    # 	edge_clus_coeff[n]=0
    # 	for e in G.edges(n):
    # 		num=len(list(nx.common_neighbors(G,e[0],e[1])))
    # 		den=(min(G.degree(e[0]),G.degree(e[1]))-1)
    # 		if den==0:
    # 			den=1
    # 		edge_clus_coeff[n]+=num/den
    # # for e in G.edges():
    # #     G[e[0]][e[1]]['ecc'] = f.ecc_single(G,e)
    
    # # for i in G.nodes():
    # #     edge_clus_coeff[i]=sum(map(f.ecc(G,e),G.edges(i)))
    # centrality_measures['Edge Clustering Coefficient']=edge_clus_coeff
    
    # print("10. Page Rank")
    # centrality_measures['Page Rank']=nx.pagerank(G)
    
    # print("11. Random Walk Betweenness Centrality")
    # centrality_measures["Random Walk Betweenness Centrality"]=nx.current_flow_betweenness_centrality(f.trim_graph(G))
    
    # print("12. Load Centrality")
    # centrality_measures["Load Centrality"]=nx.load_centrality(G)
    
    # print("13. Communicability Betweenness")
    # centrality_measures["Communicability Betweenness"]=nx.communicability_betweenness_centrality(f.trim_graph(G))
    
    # print("14. Harmonic Centrality")
    # centrality_measures["Harmonic Centrality"]=nx.harmonic_centrality(G)
    	
    # print("15. Reaching Centrality")
    # reach_cent={}
    # for node in G.nodes:
    # 	reach_cent[node] = nx.local_reaching_centrality(G,node)
    # centrality_measures["Reaching Centrality"]=reach_cent
    
    # print("16. Katz Centrality")
    #centrality_measures["Katz Centrality"]=nx.katz_centrality(G)

    return centrality_measures
