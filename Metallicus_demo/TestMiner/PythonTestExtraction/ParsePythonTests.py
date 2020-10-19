import sys
import os

#picks the appropriate python ast parsing based on test framework used in match file
matchfile=sys.argv[1] # name of test suite file to parse tests from
path_sep=os.path.sep
if not os.path.isfile('.'+path_sep+matchfile[:-3]+"_test.txt"):
	with open(matchfile,'r') as f:
		content=f.read()
		if 'unittest' in content:
			os.system("python parseUnittestAst.py "+matchfile+" > "+matchfile[:-3]+"_test.txt")
		elif 'pytest' in content:
			os.system("python parseAst.py "+matchfile+" > "+matchfile[:-3]+"_test.txt")

