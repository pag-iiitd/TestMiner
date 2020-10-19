#for post processing of extracted tests in a readable format and further feature addition.

import re
import sys

#Java: for list of string add quotes and escape single quotes for strings with quote inside
def process_tuple(list3):
	if 'String[]' in list3[2] or 'char[]' in list3[2]:
		list3[0]=list3[0].replace('[','[\"')
		list3[0]=list3[0].replace(']','\"]')
		#list3[0]=list3[0].replace('\'[','[\'')
		#list3[0]=list3[0].replace(']\'','\']')
		list3[0]=list3[0].replace(', ','\", \"')
		#note: all elements are stored as string and eval later
		list3[0]=eval(list3[0])
	elif re.match('^\-?[0-9]+(\.[0-9]+)?$',list3[0]) and not re.match('^0[0-9\.]+$',list3[0]) and (list3[0][0:2]!='-0') and list3[2]!='python_str':#for numeric entities such that they do not begin with 0 or -0
		#print(list3)
		list3[0]=eval(list3[0])
	elif re.match('^[\[\{].+[\}\]]$',list3[0]) and list3[2]!='python_str':#for lists and dictionary
		#print(list3[0])
		try:
			list3[0]=eval(list3[0])
		except: #if var name passed to dict then treat as string
			pass
	elif 'bool' in list3[2] or 'None' in list3[2]:
		list3.append(None)
		return list3
	#NOTE: let other types be treated as strings
	list3.append(getfeatures(list3[0]))
	return list3

#returns list of features on char type, len, abs_rep from string or numeric type. Add returned list as fourth element to trio- for lists, tuples, dict type None is added
#TODO: can we extract anything from list or tuple?
def getfeatures(ele):
	#print(ele,type(ele))
	if isinstance(ele, str):
		if ele.startswith("\"") and ele.endswith("\""):
			ele=ele[1:-1]#remove leading and trailing double quotes
		
		abstractrep=ele	
		chartype='M'#Types: Numeric(N), Letter(L), LetterUpper(UL), LetterLower(LL), Specialchar(S), AlphaNumeral(ANM), LetterNumeralSplMix(M)
		length=[len(str(ele)),'L']#Tuple of magnitude and category: Short(S)<4, Medium(M)4<=m<=10, Long(L)>10

		if re.match('^\-?[0-9]+(\.[0-9]+)?$',ele) and ele!='-0' and not re.match('^0[0-9\.]+$',ele):
			chartype='N'
		elif re.match('^[A-Z]+$',ele):
			chartype='UL'
		elif re.match('^[a-z]+$',ele):
			chartype='LL'
		elif re.match('^[a-zA-Z]+$',ele):
			chartype='L'
		elif re.match('^[0-9a-zA-Z]+$',ele):
			chartype='ANM'
		elif re.match('^[\s\W_]+$',ele):#all spl char with whitespace char or nonalphanumeral
			chartype='S'
		else:
			chartype='M'

		if len(str(ele))<4:
			length[1]='S'
		elif len(str(ele))>=4 and len(str(ele))<=10:
			length[1]='M'
		else:
			length[1]='L'
		abstractrep=abstract(ele)
		return [chartype,length,abstractrep]

	if isinstance(ele,int) or isinstance(ele,float):
		#no type so insert blank there, also no abstracttype so blank there
		length=[len(str(ele)),'IM']#number of digits and range type: Small(IS)<2digit, Medium(IM) 2<=m<=3, Large 1000<=l<10000(IL)  >3, Very Large above 100000 (IVL) >5
		if ele<=99:
			length[1]='IS'
		elif ele>99 and ele<1000:
			length[1]='IM'
		elif ele>=1000 and ele<100000:
			length[1]='IL'
		elif ele>=100000:
			length[1]='IVL'
		return ['',length,'']

#returns abstract representation of a string. These representations to be used to compute edit-distance between pairs
def abstract(ele):
	#Represent L for letters, D for digits, leave spl char as is 
	s=''#to store abstracted rep
	for i in ele:
		if re.match('[0-9]',i):
			s=s+'D'
		elif re.match('[a-zA-Z]',i):
			s=s+'L'
		else:
			s=s+i
	ctr=1
	prev=None
	s_comp=''
	if s and s[0]!='L' and s[0]!='D':#special char at beginning
		s_comp=s_comp+s[0]

	for chr in s:
		if prev:
			if prev==chr and (prev=='L' or prev=='D'):
				ctr=ctr+1
			else:
				if prev!=chr and (prev=='L' or prev=='D'):
					s_comp=s_comp+prev+str(ctr)
					ctr=1
				if chr!='L' and chr!='D':
					s_comp=s_comp+chr
		#print(s_comp,ctr,chr)		
		prev=chr
	if prev:
		#s_comp=s_comp+prev
		if prev=='L' or prev=='D':
			s_comp=s_comp+prev+str(ctr)
	return s_comp
	
#receives input from test extractor- java, python- pytest or unittest
def convert_tests(fname):
	#fname="run_op.txt"
	d=None
	with open(fname,'r',encoding='latin-1') as f:
		data=str(f.read()).strip()
		if data[-3:]==', [' or data[-3:]==',\n[':
			d='[['+data[:-3]+']'
	if(not data):
		sys.exit(0)
	if(d):
		with open(fname,'w',encoding="latin-1") as f:
			f.write(d)
	
	with open(fname,'r',encoding='latin-1') as f:#TODO: add quotes insode array or list types- can do at the stage of type-conversion also needed before dynamic feature processing
		#data=data.replace("'","\\\'")
		data=f.read()
		data=data.strip()
		#data=data.replace("=","$@$")#= cant be eval
		if ";#" in data:#indicates java as source
			
			data=data.strip().replace('\\','\\\\')
			data=data.replace('\\\\u','\\u')
			data=data.strip().replace('\"','\\"')
			data=data.replace(";#","\"")#on escaping double quotes in java and introducing original	
		data=data.replace('\n','\\n')
		data=data.replace('\r','\\r')
		data=data.replace('\u0000','\\u0000')
		data=data.replace('\\x00','\\u0000')
		#data=data.replace('\t','\\t')
		#data=data.encode('ascii','backslashbackslashreplace').decode('ascii','backslashbackslashreplace')
		#print(data)
		data=eval(data)
		#remove duplicates
		test_data=list()
		#print(data)
		for test in data:
			if len(test)==1:#indicates only exp_op in the test- possible test_wrap like cases where generic call to a fucntion in unittest- discard such tests
				continue
			case=list()
			for ele in test:
				if not ele[1]:
					continue
				ele_proc=process_tuple(ele)
				if ele_proc not in case:
					case.append(ele_proc)
			test_data.append(case)
		print(str(test_data).replace('\\n','\n').replace('\\r','\r').replace('\\u0000','\u0000').replace('\\t','\t').encode('latin-1','backslashreplace'))
	#TODO: iterate test_Data and process each tuple
	f.close()
try:
	convert_tests(sys.argv[1])
except:
	print('')
#if __name__=="__main__":
#	convert_tests('validators_url_tests.txt')
