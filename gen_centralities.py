#Calculates the centralities for the default organism and writes it to a csv file
import functions as f
import networkx as nx

G,ess=f.import_data()
dics=f.calc_centralities(G)
with open('TCSV.csv','w') as g:
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