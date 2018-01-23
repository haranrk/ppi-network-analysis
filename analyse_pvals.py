import functions as f
import os.path

org_list = f.import_org_names()
pvals={}
for x in org_list:
	if os.path.isfile('p_val_data/new_string/%s.pval'%(x)):
		pvals[x]={}
		pvals[x]=f.import_pvals(x)

significant_features={}
for org_name, pval in pvals.items():
	print("Number of significant features in %s" %(org_name))
	significant_features[org_name]=[]
	for centrality,val in pval.items():
		if val[1]=='<1x10^-6' or val[1]=='<1x10^-3' :
			# print(centrality)
			significant_features[org_name].append(centrality)
	print(len(significant_features[org_name]))		

sig_acc_org=significant_features['158879']

for n,v in significant_features.items():
	sig_acc_org=set(sig_acc_org).intersection(significant_features[n])

print("Common significant features across all organsims")
print (len(sig_acc_org))