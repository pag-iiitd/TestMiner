#combine all param_map notebook code to actual module
#As args for query and match takes names of feature extracted files; documentations from which param desc is extracted; 
#match signatures original
#Signature with argname needed only for position reference- datatype and arg names are obtained from feature list
#Need Description extraction+cleaning; ParamName ParamType and ParamFeature from file
#[(0.4911, 'desc_sim'), (0.3856, 'feat_sim'), (0.1234, 'par_sim'), (0.0, 'type_sim')]
"""Given doc- extract param descr. 
Load feature list files. Prepare list of tuples with pname, descr, type, feat. Two such lists- 
one each for query and match. For every query param pick all possible pairs compute 4 scores and pass to classifier.
Predict for the pair- if match '0' log its name and prob. if prob greater than previous. Return list of name_m to position_q pairs
like [[1,param_m1],[0,param_m2]] and write to mappings.txt- TODO: these indices should ignore 'self'
TODO: Cases to handle: 1) many params to one match. 2) No match
Note: processes only first sample test from query and match to draw mappings"""

from utility import *
from FeatureSim import *
import sys
from gensim.corpora import Dictionary
from gensim.models import Word2Vec, WordEmbeddingSimilarityIndex
from gensim.similarities import SoftCosineSimilarity, SparseTermSimilarityMatrix
import os
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

curr_dirpath=os.getcwd()
path_sep=os.path.sep
parent_path=curr_dirpath[:curr_dirpath[:-1].rfind(path_sep)]

model=KeyedVectors.load(parent_path+path_sep+'scripts'+path_sep+'match_framework_format'+path_sep+'w2v_crosslib_120k_oov.bin')
with open(parent_path+path_sep+'scripts'+path_sep+'match_framework_format'+path_sep+'combined3doclist_similaritymatrix.pkl', "rb") as myFile: # save grouping in a file to load later
    similarity_matrix=pickle.load(myFile)
with open(parent_path+path_sep+'scripts'+path_sep+'match_framework_format'+path_sep+'combined3doclist.pkl', "rb") as myFile: # save grouping in a file to load later
    docs_list=pickle.load(myFile)
dictionary = Dictionary(docs_list)	

match_feat_file='"'+sys.argv[1]+'"'
query_feat_file='"'+parent_path+path_sep+'query'+path_sep+'querytestp.txt"'
sig_q='"'+sys.argv[2]+'"' #of query
doc_q='"'+sys.argv[3]+'"' #of query
sig_m='"'+sys.argv[4]+'"' #of match
doc_m='"'+sys.argv[5]+'"' #of match
fmatch_score=eval(sys.argv[6])
#tree_model=pickle.load(open('crosslib_tree_param_classifier_v2.sav', 'rb'))#can change to v1 as per results
#sepfeat2- considers subfeatures as separate- gives value to descr and struct, sepfeat3: (0.5213, 'desc_sim'), (0.2896, 'feat_sim_struct'), (0.1448, 'par_sim'), (0.0443, 'type_sim')
tree_model=pickle.load(open('crosslib_tree_param_classifier_sepfeat3.sav', 'rb'))#can change to sepfeat2 (needs sep feat logic), v1 or v2 as per results


import networkx as nx

def prepareGraph():
	g = nx.Graph()
	#higher the weight less important (more abstract) it is. To compute score- use: 
	#LANG
	#numeric types
	g.add_weighted_edges_from([("Object", "Number",1.5), ("Number", "Integer",1), ("Integer", "java_int",0.5), ("Integer", "java_Integer",0.5),("Integer", "java_java.lang.Integer",0.5), ("Integer", "python_int",0.5), ("Number", "Float",1), ("Float", "java_float",0.5), ("Float", "java_Float",0.5),("Float", "java_java.lang.Float",0.5), ("Float", "python_float",0.5), ("Number","Long",1), ("Long","java_long",1), ("Long","java_Long",0.5),("Long","java_java.lang.Long",0.5), ("Long","python_int",0.5), ("Number","Byte",1), ("Byte","java_byte",0.5), ("Byte","java_Byte",0.5),("Byte","java_java.lang.Byte",0.5), ("Number","Short",1), ("Short","java_short",0.5), ("Short","java_Short",0.5),("Short","java_java.lang.Short",0.5), ("Short","python_int",0.5), ("Number","Double",1), ("Double","java_double",0.5), ("Double","python_float",0.5), ("Number","BigInteger",1), ("BigInteger","java_BigInteger",0.5),("BigInteger","java_java.math.BigInteger",0.5), ("BigInteger","python_int",0.5), ("Number","BigDecimal",1), ("BigDecimal","java_BigDecimal",0.5),("BigDecimal","java_java.math.BigDecimal",0.5), ("BigDecimal","python_decimal",0.5), ("Number","ComplexNumber",1), ("ComplexNumber","python_complex",0.5)])
	#string-related types
	g.add_weighted_edges_from([("Object","String",1.5), ("String","java_String",0.5),("String","java_java.lang.String",0.5), ("String","python_str",0.5), ("java_java.lang.CharSequence","java_String",0.5),("java_java.lang.CharSequence","java_java.lang.String",0.5), ("java_java.lang.Comparable<T>","java_String",0.5),("java_java.lang.Comparable<T>","java_java.lang.String",0.5), ("Object","StringBuffer",1.5), ("StringBuffer","java_StringBuffer",0.5),("StringBuffer","java_java.lang.StringBuffer",0.5), ("java_java.lang.CharSequence","java_StringBuffer",0.5),("java_java.lang.CharSequence","java_java.lang.StringBuffer",0.5), ("Object","StringBuilder",1.5), ("StringBuilder","java_StringBuilder",0.5),("StringBuilder","java_java.lang.StringBuilder",0.5), ("java_java.lang.CharSequence","java_StringBuffer",0.5),("java_java.lang.CharSequence","java_java.lang.StringBuffer",0.5) ])
	#misc
	g.add_weighted_edges_from([("Object","Character",1.5), ("Character","java_char",0.5), ("Character","java_Character",0.5),("Character","java_java.lang.Character",0.5), ("Character","python_chr()",0.5), ("java_java.lang.Comparable<T>","Character",1), ("Object","Boolean",1.5), ("Boolean","java_boolean",0.5), ("Boolean","java_Boolean",0.5),("Boolean","java_java.lang.Boolean",0.5), ("Boolean","python_bool",0.5), ("Object","Array",1.5), ("Array","java_String[]",0.5),("Array","java_java.lang.String[]",0.5), ("Array","java_char[]",0.5), ("Array","java_int[]",0.5), ("Array","java_double[]",0.5), ("Array","java_long[]",0.5), ("Array","java_float[]",0.5), ("Array","java_byte[]",0.5),("Array","java_Integer[]",0.5),("Array","java_java.lang.Integer[]",0.5), ("Array","java_Double[]",0.5),("Array","java_java.lang.Double[]",0.5), ("Array","java_Float[]",0.5),("Array","java_java.lang.Float[]",0.5), ("Array","java_Byte[]",0.5),("Array","java_java.lang.Byte[]",0.5), ("Array","python_list",0.5)])
	#UTIL
	#lists
	g.add_weighted_edges_from([("Object","AbstractCollection",1.5), ("java_java.util.Collection<E>","AbstractCollection",1), ("AbstractCollection","AbstractList",1), ("java_java.util.List<E>","AbstractList",1),("java_java.util.List<E>","python_list",0.5), ("AbstractList","ArrayList",1), ("ArrayList","java_ArrayList",0.5),("ArrayList","java_java.util.ArrayList",0.5), ("ArrayList","python_list",0.5), ("AbstractList","AbstractSequentialList",1), ("AbstractSequentialList","LinkedList",1), ("LinkedList","java_LinkedList",0.5),("LinkedList","java_java.util.LinkedList",0.5), ("AbstractList","Vector",1), ("Vector","Stack",1), ("Stack","java_Stack",0.5),("Stack","java_java.util.Stack",0.5), ("AbstractCollection","AbstractQueue",1), ("AbstractQueue","PriorityQueue",1), ("PriorityQueue","java_PriorityQueue",0.5), ("PriorityQueue","java_java.util.PriorityQueue",0.5)])
	#maps/sets
	g.add_weighted_edges_from([("Object", "AbstractMap",1.5), ("java_java.util.Map<K,V>","AbstractMap",1),("java_java.util.Map<K,V>","python_dict",0.5), ("AbstractMap","HashMap",1), ("HashMap","java_HashMap",0.5),("HashMap","java_java.util.HashMap",0.5), ("HashMap","python_dict",0.5), ("HashMap","LinkedHashMap",1), ("LinkedHashMap","java_LinkedHashMap",0.5),("LinkedHashMap","java_java.util.LinkedHashMap",0.5), ("AbstractCollection","AbstractSet",1), ("AbstractSet","HashSet",1), ("HashSet","java_HashSet",0.5),("HashSet","java_java.util.HashSet",0.5), ("HashSet","python_set",0.5) ])
	#misc
	g.add_weighted_edges_from([("Object","Date",1.5), ("Date","java_Date",0.5),("Date","java_java.util.Date",0.5), ("java_java.lang.Comparable<T>","java_Date",0.5),("java_java.lang.Comparable<T>","java_java.util.Date",0.5), ("Object","BitSet",1.5), ("BitSet","java_BitSet",0.5),("BitSet","java_java.util.BitSet",0.5) ])
	return g

g=prepareGraph()

#returns list of feature descr for each param
#mulitple indicates if more than one tests to consider- for query assumed only first test is used
#for multiple true the only change in structure is that for abstract structure a list of atmost size 3 
#is returned instead of a string element
def load_feat_list(fname,multiple=False):
	if fname.startswith("\""):
		fname=fname[1:len(fname)-1]
	with open(fname,'r',encoding='latin-1') as f:
		data=str(f.read()).strip()
	if(not data or data.strip()==""):
		sys.exit(0)
	data=data.replace('\\n','\\\\n')
	data=data.replace('\\r','\\\\r')
	

	data=eval(eval(data).decode('latin-1'))#replace('\\n','\n').replace('\\r','\r')
	if not multiple:
		data=data[0] #pick only the first set of param descriptions for processing
	else:#TODO: add mulitple structures
		data=testpicker(data)
	#print(type(data))
	f.close()
	"""with open("mapscore.txt", 'a+') as f:
		f.write(str(data))#exclude exp	"""
	
	return data

#inputs list of test cases features, assuming tests>2
#returns list of merged on len and chartype of atmost 3 tests for match that are not false/invalid- picks from start, middle and endswith
def testpicker(testsfeatlist):
	size=len(testsfeatlist)
	shortlist=list()
	if size==0:
		return list()
	if size==1:
		shortlist.append(testsfeatlist[0])
	elif size==2:
		shortlist.append(testsfeatlist[0])
		shortlist.append(testsfeatlist[1])
	else:
		#corner case: testsfeatlist of size 3- in this case returnNext may return invalid test if doesnt enter while loop
		#hence the checks
		t1,ind1=returnNext(testsfeatlist,0,int(size/2)-1)
		if "'false', 'EXP_" not in str(t1) and "'False', 'EXP_" not in str(t1):#ignore test cases wuth false output- as those are basically invalid inputs
			shortlist.append(t1)
		t2,ind2=returnNext(testsfeatlist,int(size/2),size-1)
		if "'false', 'EXP_" not in str(t2) and "'False', 'EXP_" not in str(t2):
			shortlist.append(t2)
		t3=testsfeatlist[-1]# to move in reverse if last test not valid hence moves to ind2+1
		if "'false', 'EXP_" not in str(t3) and "'False', 'EXP_" not in str(t3):
			shortlist.append(t3)
		else:
			if ind2+1<size:
				t3,ind3=returnNext(testsfeatlist,ind2+1,size)
				if "'false', 'EXP_" not in str(t3) and "'False', 'EXP_" not in str(t3):
					shortlist.append(t3)
	
	args_len=0#number of parameters; shortlist[0] is [val,argname,argtype,[type,[len,lentype],[abstype1..]]]
	y=shortlist[0]#to store test with max args
	for x in shortlist:
		if len(x)>args_len:#taking max as number of tests args may vary if coming from differesnt unittestmethods on same function
			args_len=len(x)
			y=x
			
	arg_names=list()
	
	for a in y:#traverse args in a test
		arg_names.append(a[1])
	
	"""
	extract arg names from shortlist with longest len.
	for each arg search in shortlist to append to finaltestfeat"""
	#further merging on shortlisted tests
	finaltestfeat=list()
	#args_len=len(shortlist[0])
	
	for arg in arg_names:
		"""with open("mapscore.txt", 'a+') as f:
			f.write(str(arg))#exclude exp	"""
		chartype='M'
		maxlen=-1
		len_feat=list()
		prev_chartype=None
		structs=[]
		val=''
		type=''
		noparamfeat=False#to capture if param features not supported- that is None
		if shortlist[0]:
			for i in range(len(shortlist[0])):
				if shortlist[0][i][1]==arg and shortlist[0][i][3]:
					chartype=shortlist[0][i][3][0]
					break
			
		for test in shortlist:
			for a in test:
				if a[1]==arg:
					val=a[0] #will pick latest to add to finaltest- doesn;t matter
					type=a[2] #will pick latest to add to finaltest-doesn't matter
					if a[3]:#param feature supported
						if a[3][1][0]>maxlen:#charlen
							maxlen=a[3][1][0]
							len_feat=a[3][1]
					
						if prev_chartype:
							if a[3][0]!=prev_chartype:
								chartype='M'
								prev_chartype=a[3][0]
						else:
							prev_chartype=a[3][0]
						structs.append(a[3][2])
						
						break
					else:
						noparamfeat=True
						break
			if noparamfeat:
				break
		if noparamfeat:
			finaltestfeat.append([val,str(arg),type,None])		
		else:
			#first 3 elements don't matter
			"""with open("mapscore.txt", 'a+') as f:
				f.write("--"+str(arg))#exclude exp	"""
			finaltestfeat.append([val,str(arg),type,[chartype,len_feat,structs]])		
		
	"""for i in range(args_len):#traverse each par- TODO: arg-order may be different in same file. preprocessing needed- maybe alphabetically
		maxlen=0
		len_feat=list()
		prev_chartype=None
		if shortlist[0][i][3]:#if type not supported in param feature then can be None
			chartype=shortlist[0][i][3][0]
		else:
			finaltestfeat.append([shortlist[0][i][0],shortlist[0][i][1],shortlist[0][i][2],None])
			continue
		structs=[]
		for test in shortlist:#traverse test's particular param
			if i>=len(test):
				continue
			#possible that some
			if test[i][3]:#param feat not None type
				if test[i][3][1][0]>maxlen:#charlen
					maxlen=test[i][3][1][0]
					len_feat=test[i][3][1]
				if prev_chartype:
					if test[i][3][0]!=prev_chartype:
						chartype='M'#mixed
						prev_chartype=test[i][3][0]
				else:
					prev_chartype=test[i][3][0]
				structs.append(test[i][3][2])#list of structs
		#first 3 elements don't matter
		finaltestfeat.append([shortlist[0][i][0],shortlist[0][i][1],shortlist[0][i][2],[chartype,len_feat,structs]])"""
	"""with open("mapscore.txt", 'a+') as f:
		f.write("shortlist: "+str(shortlist)+"::"+str(finaltestfeat)+"\n")#exclude exp"""
	return finaltestfeat
	
#returns appropriate (nonfalse) test and its index in given range of indices in testsfeatlist- upperlimit not inclusive
def returnNext(testsfeatlist,lowerlimit,upperlimit):
	t=testsfeatlist[lowerlimit]
	ctr=lowerlimit
	while(ctr<upperlimit):
		t=testsfeatlist[ctr]
		if "'false', 'EXP_" in str(t) or "'False', 'EXP_" in str(t):
			ctr=ctr+1
		else:
			break
	
	return (t,ctr)
	
#add param description to feature list. fname is filepath whose feature list to load
#ismatch is a boolean which is true if processing is on match and not query- needed for load_feat_list for multiple tests
def merge_param_details(docstring,sig,fname,ismatch=False):
	param_doc_dict=get_param_docs_dict(docstring, sig) #returns dictionary of param name to its description
	#print(docstring,sig,param_doc_dict)
	
	data_list=load_feat_list(fname,ismatch)
	merge_list=list()
	"""with open("mapscore.txt", 'a+') as f:
		f.write(docstring+"==="+str(param_doc_dict))"""
	for ele in data_list: #iter param details
		flag=False
		for par in param_doc_dict:
			if ele[1]==par:
				el_new=ele
				el_new.append(param_doc_dict[par])
				merge_list.append(el_new)
				flag=True
		if not flag and ele[1]!='self': #for params whose description not there
			el_new=ele
			el_new.append("")
			merge_list.append(el_new)
	
	return merge_list	

def calculate_name_sim(p1, p2):
	'''for calculating name similarity'''
	p1=lemmatize_doc(drop_stop_words(' '.join(' '.join(camel_case_split2(p1)).lower().split('_'))))
	p2=lemmatize_doc(drop_stop_words(' '.join(' '.join(camel_case_split2(p2)).lower().split('_'))))
	
	try:
		score=similarity_matrix.inner_product(dictionary.doc2bow(p1.split()), dictionary.doc2bow(p2.split()), normalized=True)
		"""with open("mapscore.txt", 'a+') as f:
			f.write('\n'+str(p1)+"=="+str(p2)+"=="+str(score)+'\n')"""
		return score
	except:
		"""with open("mapscore.txt", 'a+') as f:
			f.write('\n'+str(p1)+"=="+str(p2)+'\n')"""
		'''if word not in vocabulary'''
		return 0 	
	
def get_desc_sim(pdesc1,pdesc2):
	try:
		pdesc1=get_cleaned_doc(pdesc1)
		pdesc2=get_cleaned_doc(pdesc2)
		score=similarity_matrix.inner_product(dictionary.doc2bow(pdesc1.split()), dictionary.doc2bow(pdesc2.split()), normalized=True)
		return score
	except:# when desc empty
		return 0 


#takes two data types
def get_type_sim(src, dest):
    if src==dest:
        return 1
    else:
        try:
            dist,path=nx.single_source_dijkstra(g,src,dest)
            sim=1.0/(1.0+0.4*dist) #into 0.5 is just for scaling
            return sim
        except:
            return 0	

#returns a list with 4 scores between the two params
#featlist: [value,argname,argtype,features,descr]
#score order: 'par_sim','type_sim','desc_sim','feat_simchartyp','feat_simlentype','feat_sim_struct'
def getscores(featlist1,featlist2):
	p_sim=calculate_name_sim(featlist1[1],featlist2[1])
	t_sim=get_type_sim(featlist1[2],featlist2[2])
	desc_sim=get_desc_sim(featlist1[4],featlist2[4])
	if featlist1[3] and featlist2[3]:
		if isinstance(featlist2[3][2],list):#absstruct component is a list
			#segregate each of featlist2[3][2] to convert to regular featlist type and get scores with featlist1[3] 
			#and pick feat_sim with max val on feat_sim[2]to return
			structscores=list()
			for struct in featlist2[3][2]:
				modified_featlist=[featlist2[3][0],featlist2[3][1],struct]
				featobj=FeatureSimilarity(featlist1[3],modified_featlist)
				feat_sim=featobj.getsimilarity_sep()#feat_sim[0] and [1] would be same but had to call on all to handle non-string types
				structscores.append(feat_sim[2])
			return [p_sim,t_sim,desc_sim,feat_sim[0],feat_sim[1],max(structscores)]# or could choose between max or average
		else:
			featobj=FeatureSimilarity(featlist1[3],featlist2[3])
			#feat_sim=featobj.getsimilarity()
			#return [p_sim,t_sim,desc_sim,feat_sim]
			feat_sim=featobj.getsimilarity_sep()
			return [p_sim,t_sim,desc_sim,feat_sim[0],feat_sim[1],feat_sim[2]]
	else:
		return [p_sim,t_sim,desc_sim,0,0,0]
		
#returns (param_q,param_m) match pairs
def pickbestpairs():
	paramsfeat_q=merge_param_details(doc_q,sig_q,query_feat_file)
	paramsfeat_m=merge_param_details(doc_m,sig_m,match_feat_file,True)
	pairs=list()# contain list of pair-list
	combined_param_score=0 #for later refining of match of function
	score_triplet=[]
	pair_wtd_score=[]
	for parfeat in paramsfeat_q:
		matchwith= None
		matchprob=0
		match_wtdscore=0
		match_scores=[0,0,0,0,0,0]
		for parfeatm in paramsfeat_m:
			scores=getscores(parfeat,parfeatm)
			(label,prob,wtd_score)=classifier_prediction(scores)
			with open("mapscore.txt", 'a+') as f:
				f.write(parfeat[1]+"--"+parfeatm[1]+"--"+str(scores)+str(wtd_score))
			#print("Checking:",parfeat[1],parfeatm[1])
			if parfeatm[1].startswith('EXP_') and parfeat[1].startswith('EXP_'):
				matchwith=parfeatm[1]
				matchprob=1
				matchwith='EXP_op'
				match_scores=scores
			elif not parfeatm[1].startswith('EXP_') and not parfeat[1].startswith('EXP_') and label.item(0)==0 and prob>=matchprob and wtd_score>match_wtdscore and max(scores)>0.5 and (wtd_score>0.49 or scores[-1]>0.64 or (scores[-1]>=0.62 and fmatch_score>0.65)):#pick best prediction
				matchwith=parfeatm[1]#parname
				matchprob=prob
				match_wtdscore=wtd_score
				match_scores=scores
		if matchwith!='EXP_op':
			score_triplet.append(match_scores)	
			combined_param_score=combined_param_score+match_wtdscore
		pairs.append([parfeat[1],matchwith])
		pair_wtd_score.append(match_wtdscore)#final weighted param score
		#print(parfeat[1],matchwith,label,prob,match_wtdscore)
		
		#if matchwith==None indicates no match found- likely if more args in query- assumes that of there is a match then it would be found
		#IMP: for such cases default value from template to be used during test generation
	
	pairs=refinePairs(pairs,pair_wtd_score) #discard many to one mappings by picking candidate with best wtdscore on paramfeats
	
	#return None to discard function matches whose none of param strcuture score exceed 0.6
	flag=False#False indicates none param struct score exceeds 0.6
	for score in score_triplet:
		if score[-1]>=0.65 or (score[-1]>=0.62 and fmatch_score>0.65): #last arg is structure score
			flag=True
			break
	
	"""with open("mapscore.txt", 'a+') as f:
		f.write(sig_m+"---"+str(paramsfeat_q)+"\n"+str(paramsfeat_m)+"\n"+str(pairs)+str(pair_wtd_score)+"::"+str(score_triplet)+'::'+str(combined_param_score/(len(paramsfeat_q)-1))+"\n*****\n")#exclude exp
	"""
	if not flag:
		return None
	
	
	return pairs

#inputs list of q_par,m_par pairs and corresponding list of parfeat wtd score and discards cases of many to one pair mappings
#by picking candidate with best wtdscore on paramfeats	
def refinePairs(pairs,pair_wtd_score):	
	m_arg_ind_mapping=dict() #maintains mapping of matching arg with indices in pair where it appears
	#leftover_q_args=list() # ones where pair already mapns to None
	for i in range(len(pairs)):
		if pairs[i][1] in m_arg_ind_mapping: #matching arg
			m_arg_ind_mapping[pairs[i][1]].append(i)
		else:
			if pairs[i][1]:
				m_arg_ind_mapping[pairs[i][1]]=[i]
		
	with open("mapscore.txt", 'a+') as f:
		f.write(str(m_arg_ind_mapping)+"\n*****\n")#exclude exp

	marg_bestind=dict()
	for arg in m_arg_ind_mapping:
		max_score=0
		max_score_ind=-1
		for score_ind in m_arg_ind_mapping[arg]:
			if pair_wtd_score[score_ind]>=max_score:
				max_score=pair_wtd_score[score_ind]
				max_score_ind=score_ind
		marg_bestind[arg]=max_score_ind # assgigns only one best pair from pairs that has arg as match candidate
	refinedpairs=list()
	for k in range(len(pairs)):
		if pairs[k][1] and marg_bestind[pairs[k][1]]==k:#found the best mapping at index k
			refinedpairs.append([pairs[k][0],pairs[k][1]])
		else:
			refinedpairs.append([pairs[k][0],None])
	#for arg in leftover_q_args:
	#	refinedpairs.append([arg,None])
	return refinedpairs
	
"""for param matches- return list of [q_pos,match_name] indicating
which param from 'match' to map to which index of 'query' param"""
def prepare_index_map_list():
	pairs=pickbestpairs()#returns list of (param_q,param_m)
	if not pairs:#function match discarded on strcutural disimilarity
		print("")
		return list()
	q_params=get_params(sig_q) #returns list of param names
	pairs_new=list()
	for p in pairs:
		if(not p[0].startswith('EXP_')):
			if not p[1]: # p[1] may be None if no match found- pick default then with some indication ## prefixed and suffixed
				indx=q_params.index(p[0])
				"""load qfeatlist and pick value(0th position) of p[0] arg name (1th position)"""
				qft=load_feat_list(query_feat_file)#returns features of first test case- for the query
				defval=""
				for ele in qft: #iter param details
					if ele[1]==p[0]:#found query param not having match param
						defval=ele[0]
				if isinstance(defval,str):#to avoid issue at later eval
					defval="\""+defval.replace("\"","\\\"")+"\""
				pairs_new.append([indx,"##"+str(defval)+"##"])#rplace p[1] by default val at index of p[0] and eval later to type
			else:
				pairs_new.append([q_params.index(p[0]),p[1]])
	print(pairs_new)
	return pairs_new
	
	
	
def classifier_prediction(scorelist):
	label=tree_model.predict([scorelist])
	ft_wt=tree_model.feature_importances_
	wtd_score=0
	tot_wt=0# to capture actual non-zero score wts
	for i in range(len(scorelist)):
		wtd_score=wtd_score+ft_wt.item(i)*scorelist[i]
		if scorelist[i]!=0: 
			tot_wt=tot_wt+ft_wt.item(i)
		if scorelist[i]==0 and i<=2:#wt. ignore condition relaxed only on features so i<=1 as support mainly for string so should not penalize other types, also descr score 0 indicates description of other param missing so not counted
			tot_wt=tot_wt+ft_wt.item(i)
		if scorelist[i]==0 and i==2:
			wtd_score=wtd_score+0.5*ft_wt.item(i)*scorelist[0]+0.5*ft_wt.item(i)*scorelist[1] #distribute weight of desc among pname and ptype if no desc
		if scorelist[i]==0 and i==5:#for non-string typesthe abs is 0 so length category is given its weight
			wtd_score=wtd_score+ft_wt.item(i)*scorelist[4] #distribute weight of abs to length type
			tot_wt=tot_wt+ft_wt.item(i)
	
	#print(scorelist,tree_model.predict_proba([scorelist]))
	label_prob=tree_model.predict_proba([scorelist]).item(label.item(0))
	"""with open("mapscore.txt", 'a+') as f:
		f.write(str(label)+"+++"+str(ft_wt)+'::::'+str(scorelist)+"+++"+str(wtd_score)+"=-=-"+str(wtd_score/tot_wt))#exclude exp
	"""
	
	if tot_wt==0:
		tot_wt=1
	return (label,label_prob,wtd_score/tot_wt)
	
#function call
prepare_index_map_list()