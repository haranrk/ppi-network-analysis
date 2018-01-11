import numpy as np 
import networkx as nx 
import random as rd 
import functions as f

G,ess=f.import_data()
dicshs=f.calc_centralities(G)
niter=1000
p_vals={}
P={}

for name in dicshs:
	print(name)
	p_vals[name]=[]
	P[name]=[]

	for name,dic in dicshs.items():
		print(name)
		P=[]
		c,sig=0,[]
		for nd in G.nodes():
			if nd in ess:
				c+=1
				sig.append(dic[nd])
		for i in range(niter):
			P=[]
			chig=[]
			sel=rd.sample(G.nodes,c)
			for nd in sel:
				chig.append(dic[nd])
				P.append(f.zsco(sig,chig))
			p_vals[name].append(len([i for i in P if i>2.33]))

for name,value in p_vals.items():
	 	p_vals[name]=np.mean(value)/niter

for name,p_val in p_vals.items():
	print(name)
	print(p_val)
