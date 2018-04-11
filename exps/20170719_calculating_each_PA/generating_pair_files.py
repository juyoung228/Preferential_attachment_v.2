
# coding: utf-8


'''
This .py is designed to run at Karst Server (linux)
Becareful! it needs somewhat huge memory.
Avoid to run on window...

input: network_pair, network_pair_age
output: PA_per_age_year_domain
downloading_data: https://drive.google.com/drive/folders/1N6NFjpeBIp4lkoFMTHD_hZE0Pw3i4PSM?usp=sharing
'''

import networkx as nx

def before_calculate(path):
    '''
    This function is for building before & after graph 
    according to the time group (1~10)
    '''
    year_categories = {}
    
    after = nx.DiGraph()
    before = nx.DiGraph()
    
    # open files in 'network_pair_age' to ensure build a network 
    #which consists of only certain time group
    
    f = open(path,'r')
    lines = f.readlines(0)
    for line in lines:
        pairs = line.split('\t')[0]+'\t'+line.split('\t')[1]
        year_categories[pairs] = None
       
    f_after = open("./13N_0403/"+(path.split("/")[2]).split("_")[0]+"_2015_N_n.txt",'r')
    lines_after = f_after.readlines(0)
    for line_after in lines_after:
        if line_after.replace("\n","") in year_categories:
            after.add_edge(line_after.split('\t')[0], line_after.split('\t')[1])    
    f_after.close()
    
    f_before = open("./13N_0403/"+(path.split("/")[2]).split("_")[0]+"_2014_N_n.txt",'r')    
    lines_before = f_before.readlines(0)
    for line_before in lines_before:
        if line_before.replace("\n","") in year_categories:
            before.add_edge(line_before.split('\t')[0], line_before.split('\t')[1])
    
    f_before.close()
    
    print ('before'+path+"\n"+nx.info(before))
    print ('after'+nx.info(after))
    calculate(path, before, after)
    return None


def calculate (path, before, after): 
    '''
    The fuction calculates PA value by using before & after network
    '''
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
            n_1 = after.in_degree(i)-before.in_degree(i)
            pairs[before.in_degree(i)] = n_1
        else:
            n_1 = after.in_degree(i)-before.in_degree(i) 
            pairs[before.in_degree(i)] += n_1
    for n,An in pairs.items():
        x.append(n)
        y.append(An/float(degrees_before.get(n)))
        #print(n,l/degreeF.get(n))
    
    # example; ./Done/1_2015_yeartxt1.txt 
    f = open('./Done'+path.split(".")[1]+path.split(".")[2]+".txt","w")
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


#The diretory has 
paths = get_filepaths('./Use')
for path in paths:
#	print(path.split(".")[1]+path.split(".")[2])
	print(path)
        before_calculate(path)

