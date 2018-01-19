# Calculates the p values for all the centralities and stores it in p_val_data/org_name.pval
import numpy as np 
import networkx as nx 
import random as rd 
import functions as f

org_name=3702
# ess,dicshs,Gnodes=f.import_from_mat()
G,ess=f.import_data(org_name,0)
dicshs=f.calc_centralities(G,org_name)
trimmed_G=f.trim_graph(G)
niter=1000
p_vals_mean={}
p_vals_med={}
P={}

for name in dicshs.keys():
	p_vals_mean[name]=0
	p_vals_med[name]=0
	P[name]=[]

print("\nCalculating p values")
for name,dic in dicshs.items():
	#print(name)
	P=[]
	c,sig=0,[]
	#print('Lenght of dic: %d'%(len(dic.keys())))
	for node in G.nodes():
		if (node in ess) and (node in dic.keys()):
			c+=1
			sig.append(dic[node])
	#print(c)
	for i in range(niter):
		chig=[]
		if name in ("Information Centrality","Random Walk Betweenness Centrality","Communicability Betweenness"):
			sampled_nodes=rd.sample(trimmed_G.nodes(),c)
		else:
			sampled_nodes=rd.sample(G.nodes(),c)
		for node in sampled_nodes:
			chig.append(dic[node])
		P.append(f.compare(sig,chig))

	p_vals_mean[name]=len([i for i in P if i[0]>2.33])
	p_vals_med[name]=len([i for i in P if i[1]>2.33])

print("\np values:")
for name in p_vals_mean:
	print(name)
	print(f.printpv(p_vals_mean[name],niter))
	print(f.printpv(p_vals_med[name],niter))

with open('p_val_data/%s.pval'%(org_name),'w') as file:
	file.write('pvaltype ')
	centrality_list=list(dicshs)
	for x in centrality_list:
		file.write(str(x)+' ')
	file.write('\nmean ')
	
	for x in centrality_list:
		file.write(f.printpv(p_vals_mean[name],niter)+' ')
	file.write('\nmedian ')

	for x in centrality_list:
		file.write(f.printpv(p_vals_med[name],niter)+' ')

# get=f.percentilewise(dicshs,5,ess)
# for name,dic in get.items():
# 	print (name)
# 	print (get[name])

