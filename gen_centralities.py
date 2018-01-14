#Calculates the centralities for the default organism and writes it to a csv file
import functions as f
import networkx as nx

org_name=272635
G,ess=f.import_data(org_name)
dics=f.calc_centralities(G)
with open('centrality_data/%s.csv' % (org_name),'w') as g:
	for nd in G.nodes():
		tbw=(nd+',')
		for name,value in dics.items():
			if nd not in value.keys():
				tbw+=('-1')+', '
			else:
				tbw+=(str(value[nd]))+', '
							
		if nd in ess:
			tbw+=("1")
		else:
			tbw+=("0")
		tbw+=("\n")
		g.write(tbw)