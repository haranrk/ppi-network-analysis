import numpy as np 
import networkx as nx 
import random as rd 
from matplotlib import pyplot as plt 
import functions as f

def randomise1(G):

	lst_nds=G.nodes()
	dum=list(lst_nds).copy()
	rd.shuffle(dum)
	map=dict(zip(lst_nds,dum))

	G_shuf=nx.Graph()

	for ed in G.edges():
		G_shuf.add_edge(map[ed[0]],map[ed[1]])

	return (G_shuf)

def randomise2(G):

	lst_nds=G.nodes()
	dum=list(lst_nds).copy()
	rd.shuffle(dum)

	map=dict(zip([x for x in range(len(G.nodes()))],dum))
	G_dum=nx.configuration_model([G.degree(nd) for nd in G.nodes()])
	G_ret=nx.Graph()

	for ed in G_dum.edges():
		G_ret.add_edge(map[ed[0]],map[ed[1]])

	G_ret=nx.Graph(G_ret)
	G_ret.remove_edges_from(G_ret.selfloop_edges())

	return (G_ret)

def inter(nds,ess):
	c=0
	for nd in nds:
		if nd in ess:
			c+=1
	return (c)

def wdegree_centrality(G):
	w_d={} 

	for nd in G.nodes():
		w_d[nd]=0
		for ngh in G.neighbors(nd):
			w_d[nd]+=G.edge[nd][ngh]['weight']

	lst1=list(w_d.values())
	m=(np.max(lst1))

	lst2=list(lst1/m)
	
	return dict(zip(w_d.keys(),lst2))

def jack_f(G,c):# c - % of nodes to be removed
	G_ret=nx.Graph()
	G_ret=G
	G_ret.remove(rd.sample(G.nodes(),int(len(G.nodes())*c/100)))
	return (G_ret)

def compare(dist1,dist2):
	if np.mean(dist1)>np.mean(dist2):
		return 3
	else:
		return 1


def dict_file(org,thresh,n):
	ret={}
	with open('TRAINING_'+str(org)+'_'+str(thresh)+'.txt') as f:
		s=''
		while True:
			s=f.readline()
			if s=='':
				break
			ret[s.strip().split(' ')[0]]=float(s.strip().split(' ')[n])

	return ret

def p_vals(dicshs,case=1,niter=100):
	print("Calculating P vals with method #%d" % (case))
	ret={}
	P={}
	for name in dicshs:
		ret[name]=[]
		P[name]=[]
	if case==1:
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
					P.append(zsco(sig,chig))

				ret[name].append(len([i for i in P if i>2.33]))
		

	if case==2:
		for i in range(niter):
			rdicshs=f.calc_centralities(randomise1(G))
			for name in dicshs:
				sig,chig=[],[]
				for nd in G.nodes():
					if nd in ess:
						sig.append(dicshs[name][nd])
						chig.append(rdicshs[name][nd])
				P[name].append(zsco(sig,chig))
				print(P)
		for name in dicshs:
			ret[name].append(len([i for i in P[name] if i>2.33]))

	if case==3:
		for i in range(niter):
			rdicshs=f.calc_centralities(randomise2(G))
			for name in dicshs:
				sig,chig=[],[]
				for nd in G.nodes():
					if nd in ess:
						sig.append(dicshs[name][nd])
						chig.append(rdicshs[name][nd])
				P[name].append(zsco(sig,chig))
				print(P)
		for name in dicshs:
			ret[name].append(len([i for i in P[name] if np.abs(i)>2.33]))
	
	if case==4:
		for i in range(niter):
			rdicshs=f.calc_centralities(jack_f(G,20))
			for name in dicshs:
				sig,chig=[],[]
				for nd in G.nodes():
					if nd in ess:
						sig.append(dicshs[name][nd])
						chig.append(rdicshs[name][nd])
				P[name].append(zsco(sig,chig))
				print(P)
		for name in dicshs:
			ret[name].append(len([i for i in P[name] if np.abs(i)>2.33]))

	for name,value in ret.items():
	 		ret[name]=np.mean(value)/niter
	return ret





G,ess=f.import_data()
dicshs=f.calc_centralities(G)
p_vals=p_vals(dicshs,4)
for name,p_val in p_vals.items():
	print(name)
	print(p_val)
	#print(len(p_val))
# niter=1000
# '''
# G=nx.Graph()
# ess=[]
# G,ess=grapher('511145',700)
# res=10 
# '''
# G,ess=f.import_data()
# DEG=wdegree_centrality(G)
# Gnodes=list(DEG.keys())

# # ess=[]
# # with open ('511145'+'e.txt') as f:
# # 	while True:
# # 		s=f.readline()
# # 		if s=='':
# # 			break
# # 		ess.append(s.strip())

# c,sig=0,[]
# for nd in Gnodes:
# 	if nd in ess:
# 		c+=1
# 		sig.append(DEG[nd])

# P=[]
# print (c)

# d=0
# for i in range(niter):
# 	chig=[]
# 	sel=rd.sample(Gnodes,c)
# 	for nd in sel:
# 		chig.append(DEG[nd])

# 	P.append(zsco(sig,chig))

# c=[i for i in P if i>2.33]
# print (len(c))
'''
c,d=[0,0],[0,0]
gsl=[]
gssl=[]
for nd in G.nodes():
	if DEG[nd]>np.percentile(np.array(list(DEG.values())),90):
		c[0]+=1
		if nd in ess:
			c[1]+=1
			gsl.append(nd)
for nd in G.nodes():
	if sDEG[nd]>np.percentile(np.array(list(sDEG.values())),90):
		d[0]+=1
		if nd in ess:
			d[1]+=1
			gssl.append(nd)
print (c[0],c[1],d[1])
print (set(gsl).intersection(gssl))
'''

