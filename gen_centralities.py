#Calculates the centralities and stores it in centrality_data/org_name.cent
import functions as f
import networkx as nx

org_name=158879
G,ess=f.import_data(org_name)
dicshs=f.calc_centralities(G,org_name)
with open('centrality_data/%s.cent'%(org_name),'w') as file:
	file.write(str(org_name)+' ')
	centrality_list=list(dicshs)
	for x in centrality_list:
		file.write(str(x)+' ')
	file.write('\n')

	for node in G.nodes:
		file.write(node+' ')
		for x in centrality_list:
			if node not in dicshs[x]:
				file.write('-1 ')
			else:
				file.write(str(dicshs[x][node])+' ')
		file.write('\n')				

# with open('centrality_data/%s.csv' % (org_name),'w') as g:
# 	for nd in G.nodes():
# 		tbw=(nd+',')
# 		for name,value in dics.items():
# 			if nd not in value.keys():
# 				tbw+=('-1')+', '
# 			else:
# 				tbw+=(str(value[nd]))+', '
							
# 		if nd in ess:
# 			tbw+=("1")
# 		else:
# 			tbw+=("0")
# 		tbw+=("\n")
# 		g.write(tbw)