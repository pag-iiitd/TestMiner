# -*- coding: latin-1 -*-
import sys
import os
#python ParseTests.py python_repo\validators_repo\tests\test_url.py url "url(value, public=None) ......"
#python ParseTests.py com\google\common\primitives\IntsTest.java com.google.common.primitives.IntsTest "tryParse(java.lang.String) ...."
#python ParseTests.py python_repo\stringutils_repo\tests.py is_url "is_url(string, allowed_schemes=None) ....."

def line_prepender(filename, line):
    with open(filename, 'r+',encoding='latin-1') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

#integrate test extraction logic for java and python. takes 3 inputs for java and 1 for python. 
#Further processes to get features etc.
#output: processed file with features suffixed with _testp.txt
#TODO: check incremental build option
#Java datatype expansion not needed as soot seems to accept String instead of java.lang.String
matchfile='"'+sys.argv[1]+'"' # name of test suite file to parse tests from eg. TestMethods\\IntsTest.java , TestMethods\\unittestSample_adv2.py
funcsig='"'+sys.argv[3]+'"' #tryParse(java.lang.String), wrap(text, width=70,  **kwargs) NOTE: return type check removed on signature- approximation
path_sep=os.path.sep
curr_dirpath=os.getcwd()
function_name=funcsig[1:].split('(')[0]
match_score=sys.argv[8]

parent_path=curr_dirpath[:curr_dirpath[:-1].rfind(path_sep)]
jars_path=parent_path+path_sep+"jars"+path_sep+"*"
equinox_jar='"'+parent_path+path_sep+'jars'+path_sep+'org.eclipse.equinox.launcher_1.4.0.v20161219-1356.jar"'
#print('.\\TestMethods\\'+matchfile[1:matchfile.find('.')]+"_test.txt")
if not os.path.isfile('.'+path_sep+'TestMethods'+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_test.txt"):
#logic to check of java v/s python script based on file ext
	#print(matchfile)
	if matchfile.endswith('.java\"'):#funsig should only have datatype but db sig has var name as well- discard
		#print('JAVA')
		#NOTE: buildin workspace takes long, hence not all projects placed in src folder- rest are right outside src
		testsuite='"'+sys.argv[2]+'"' #matched test suite file name frm bin path eg. TestMethods.IntsTest
		os.chdir(parent_path+path_sep+'CrosslibJavaWorkspace'+path_sep+'CrossLibExtraction'+path_sep)
		os.system('java -jar '+equinox_jar+' -noSplash -data "'+parent_path+path_sep+'CrosslibJavaWorkspace" -application org.eclipse.jdt.apt.core.aptBuild')
		#print(os.getcwd())
		os.system('java -cp bin InstrumentCode.Init '+testsuite)
		os.system('java -jar '+equinox_jar+' -noSplash -data "'+parent_path+path_sep+'CrosslibJavaWorkspace" -application org.eclipse.jdt.apt.core.aptBuild')
		os.system('java -cp bin;'+jars_path+';. InstrumentCode.MethodsExtraction '+testsuite+" "+funcsig)
		os.system('java -jar '+equinox_jar+' -noSplash -data "'+parent_path+path_sep+'CrosslibJavaWorkspace" -application org.eclipse.jdt.apt.core.aptBuild')
		#This will create a file testcases.txt in current directory, containing the extracted testcases
		#print(testsuite, curr_dirpath+'\\TestMethods\\'+matchfile[1:matchfile.find('.')]+"_test.txt")
		os.makedirs(curr_dirpath+path_sep+'TestMethods'+path_sep+matchfile[1:matchfile.rfind(path_sep)],exist_ok=True)
		os.system('java -cp bin;'+jars_path+';. TestMethods.ExtractTestcase '+testsuite+' > '+curr_dirpath+path_sep+'TestMethods'+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_test.txt")
		os.chdir(curr_dirpath)
	elif matchfile.endswith('.py"'):#make it save in Testmethods folder in PythonTestExtraction folder
	#picks the appropriate python ast parsing based on test framework used in match file
		funcname='"'+function_name+'"' #wrap
		with open(matchfile[1:len(matchfile)-1],'r',encoding='latin-1') as f:
			content=f.read()
		#print(curr_dirpath+"\\TestMethods\\"+matchfile[1:matchfile.rfind('\\')])
		os.makedirs(curr_dirpath+path_sep+"TestMethods"+path_sep+matchfile[1:matchfile.rfind(path_sep)], exist_ok=True)
		if 'unittest' in content:#executes generated instrumentation to obtain code for processing
			#print("TestMethods\\"+matchfile[1:matchfile.find('.')]+"_test.txt")
			os.system("python parseUnittestAst.py "+matchfile[1:len(matchfile)-1]+" "+funcname+" "+funcsig+" > "+matchfile[1:matchfile.find('.')]+"_"+function_name+"_instr.py")
			line_prepender(matchfile[1:matchfile.find('.')]+"_"+function_name+"_instr.py",'import unittest')
			line_prepender(matchfile[1:matchfile.find('.')]+"_"+function_name+"_instr.py",'# -*- coding: latin-1 -*-')
			if 'unittest.main()' not in content:
				with open(matchfile[1:matchfile.find('.')]+"_"+function_name+"_instr.py", "a",encoding='latin-1') as myfile:
					myfile.write("if __name__ == '__main__':\n\tunittest.main()")
			os.system("python "+matchfile[1:matchfile.find('.')]+"_"+function_name+"_instr.py"+" > TestMethods"+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_test.txt")
		elif 'pytest' in content:
			#print(matchfile[1:len(matchfile)-1], "TestMethods\\"+matchfile[1:matchfile.find('.')]+"_test.txt")
			os.system("python parseAst.py "+matchfile[1:len(matchfile)-1]+" "+funcname+" "+funcsig+" > TestMethods"+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_test.txt")
#add post processing logic- call that code
#print(curr_dirpath+"\\TestMethods\\"+matchfile[1:matchfile.rfind('\\')])
os.makedirs(curr_dirpath+path_sep+"TestMethods"+path_sep+matchfile[1:matchfile.rfind(path_sep)], exist_ok=True)
#print("$$$")
os.system("python processExtract.py \"TestMethods"+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_test.txt\" > TestMethods"+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_testp.txt\"")
#print("!!!")

featureExtract_path=curr_dirpath+path_sep+"TestMethods"+path_sep+matchfile[1:matchfile.find('.')]+"_"+function_name+"_testp.txt"

#call param mapping logic to store in a file with fixed name D:\\Desktop\\Crosslib_python\\CrossLibTest\\ParamMap\\mappings.txt
# stores for single match the mappings in file at a time
ParamMapper_path=parent_path+path_sep+'ParamMap'+path_sep
os.chdir(ParamMapper_path)
#query and match takes names of feature extracted files; documentations from which param desc is extracted; 
#match signatures original: match_featfile,sig_q,doc_q,sig_m,doc_m
#print(sys.argv[7])
os.system("python MapParams.py "+featureExtract_path+" \""+sys.argv[4]+"\" \""+sys.argv[5]+"\" \""+sys.argv[6]+"\" \""+sys.argv[7]+"\" "+str(match_score)+" >mappings.txt")