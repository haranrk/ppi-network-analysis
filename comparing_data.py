import functions as f

ess1,dicshs1,Gnodes=f.import_from_mat()
G,ess2=f.import_data(158879,0)
dicshs2=f.calc_centralities(G,158879)
output=''
for name,val in dicshs1.items():
    output+=('%s\n'%(name))
    output+=('%s\n'%(len(dicshs2[name].keys())))
    output+=('%s\n'%(len(dicshs1[name].keys())))
    c=0
    output+=('%s\t\t%s\t\t%s\t\t%s\n'%('old string','new string','old/new','i'))
    for x in dicshs1[name]:
        if x in dicshs2[name].keys():
            c+=1
            output+=('%f\t\t%f\t\t%f\t\t%d\n' % (dicshs1[name][x],dicshs2[name][x],dicshs1[name][x]/dicshs2[name][x],c))
print(output)            
f.log_output(output,"comparing_cent_data")
