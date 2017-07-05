
# coding: utf-8

# In[ ]:




# In[1]:


import sys
import networkx as nx
import os


# In[13]:

class nodedict:
	def __init__(self):
		self._set=set()
		self._index=len(self._set)
		self._dict={}
		self._inverse={}

	def getIdFromJ(self,J):
		
		if J not in self._set:
			jid = len(self._set)
			self._dict[J]= jid
			self._set.add(J)
			self._inverse[jid] = J
		return self._dict[J]

	def getJFromId(self,jid):
		return self._inverse[jid]

"""The personalized page rank"""
#	path: the path of network
#	personalized_weights_path: set None, if do not use ppr
# 	damping_parameter: alpha value in pr
# 	file_to_save: path to save result

def run_ppr(path,personalized_weights_path,damping_parameter,file_to_save,iterations=100):
	
	nd = nodedict()

	weighted_js=None

	if personalized_weights_path!=None:
		weighted_js={}
		content = open(personalized_weights_path).read().strip()
		lines = content.split("\n")
		for line in lines:
			splits = line.strip().split("\t")
			# print splits

			weighted_js[nd.getIdFromJ(splits[0].strip())] = float(splits[1].strip())

	# print "decis support syst", weighted_js['decis support syst']

	edgelist = []
	check=False
	for line in open(path):
		splits =line.strip().lower().split("\t")

		if len(splits)!=3:
			print ("line errors:",line.strip(),"in path:",path)
			continue

		
		for i in splits[:2]:
			if nd.getIdFromJ(i) not in weighted_js.keys():
				print (i)
				check=True
		
		edgelist.append((nd.getIdFromJ(splits[0]),nd.getIdFromJ(splits[1]),float(splits[2])))


	if check:
		print ("journal not in dict.")
		return
	else:
		print ("check passed,",path)

	#create Directed Graph
	DG=nx.DiGraph()
	DG.add_weighted_edges_from(edgelist)
	pr = nx.pagerank(DG,personalization=weighted_js,alpha=damping_parameter, max_iter=iterations)

	lines=[]
	for key in sorted(pr.keys()):
		lines.append(nd.getJFromId(key)+"\t"+str(pr[key]))

	open(file_to_save,"w").write("\n".join(lines))



# In[18]:

if __name__=="__main__":
	damping_parameters=[0.15,0.5,0.85]
	iterations = 100
	for file in os.listdir('C:\\Users\\Administrator\\Desktop\\PPR\\data\\'):
		path = 'C:\\Users\\Administrator\\Desktop\\PPR\\data\\'+file
		if not path.endswith(".txt"):
			continue
		for dp in damping_parameters:
			result_path = "C:\\Users\\Administrator\\Desktop\\PPR\\result\\"+str(file.split(".")[0])+"_"+str(dp).replace(".","_")+".txt"
			run_ppr(path,"C:\\Users\\Administrator\\Desktop\\weights.txt",dp,result_path,iterations)


# In[ ]:



