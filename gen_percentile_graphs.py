import functions as f

org_list = f.import_org_names()

for org in org_list:
	print(org)
	G,ess=f.import_data(org,1)
	f.grapher(org,f.calc_centralities(G,org,1),5,ess)
	print(org)
