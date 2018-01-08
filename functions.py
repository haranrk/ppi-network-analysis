import networkx as nx

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