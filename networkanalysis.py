import networkx as nx
from collections import defaultdict
import random
import itertools
import networkx as nx
from collections import OrderedDict
import math
import numpy as np
import functions as f    
from optparse import OptionParser

usage="Usage: %prog -f <filename>"
parser = OptionParser(usage)
parser.add_option("-f", "--file", dest="org_name", help="Organism ID")
(options,args)=parser.parse_args()

if 'org_name' not in locals():
	G,ess_proteins = f.import_data()    
else:
	G,ess_proteins = f.import_data(org_name)

centrality_measures=f.calc_centralities(G)

for name, values in centrality_measures.items():
	ess_protein_measures = []
	non_ess_protein_measures = []
	
	for node, measure in values.items():
	    if node in ess_proteins:
	        ess_protein_measures.append(measure)
	        #print(measure)
	    else:
	        non_ess_protein_measures.append(measure)
	ess_protein_measures = np.array(ess_protein_measures)
	non_ess_protein_measures = np.array(non_ess_protein_measures)
	print(name)
	print("Ess:     %f %f \nNon_ess: %f %f \n" % (ess_protein_measures.mean(), ess_protein_measures.std(), non_ess_protein_measures.mean(), non_ess_protein_measures.std()))





#for i in degreenew.keys():
#i = ess_proteins[0]
#print(i,degreenew[i],closeness[i],betweenness[i],clust_coeff[i],eigenc[i],(cliq[i]/max(cliq.values())),(edge_clus_coeff[i]/max(edge_clus_coeff.values())),pg[i])


#def measuring_measures(centrality):
    
