import numpy as np 
import networkx as nx 
import random as rd 
from matplotlib import pyplot as plt 

def grapher(org,thresh):
	G=nx.Graph()
	s=''
	l=[]
	ess=[]

	with open (org+'e.txt') as f:
		while True:
			s=f.readline()
			if s=='':
				break
			ess.append(s.strip())


	with open(org+'.txt') as f:
		while True:
			s=f.readline()
			if s=='':
				break

			l=(s.strip().split(' '))

			if int(l[len(l)-1])>thresh:
				G.add_edge(l[0],l[1],weight=float(l[len(l)-1]))

	return (G,ess)

def randomise1(G):

	lst_nds=G.nodes()
	dum=lst_nds.copy()
	rd.shuffle(dum)
	map=dict(zip(lst_nds,dum))

	G_shuf=nx.Graph()

	for ed in G.edges():
		G_shuf.add_edge(map[ed[0]],map[ed[1]])

	return (G_shuf,dum)

def randomise2(G):

	lst_nds=G.nodes()
	dum=lst_nds.copy()
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





def zsco(dist1,dist2):
	x1=np.mean(np.array(dist1))
	x2=np.mean(np.array(dist2))
	ssig1=(np.std(np.array(dist1))/np.sqrt(len(dist1)))**2
	ssig2=(np.std(np.array(dist2))/np.sqrt(len(dist2)))**2
	return ((x1-x2)/(np.sqrt(np.abs(ssig1-ssig2))))

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




niter=1000
'''
G=nx.Graph()
ess=[]
G,ess=grapher('511145',700)
res=10 
'''
DEG=wdegree_centrality(grapher('243273',700)[0])
Gnodes=list(DEG.keys())

ess=[]
with open ('511145'+'e.txt') as f:
	while True:
		s=f.readline()
		if s=='':
			break
		ess.append(s.strip())

c,sig=0,[]
for nd in Gnodes:
	if nd in ess:
		c+=1
		sig.append(DEG[nd])

P=[]
print (c)

d=0
for i in range(niter):
	chig=[]
	sel=rd.sample(Gnodes,c)
	for nd in sel:
		chig.append(DEG[nd])

	P.append(zsco(sig,chig))

c=[i for i in P if i>2.33]
print (len(c))
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

