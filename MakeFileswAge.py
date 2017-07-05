
# coding: utf-8

# In[14]:

import os

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def make_yearfiles(path):
    years = {}
    f = open(path.replace("\\","\\\\"), 'r')
    lines = f.readlines(0)
    for line in lines:
        _id = line.split('\t')[0]
        _pub = line.split('\t')[1].replace('\n','')
        years[_id] = _pub
    f.close()
    
    f2 = open("F:\\13N_0403\\2015\\"+path.split("\\")[3].replace(".",'_N_n.'),'r')
    lines2 = f2.readlines()
    f_year = open("F:\\13N_year\\"+path.split("\\")[3].replace(".",'_year.'),'w')
    for line2 in lines2:
        citing = line2.split('\t')[0]
        cited = line2.split('\t')[1].replace('\n','')
        citing_y = years[citing]
        cited_y = years[cited]
        f_year.write(line2.replace('\n','')+"\t"+str(int(citing_y)-int(cited_y))+"\n")

    f2.close()
    f_year.close()


# In[ ]:

# Run the above function and store its results in a variable.   
full_file_paths = get_filepaths("F:\\13_year\\2015")
for path in full_file_paths:
    make_yearfiles(path)


# In[ ]:



