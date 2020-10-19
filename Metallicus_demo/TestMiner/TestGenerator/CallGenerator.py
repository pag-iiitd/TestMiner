"""TODO: 1) Load test template file and depending on .py or .java call appropriate generator script
2) Load data from mappings.txt to pass through type conversion to load in array and pass to py/java scripts 
May require type conversion later- atleast have Boolean and None-null conversion first or string in 
single quote to double quote for Java- even for elements inside list types
Assumptions: Python is in pytest format with assert == format as methodcall(args)==exp_op. 
Java uses unittest with a single method in the class and assertEquals only as methodcall(args),exp_op
Inputs: template, extracted_tests file, mappings file
Sample: >python CallGenerator.py D:\\Desktop\\Crosslib_python\\CrossLibTest\\query\\test_temp.py D:\\Desktop\\Crosslib_python\\CrossLibTest\\ParamMap\\mappings.txt D:\\Desktop\\Crosslib_python\\CrossLibTest\\PythonTestExtraction\\TestMethods\\org\\apache\\commons\\validator\\routines\\InetAddressValidatorTest_isValid_testp.txt java
"""

import copy
import sys
import os
from PytestGen import *

current_path=os.getcwd()
path_sep=os.path.sep
parent_path=current_path[:current_path[:-1].rfind(path_sep)]

jars_path=parent_path+path_sep+"jars"+path_sep+"*"
templatefp=sys.argv[1] #filepath to query test template
mappingfp=sys.argv[2] #filepath to mappings file
match_tests=sys.argv[3] #filepath to extracted and processed tests from matches
match_lang= sys.argv[4] # can be inferred from test file extension in master.py
def load_process_data():
	if templatefp.endswith('.py'):
		to_lang='python'
	elif templatefp.endswith('.java'):
		to_lang='java'
	with open(match_tests, 'r',encoding='utf-8') as f:
		dat=f.read()
		if(not dat):
			sys.exit(0)
		else:
			try:
				tests = eval(eval(str(dat)).decode('utf-8',"backslashreplace"))
			except:
				tests=eval(eval(str(dat).replace('\\n','\\\\n')).decode('utf-8',"backslashreplace"))
				#print(tests)
	with open(mappingfp, 'r',encoding='utf-8') as f:
		mappings = eval(str(f.read()))
	#convert values to update in lists of tests
	
	tests_copy=copy.deepcopy(tests) #to iterate while converted values are updated in original tests
	ctr1=0
	for case in tests_copy:
		ctr2=0
		for arg_element in case:
			value= str(arg_element[0])
			value_converted=converttype(value,match_lang,to_lang) #TODO: check if value always in string type with extra loaded quotes
			#print(value,value_converted)
			tests[ctr1][ctr2][0]=value_converted
			ctr2=ctr2+1
		ctr1=ctr1+1
	#print(tests)
	
	testlist_forgen=list() #contains list of exp,args.. converted values ordered from mappings as to be passed to generator
	#initialize above list as later actual values are to be appended at certain indices
	test_num=len(tests)#number of test cases
	arg_num=len(mappings)#number of arg values per test case
	for j in range(test_num):
		list_tmp=list()
		for i in range(arg_num+1):
			list_tmp.append(0)
		testlist_forgen.append(list_tmp)
	#print(tests)
	#gather all exp_op from tests in exp_list
	exp_list=list()
	for case in tests:
		for arg in case:
			if not arg[1]:
				continue
			if arg[1].startswith('EXP_'):
				exp_list.append(arg[0])
				break
	
	#exp values are added before at 0th indx as they are not in mapping
	for case,exp in zip(testlist_forgen,exp_list):#TODO:check if sublist can be updated when outer iterated
		case[0]=exp
	
	#populate other arg values at ordered position	
	for map in mappings:
		target_ind=map[0]+1
		argname=map[1]
		#TODO: add logic when argname is ##xxx## for default val instead
		ctr=0
		for case in tests:
			if argname.startswith("##") and argname.endswith("##"):#default val
				
				argname=argname.replace('\n','\\n')
				argname=argname.replace('\r','\\r')
				argname=argname.replace('\t','\\t')
				argname=argname.replace('\r','\\r')
				#print(argname)
				val=eval(argname[2:-2])#decode
				testlist_forgen[ctr][target_ind]=val
			else:
				flag=False#indicate that arg found- some mappings don;t hold throughour test file so if mapped arg not present then should be valued None
				for args in case:
					if(args[1]==argname):
						flag=True
						testlist_forgen[ctr][target_ind]=args[0]
						break
				if not flag: #mapped arg not present for that particular test case
					testlist_forgen[ctr][target_ind]='+;+'
			ctr=ctr+1
	
	testlist_forgen_cpy=list()
	for test in testlist_forgen:# this elimination needed for textwrapper like cases in cpython where same function name with diff args
		if '+;+' in test:
			continue
		else:
			testlist_forgen_cpy.append(test)
	
	testlist_forgen=testlist_forgen_cpy
	#print(testlist_forgen)
	# pass testlist to java or python scripts
	if to_lang=='python':
		genpythontest(testlist_forgen,templatefp)
	elif to_lang=='java':
		#write testlist_forgen to a file in a certain format ;#; separated args and each test per line) and pass its filepath instead
		tests_str=''
		for test in testlist_forgen:
			for arg in test:
				arg=str(arg)
				arg=arg.replace('\n','\\n')
				arg=arg.replace('\r','\\r')
				arg=arg.replace('\t','\\t')
				arg=arg.replace('\r','\\r')
				tests_str=tests_str+arg+';#;'
			tests_str=tests_str+'\n'
		java_tests_forgen_fp=parent_path+path_sep+'query'+path_sep+'java_testsforgen.txt'
		with open(java_tests_forgen_fp, 'w',encoding='utf-8') as f:
			f.write(tests_str.encode('ascii','backslashreplace').decode('ascii','backslashreplace'))
			f.close()
		#templatefp: 'D:\\Desktop\\Crosslib_python\\CrossLibTest\\query\\test_temp.java'
		#java_tests_forgen_fp:'D:\\Desktop\\Crosslib_python\\CrossLibTest\\query\\java_testsforgen.txt' 		
		#script to generate tests in test template- assumes format as assertEquals only
		os.system("java -cp "+jars_path+";. AddAsserts "+templatefp+" "+java_tests_forgen_fp)
	

"""for the given value(in string form- extra double quote if actual string) and 'from' and 'to' language 
return converted form as string-  if actual string then in extra double quotes
Support only for two languages as of now
TODO: type conersion for lists, arrays across languages"""
def converttype(value, from_lang,to_lang):
	#print(value)
	if from_lang=='java' and to_lang=='python':
		if value.startswith('"') and value.endswith('"'):#string type
			return value
		elif value=='true':
			return 'True'
		elif value=='false':
			return 'False'
		elif value=='null':
			return 'None'
		else:
			try:
				if not isinstance(eval(value),str):#will not raise except if int, list.. type
					return str(eval(value))
			except:
				value=value.replace('\\','\\\\')
				value=value.replace('"','\\"')
				
				return  '"'+value+'"'#can add if specific cases found

		#TODO: for collections type?			
	elif from_lang=='python' and to_lang=='java':
		if (value.startswith('"') and value.endswith('"')) or (value.startswith('\'') and value.endswith('\'')):
			return '"'+value[1:len(value)-1]+'"'
		elif value=='True':
			return 'true'
		elif value=='False':
			return 'false'
		elif value=='None':
			return 'null'
		else:
			try:
				if not isinstance(eval(value),str):#will not raise except if int, list.. type
					if isinstance(eval(value),list):
						value=value.replace("['","[\"")# for list of strings
						value=value.replace("']","\"]")
						value=value.replace("',","\",")
						value=value.replace(", '",", \"")
						if value[0]=='[' and value[-1]==']':
							value='{'+value[1:-1]+'}'#java array
						return 'new Object[]'+value
						
					return str(eval(value))
			except:
				value=value.replace('\\','\\\\')
				value=value.replace('"','\\"')
				
				return  '"'+value+'"'#can add if specific cases found

	elif from_lang=='java' and to_lang=='java':
		if value=='true':
			return 'true'
		elif value=='false':
			return 'false'
		elif value=='null':
			return 'null'
		else:
			try:
				if not isinstance(eval(value),str):#will not raise except if int, list.. type
					return str(value)
			except:
				value=value.replace('\\','\\\\')
				value=value.replace('"','\\"')
				return  '"'+value+'"'#can add if specific cases found

	elif from_lang=='python' and to_lang=='python':
		try:
			if not isinstance(eval(value),str):#will not raise except if int, list.. type
				return str(eval(value))
		except:
			value=value.replace('\\','\\\\')
			value=value.replace('"','\\"')
				
			return  '"'+value+'"'#can add if specific cases found

load_process_data()		