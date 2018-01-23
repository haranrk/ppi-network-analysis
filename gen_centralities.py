#Calculates the centralities for all the organisms and stores it in centrality_data/org_name.cent
import functions as f

org_list = f.import_org_names()

for org_name in org_list:
	G,ess=f.import_data(org_name,1)
	dicshs=f.calc_centralities(G,org_name,1)
