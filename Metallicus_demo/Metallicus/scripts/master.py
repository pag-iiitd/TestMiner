#chdir to match framework, execute matchframework, load fid_info pickle, chdir to parsetests
#iterate and pass args to parseTests: two arguments: language name_of_querytest_template
import os
import sys
import pickle
import sqlite3
import timeit
from sys import platform
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

#assume current path is up to the point where master.py is- in scripts folder
current_path=os.getcwd()
path_sep=os.path.sep
parent_path=current_path[:current_path[:-1].rfind(path_sep)]
#execute: python master.py python test_temp.py
def sql_connection():
	try: 
		con = sqlite3.connect(current_path+path_sep+'match_framework_format'+path_sep+'crosslib_final_full_v2.db')
		#print('Connected to db')
		return con
	except Error:
		print(Error)

def sql_fetch(con,selectquery,paramtoquery):
	cursorObj = con.cursor()
	cursorObj.execute(selectquery,paramtoquery)
	#print('query run...')
	rows = cursorObj.fetchall() #returned as list of tuple of attributes
	#for row in rows:
	#	print(row)
	return rows

queryParser_path=parent_path+path_sep+'query'# path to one dir up and to query folder
start = timeit.default_timer()
with open(queryParser_path+path_sep+'querydoc.txt','r',encoding='latin-1') as f:
	data=str(f.read()).strip()
ind=data.find('\n')	
q=data[ind+1:]
query='"'+q.replace("\"","")+'"' #may need char quote escaping in doc
query_sig="\""+data[:ind]+"\"" #takes original signature with datatype and arg name for java
language=sys.argv[1]
querytestfile=sys.argv[2] #take file name of query test template- should be in pytest or junit only
Matcher_path=current_path+path_sep+'match_framework_format'+path_sep
Parser_path=parent_path+path_sep+'PythonTestExtraction'+path_sep
query=query.replace('\n','\t')
jars_path=parent_path+path_sep+"jars"+path_sep+"*"

"""Fetch match candidates for given query"""
os.chdir(Matcher_path)
#print("python getQueryMatches.py "+query+" "+query_sig)
os.system("python getQueryMatches.py "+query+" "+query_sig)#get candidate matches from repo to load in fids_info.pkl
fids_info=pickle.load(open('fids_info.pkl', "rb"))
os.chdir(Parser_path)
#call ParseTests_query.py treat as though pytest or junit files provided for query test template
# use those to extract the processed list- something like ParseTests.py with support for only two frameworks
#can pass file with this list to parseTests.py for mapping logic

#for java call parseTests_query_javaparser then os.system("python processExtract.py \"TestMethods\\"...
#For python check if parseAst suffices- assume query only inpytest format and then processExtract

"""Param-mapping requirements: extract metadata from query test template"""
if language=='java':
	os.chdir(queryParser_path)
	os.system("java -cp bin;"+jars_path+";. ParseTests_query_javaparser . "+querytestfile+" "+query_sig+"> querytest.txt")
	os.chdir(Parser_path)
elif language=='python':#supports only pytest
	#print("python parseAst.py D:\\Desktop\\Crosslib_python\\CrossLibTest\\query\\"+querytestfile+" "+query_sig[1:query_sig.find('(')]+" "+query_sig+" > D:\\Desktop\\Crosslib_python\\CrossLibTest\\query\\querytest.txt")
	os.system("python parseAst.py "+queryParser_path+path_sep+querytestfile+" "+query_sig[1:query_sig.find('(')]+" "+query_sig+" > "+queryParser_path+path_sep+"querytest.txt")



os.system("python processExtract.py "+queryParser_path+path_sep+"querytest.txt > "+queryParser_path+path_sep+"querytestp.txt")
if not os.path.exists(parent_path+path_sep+"ParamMap"+path_sep+"mappings.txt"):
	#a blank file that will be populated with mappings per candidate match function in each lines
	if 'win' in platform:
		os.system("fsutil file createnew "+parent_path+path_sep+"ParamMap"+path_sep+"mappings.txt 0")
	else:
		os.system("touch "+parent_path+path_sep+"ParamMap"+path_sep+"mappings.txt")
		
#Extract tests into feature list form and Store param mappings in ParamMap\mappings.txt
generator_path=parent_path+path_sep+"TestGenerator"+path_sep
"""Extract tests from candidates"""	

con=sql_connection()
#print(fids_info)
for val in fids_info: #test is filepath name to testsuite and testname_fname=soot version of it or just function name in case of python
	wtscore=0
	try:
		#print()
		if val[1]:
			(fid,test,testname_fname,sig,doc,wtscore)=val
			#print(sig)
		else:
			print("skipped",val[0])
			continue
		#fetch sig_m full version and pass
		m_sig_full=sql_fetch(con,"select fn_signature from functions where fn_id=?",(fid))[0][0]
		doc=doc.replace("\"","")
		doc=doc.replace('\n','\t')
		#print(test+" "+testname_fname+" "+query_sig+" ## "+query+" ## \""+m_sig_full+"\" ## \""+doc+"\"")
		os.chdir(Parser_path)#as in for loop and changing later
		#print(test,testname_fname)
		try:
			if 'final ' in sig and test.endswith(".java"):#remove final keyword in sig
				sig=sig.replace('final ','')
				m_sig_full=m_sig_full.replace('final ','')
			sig=sig.replace('\\','')
			m_sig_full=m_sig_full.replace('\\','')
			doc=doc.replace('<',"")
			doc=doc.replace('>',"")
			#print(doc)
			os.system("python ParseTests.py "+test+" "+testname_fname+" \""+sig+"\" "+query_sig+" "+query+" \""+m_sig_full.replace('\\','')+"\" \""+doc+"\" "+str(wtscore))
			#print('##')
		except Error:
			print('skipping')
		mapping_file=parent_path+path_sep+"ParamMap"+path_sep+"mappings.txt"
		with open(mapping_file, 'r',encoding='latin-1') as f:
			dat=f.read()
			#print(dat)
			if(not dat or dat.strip()==""):
				print('skipping ',fid)
				continue
	
		# on obtaining mappings.txt call generator
		os.chdir(generator_path)
		proc_tests=Parser_path+"TestMethods"+path_sep+test[:test.find('.')]+"_"+sig.split('(')[0]+"_testp.txt"
		lang=''
		if test.endswith('.py') or test.endswith('.doctest') or test.endswith('.ipynb'):
			lang='python'
		elif test.endswith('.java'):
			lang='java'
		#filepath to query test template
		#filepath to mappings file
		#filepath to extracted and processed tests from matches
		#match lang
		os.system("python CallGenerator.py "+queryParser_path+path_sep+querytestfile+" "+mapping_file+" "+proc_tests+" "+lang)
		print("processed",fid)
	except Error:#to debug or ignore matches with tricky tests
		continue#print(Error)#disable print- replace with continue when finalized
		

con.close()	

os.remove(parent_path+path_sep+"ParamMap"+path_sep+"mappings.txt")
end = timeit.default_timer()
print("Execution time: ",end-start)
print("Test suite returned at: "+queryParser_path+path_sep+querytestfile)
