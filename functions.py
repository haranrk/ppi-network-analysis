import networkx as nx
import numpy as np
from collections import Counter
import functions as f
import scipy.io as spio
import os.path

def import_data(org_name=243273,string_version=0):
    G=nx.Graph()
    string_location,edge_weight_column=string_version_data(string_version)
    print(edge_weight_column)
    datafile=open("string_data/%s/%s.ppi" % (string_location,org_name))
    print("Importing PPI data")
    
    for line in datafile:
        g=line.split(" ")
        if(int(g[edge_weight_column])>700):
            G.add_edges_from([(g[0],g[1])],weight=int(g[edge_weight_column]))
            #print('%s %s with %s' % (g[0],g[1],g[15]))

    ess_file = open('string_data/%s/%s.ess' % (string_location,org_name))
    ess_proteins = []
    for line in ess_file:
        ess_proteins.append(line.strip()) 
        #print(ess_proteins[-1])

    return G,ess_proteins

#imports node data, centralities from Raman's mat file
def import_from_mat(org_name=243273):
    mat = spio.loadmat('all_net_data.mat',squeeze_me=True)
    centrality_measures={}
    org_id=9    
    cc=list(mat['cc'][9])
    bwcent=list(mat['bwcent'][9])
    degree=list(mat['degree'][9])
    listofnodes=list(mat['nodeList'][org_id])
    centrality_measures['Betweenness Centrality']=dict(zip(listofnodes,bwcent))
    centrality_measures['Degree Centrality']=dict(zip(listofnodes,degree))
    centrality_measures['Closeness Centrality']=dict(zip(listofnodes,cc))
    ess=[listofnodes[x] for x in range(len(listofnodes)) if mat['isEss'][9][x]==1]
    # G = nx.Graph()

    return ess,centrality_measures,listofnodes


def compare(dist1,dist2):
    ret=[]
    if np.mean(dist1)<np.mean(dist2):
        ret.append(3)
    else:
        ret.append(1)

    if np.median(dist1)<np.median(dist2):
        ret.append(3)
    else:
        ret.append(1)
    return ret

def printpv(n,niter):
    if n==0:
        return '<1x10^-'+str(int(np.log10(niter)))
    else:
        return str(n/niter)


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

def zsco(dist1,dist2):
    x1=np.mean(np.array(dist1))
    x2=np.mean(np.array(dist2))
    ssig1=(np.std(np.array(dist1))/np.sqrt(len(dist1)))**2
    ssig2=(np.std(np.array(dist2))/np.sqrt(len(dist2)))**2
    return [((x1-x2)/(np.sqrt(np.abs(ssig1-ssig2))))]

def percentilewise(dicshs,res,ess):
    rret={}
 
    for name,dic in dicshs.items():
        ret={}
        for x in range(res,100,res):
            n=0
            for nd in dicshs[name].keys():
                if dicshs[name][nd]>np.percentile(list(dicshs[name].values()),x):
                    if nd in ess:
                        n+=1
            ret[x]=n,(len(ess))
        rret[name]=ret
        print (name,ret[95])
    return (rret)

def log_output(output,filename):
    with open('output_logs/%s.log' % (filename), 'w') as file:
        file.write(output)

def string_version_data(string_version):
    if string_version==1:
        string_location='new_string'
        edge_weight_column=15
    elif string_version==0:
        string_location='old_string'
        edge_weight_column=2
    else:
        print("Not available")
    return string_location,edge_weight_column

def calc_centralities(G,org_name,string_version):
    print("Calculating centralities")
    centrality_measures = {}
    string_location=f.string_version_data(string_version)[0]
    print(string_location)
    # if 1==0:
    if os.path.isfile('centrality_data/%s/%s.cent'%(string_location,org_name)):
        print("Using cached centrality data")
        file=open('centrality_data/%s/%s.cent'%(string_location,org_name))
        lines=file.readlines()
        centrality_list=lines.pop(0).strip().split(' ')
        centrality_list.pop(0)
        
        for i,centrality in enumerate(centrality_list):
            # print("%d. %s" % (i+1,centrality))
            centrality_measures[centrality]={}

        for line in lines:
            value_list=line.split(' ')
            for i,centrality in enumerate(centrality_list):
                centrality_measures[centrality][value_list[0]]=float(value_list[i+1])
    else:
        
        print("1. Degree centrality")
        centrality_measures['Degree_Centrality']=nx.degree_centrality(G)
        
        print("2. Closeness centrality")
        centrality_measures['Closeness_Centrality']=Counter(nx.algorithms.centrality.closeness_centrality(G))
        
        print("3. Betweenness centrality")
        centrality_measures['Betweenness_Centrality']=Counter(nx.algorithms.centrality.betweenness_centrality(G))
        
        print("4. Clustering coefficient")
        centrality_measures['Clustering_Co-efficient']=Counter(nx.clustering(G))
        
        print("5. Eigenvector centrality")
        centrality_measures['Eigenvector_Centrality']= nx.eigenvector_centrality(G)
        
        print("6. Subgraph centrality")
        centrality_measures["Subgraph_Centrality"]=nx.subgraph_centrality(G)
        
        print("7. Information centrality")
        centrality_measures["Information_Centrality"]=nx.current_flow_closeness_centrality(f.trim_graph(G))
        
        print("8. Clique Number")
        cliq={}
        for i in G.nodes():
           cliq[i]=nx.node_clique_number(G,i)
        centrality_measures["Clique_Number"]=cliq
        
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
    
        centrality_measures['Edge_Clustering_Coefficient']=edge_clus_coeff
        
        print("10. Page Rank")
        centrality_measures['Page_Rank']=nx.pagerank(G)
        
        print("11. Random Walk Betweenness Centrality")
        centrality_measures["Random_Walk_Betweenness_Centrality"]=nx.current_flow_betweenness_centrality(f.trim_graph(G))
        
        print("12. Load Centrality")
        centrality_measures["Load_Centrality"]=nx.load_centrality(G)
        
        print("13. Communicability Betweenness")
       # centrality_measures["Communicability_Betweenness"]=nx.communicability_betweenness_centrality(f.trim_graph(G))
        
        print("14. Harmonic Centrality")
        centrality_measures["Harmonic_Centrality"]=nx.harmonic_centrality(G)
            
        print("15. Reaching Centrality")
        reach_cent={}
        for node in G.nodes:
            reach_cent[node] = nx.local_reaching_centrality(G,node)
        centrality_measures["Reaching_Centrality"]=reach_cent
        
        print("16. Katz Centrality(not calculated)")
    #   centrality_measures["Katz_Centrality"]=nx.katz_centrality(G)
    
        datafile=open("refex_props/%s.refex" % (org_name))
        for x in range(1,94):
            print("%d. Refex#%d" % (x+16,x))
            centrality_measures["refex#%d" % (x)]={}
        for line in datafile:
            props=line.strip().split(" ")
            props=[i.strip('\t') for i in props]
            #print(props)
            for x in range(1,93):
                centrality_measures["refex#%d" % (x)][props[0]]=float(props[x+1])
    
        datafile=open("refex_rider_props/%s.riderproperties" % (org_name))
        for x in range(1,11):
            print("%d. Refex Rider#%d" % (x+16+93,x))
            centrality_measures["refex_rider#%d" % (x)]={}
        for line in datafile:
            props=line.strip().split(" ")
            props=[i.strip('\t') for i in props]
            #print(props)
            for x in range(1,len(props)-1):
                centrality_measures["refex_rider#%d" % (x)][props[0]]=float(props[x+1])
        
     
        with open('centrality_data/%s/%s.cent'%(string_location,org_name),'w') as file:
            file.write(str(org_name)+' ')
            centrality_list=list(centrality_measures)
            for x in centrality_list:
                file.write(str(x)+' ')

            for node in G.nodes:
                file.write('\n'+node+' ')
                for x in centrality_list:
                    if node not in centrality_measures[x]:
                        file.write('-1 ')
                    else:
                        file.write(str(centrality_measures[x][node])+' ')
    return centrality_measures

# ess1,dicshs1,Gnodes=f.import_from_mat()
# G,ess2=f.import_data(158879)
# dicshs2=calc_centralities(G,158879)
# for name,val in dicshs1.items():
#     print(name)
#     print(len(dicshs2[name].keys()))
#     print(len(dicshs1[name].keys()))
#     c=0
#     for x in dicshs1[name]:
        
#         if x in dicshs2[name].keys():
#             c+=1
#             print('%f %f %f %d' % (dicshs1[name][x],dicshs2[name][x],dicshs1[name][x]/dicshs2[name][x],c))
