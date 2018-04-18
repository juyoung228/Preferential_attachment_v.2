
# coding: utf-8

# In[ ]:

'''
This .py is designed to run at Karst Server (linux)
'''


# In[1]:
import networkx as nx

def before_calculate(path):
    '''
    This function is for building before & after graph according to the 
    time group (1~10)
    '''
    year_categories = {}
    
    after = nx.DiGraph()
    before = nx.DiGraph()
    
    f = open(path,'r')
    lines = f.readlines(0)
    for line in lines:
        pairs = line.split('\t')[0]+'\t'+line.split('\t')[1]
        #print(pairs)
        year_categories[pairs] = None
       
    f_after = open("/gpfs/home/j/u/juyan/Karst/13N_0403/"+(path.split("/")[8]).split("_")[0]+"_2011_N_n.txt",'r')
    lines_after = f_after.readlines(0)
    for line_after in lines_after:
        if line_after.replace("\n","") in year_categories:
            after.add_edge(line_after.split('\t')[0], line_after.split('\t')[1])    
    f_after.close()
    
    f_before = open("/gpfs/home/j/u/juyan/Karst/13N_0403/"+(path.split("/")[8]).split("_")[0]+"_2010_N_n.txt",'r')    
    lines_before = f_before.readlines(0)
    for line_before in lines_before:
        if line_before.replace("\n","") in year_categories:
            before.add_edge(line_before.split('\t')[0], line_before.split('\t')[1])
    
    f_before.close()
    
    print ('before'+path+"\n"+nx.info(before))
    print ('after'+nx.info(after))
    calculate(path, before, after)
    return None

# In[ ]:

def calculate (path, before, after): 
    degrees_before = {}
    pairs = {}
    x = []
    y = []
    #complete 
    for i in before.nodes():
        if before.in_degree(i) not in degrees_before:
            degrees_before[before.in_degree(i)] = 1
        else: degrees_before[before.in_degree(i)] += 1
            
        if before.in_degree(i) not in pairs:
	    #print('***'+str(i))
            #+str(after.in_degree(i)))
            n_1 =(after.in_degree(i))-(before.in_degree(i))
            pairs[before.in_degree(i)] = n_1
        else:
	    #print(str(i)+str(after.in_degree(i)))
            n_2 = 0
	    if not bool(after.in_degree(i)):
		#print(str(i)+str(after.in_degree(i)))
                n_2 = 0
            else:
                #print(str(i)+str(after.in_degree(i)))
		n_2 = after.in_degree(i)-before.in_degree(i) 
            pairs[before.in_degree(i)] += n_2
    for n,An in pairs.items():
        x.append(n)
        y.append(An/float(degrees_before.get(n)))
        #print(n,l/degreeF.get(n))
    f = open('/gpfs/home/j/u/juyan/Karst/Done'+ (path.split(".")[0]).split("/")[-1]+path.split(".")[1]+".txt","w")
    f.write(str(x)+"\n"+str(y))
    f.close()
    after = nx.DiGraph()
    before = nx.DiGraph()
    return None

def get_filepaths(directory):
	import os
	file_paths = []
	for root, directories, files in os.walk(directory):
		for filename in files:
			filepath = os.path.join(root, filename)
			file_paths.append(filepath)
	return file_paths


paths = get_filepaths('./Sample')
for path in paths:
#	print(path.split(".")[1]+path.split(".")[2])
	print(path)
        before_calculate(path)

