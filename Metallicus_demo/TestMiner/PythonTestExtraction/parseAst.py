import ast,copy
from filterFunctions import *
import sys

#fname="pytestSample.py"
fname=sys.argv[1]#file name of test suite
funcname=sys.argv[2]
signature=sys.argv[3]
with open(fname,'r',encoding='latin-1') as f:
	tree=ast.parse(f.read())
	#print(ast.dump(tree))


node_arg_mapping={}#global function arg to parametrize arg mapping
#funcname='get_host'
#signature='get_host(url)'

#funcname='parse_url'
#signature='parse_url(url)'
#funcname='url'
#signature='url(value, public=None)'

class ProcessAst(ast.NodeVisitor):
	tmp_arg_var=list()
	tmp_arg_var_key=dict()
	tmp_arg_val_type=list()
	classassgn=dict()#maps class level assignment of var Name's id to val node
			#maps var names (in arglist) passed to target function in test method to actual name in signature. arglist_keys is dict mapping names in invokation mapped to actual names in signature for default valued args
	#NOTE: should be called after functiondef node processed
	def map_sig_to_par(self,arglist, arglist_keys, arg_val_type):#TODO: ignore self par from all functions
		pars=signature.split('(')[1].split(')')[0].split(',')
		name_map=dict()#to replace in argvaltype and with what
		to_remove=list()#record args already used in invocation that can later be removed to process left overs to add to tuples
		ctr=0
		for a in arglist:#arglist would be smaller or equal to pars
			actual=pars[ctr]
			ctr=ctr+1
			if '=' not in actual: # such cases expected to appear before else case
				if not '**' in actual:
					name_map[a]=actual # some actual may be left that could be traversed and added after
			else:
				lhs=actual.split('=')[0].strip()
				if lhs in arglist_keys:
					name_map[arglist_keys[lhs]]=lhs
				else:#if passed without default assignment but is actually default
					name_map[a]=lhs
			to_remove.append(actual) # later removed from pars to process left overs
		to_process=[x for x in pars if x not in to_remove]#assumes will all be with =
		to_add=list()#list of list-tuples to add to all second level list in arg_val_types
		for i in to_process:
			if not '**' in i:
				tmp=i.split('=')
				arg_val=str(eval(tmp[1].strip()))
				arg_name=tmp[0].strip()
				arg_type='python_'+str(type(arg_val)).split("'")[1].strip()
				to_add.append([arg_val,arg_name,arg_type])
		
		arg_val_type_copy=copy.deepcopy(arg_val_type)
		#print("-->",arglist, arglist_keys, arg_val_type)
				
		# actual updation and addition argvaltype, approach:traverse each list, if arg_name not in arglist or arglist_keys then likely the expected output- then update it name with 'EXP' prefix
		for test_ind in range(len(arg_val_type)):
			for arg_ind in range(len(arg_val_type[test_ind])):
				if arg_val_type[test_ind][arg_ind][1] not in arglist and arg_val_type[test_ind][arg_ind][1] not in arglist_keys:# likely expected output
					arg_val_type_copy[test_ind][arg_ind][1]='EXP_'+arg_val_type[test_ind][arg_ind][1]
				elif arg_val_type[test_ind][arg_ind][1] in arglist: #update name from nal_map
					arg_val_type_copy[test_ind][arg_ind][1]=name_map[arg_val_type[test_ind][arg_ind][1]]
			#addition logic
			for i in to_add:
				arg_val_type_copy[test_ind].append(i)

		return arg_val_type_copy	

	def traverseFunctionDef(self,node):
		classnode=None
		all_test=list()
		for nd in ast.walk(tree):#walks bfs order
			if isinstance(nd, ast.ClassDef):
				classnode=nd
			elif isinstance(nd, ast.Assign) and classnode!=None and nd in ast.iter_child_nodes(classnode) and not isinstance(nd.value, ast.Name) and not isinstance(nd.value, ast.Call):#assignment as class field and 'most likely' points to some constant
				self.classassgn[nd.targets[0].id]=nd.value	#Name node to value mapping		
			elif isinstance(nd, ast.FunctionDef):
				arg_details=list()
				for n in ast.walk(nd):
					if isinstance(n,ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr=='parametrize': #logic for reference passing to parametrize:
						self.getArgs(n)
						#if arg_details:
						#	break
				for n in ast.walk(nd):#another iteration needed as walk if bfs and assert visited before call nodes					
					if isinstance(n, ast.Assert):
						arg_tmp=self.checkRelevantAssert(n)
						
					if isinstance(n, ast.Assert) and isinstance(n.test,ast.Compare):#comparison inside assert
						if not arg_tmp or len(arg_tmp)==0:
							continue
						else:
							arg_details=arg_tmp
						if len(n.test.comparators)==1:
							if isinstance(n.test.comparators[0], ast.NameConstant):#others will get captured from parametrize, these hardcoded are added to output here
								if n.test.comparators[0].value == True or n.test.comparators[0].value == False:							
									expected=[str(n.test.comparators[0].value),'EXP_op','python_bool']
								else:
									expected=[str(n.test.comparators[0].value),'EXP_op','python_NoneType']
								if arg_details:
									tmp_copy=copy.deepcopy(arg_details)
									for i in range(len(tmp_copy)):
										arg_details[i].append(expected)
					elif isinstance(n, ast.Assert) and not isinstance(n.test, ast.Compare) and n.msg==None: #assuming visited after calls
						#print("here..")
						if not arg_tmp or len(arg_tmp)==0:
							continue
						else:
							arg_details=arg_tmp
						expected=['True','EXP_op','python_bool']#default
						if isinstance(n.test, ast.UnaryOp) and isinstance(n.test.op, ast.Not):
							expected=['False','EXP_op','python_bool']		#for assert not				
						for nd in ast.walk(n):#for validationfailure assume expected op is False
							if isinstance(nd,ast.Call):
								for obj in nd.args:
									if isinstance(obj,ast.Name) and obj.id=='ValidationFailure':
										expected=['False','EXP_op','python_bool']
										break
						
						if arg_details and len(arg_details)>0:
							tmp_copy=copy.deepcopy(arg_details)
							#print(arg_details)
							for i in range(len(tmp_copy)):
								arg_details[i].append(expected)
				if arg_details and len(arg_details)>0:
					all_test.extend(arg_details)				
				#print("\n***************\n")
				
		print(all_test)
		#self.generic_visit(node)
		
	#returns arg details if assert is on target function, else None. This is to ignore useless asserts
	def checkRelevantAssert(self,AssertNode):
		for nd in ast.walk(AssertNode):#for validationfailure assume expected op is False
			if isinstance(nd,ast.Call) and isinstance(nd.func, ast.Name):#will fetch call from assert test as well as args
					if nd.func.id==funcname:
						args=self.getArgs(nd)
						#print(nd.func.id+";;"+str(args))
						return args
		return None
		
#mapped actual arg name as in function signature to target function to names passed in parametrize	
	def getArgs(self,CallNode):#Assumes primitive type args and only two calls per function
		arg_var=list() #stores arguments names of target function
		arg_var_key=dict() # stores mapping to actual keyword in case of default values present
		arg_val_type=list() #stores tuple of this list of size 3 [value, argname, datatype] for each relevant value- it's a list of tuples of lists
		arg_indx=dict()	#stores index to arg name and potentially expected arg, appearing in parametrize- may also have expected value's var name	
		#print(type(CallNode.func))

		if isinstance(CallNode.func, ast.Name) and not CallNode.func.id==funcname:#ignore other function calls
			return		

		for n in CallNode.args:
			#print(n)
			if isinstance(n, ast.Name) and isinstance(CallNode.func, ast.Name) and CallNode.func.id==funcname: #extract arg names as from target function call
				#print('deep..',CallNode.func.id)
				arg_var.append(n.id)
			elif isinstance(n, ast.Str):#initial one may indicate var names in parametrize
				if len(arg_val_type)==0:
					var_names=n.s.split(',')
					ctr=0
					for v in var_names:
						arg_indx[ctr]=v.strip()
						ctr=ctr+1
			elif isinstance(n,ast.Tuple):#initial one may indicate var names in parametrize
				if len(arg_val_type)==0:
					ctr=0					
					for e in n.elts:
						if isinstance(e,ast.Str):
							arg_indx[ctr]=e.s
							ctr=ctr+1
			elif isinstance(n, ast.List):#indicates begining of values or initial var- further parsing may need recursive call(or separate function for datatype parsing logic) and tackle tuples
				if len(arg_indx)==0:#assumes function args from parametrize may have been processed first
					ctr=0					
					for e in n.elts:
						if isinstance(e,ast.Str):
							arg_indx[ctr]=e.s
							ctr=ctr+1
				else:#test traversal
					
					for e in n.elts:# two possiblities- a tuple or non-tuple--non-tuple indicates single input to parametrize so arg should have 0th key only						
						tests_tup=list()#list of all arg lists					
						if not isinstance(e,ast.Tuple):					
							
							tup=['',arg_indx[0],'']
							tests_tup.append(self.parse_types(e,tup))
						else:#Tuple type
							ctr=0
							for t in e.elts:							
								tup=['',arg_indx[ctr],'']
								tests_tup.append(self.parse_types(t,tup))
								ctr=ctr+1
						arg_val_type.append(tests_tup)# add the processed test args to master tuple		
			elif isinstance(n, ast.Name) and isinstance(CallNode.func, ast.Attribute) and CallNode.func.attr=='parametrize': #logic for reference passing to parametrize
				if isinstance(self.classassgn[n.id], ast.List):#assuming for test cases
					for e in self.classassgn[n.id].elts:# two possiblities- a tuple or non-tuple--non-tuple indicates single input to parametrize so arg should have 0th key only						
						tests_tup=list()#list of all arg lists					
						if not isinstance(e,ast.Tuple):					
							tup=['',arg_indx[0],'']
							tests_tup.append(self.parse_types(e,tup))
						else:#Tuple type
							ctr=0
							for t in e.elts:							
								tup=['',arg_indx[ctr],'']
								tests_tup.append(self.parse_types(t,tup))
								ctr=ctr+1
						arg_val_type.append(tests_tup)# add the processed test args to master tuple		

	
		for k in CallNode.keywords:
			if isinstance(k, ast.keyword):
				arg_var.append(k.value.id)
				arg_var_key[k.arg]=k.value.id#for keywords stores mapping from actual name to arg

		if len(arg_var)>0:
			self.tmp_arg_var=copy.deepcopy(arg_var)
			self.tmp_arg_var_key=copy.deepcopy(arg_var_key)

		if len(arg_val_type)>0:
			self.tmp_arg_val_type=copy.deepcopy(arg_val_type)


		arg_val_type_copy=arg_val_type
		if isinstance(CallNode.func, ast.Name) and CallNode.func.id==funcname:
			#print(self.tmp_arg_var)
			arg_val_type_copy=self.map_sig_to_par(self.tmp_arg_var, self.tmp_arg_var_key, self.tmp_arg_val_type)

		#TODO cases: class attribute invocation, keyword default can be missing from parameterize
		#print(arg_var)
		#print(arg_var_key)
		#print(arg_val_type)
		return arg_val_type_copy

	#for traversal of actual parametrize values in list- store types like List, Tuple as string in appropriate denotation
	def parse_types(self,n,tup):
		if isinstance(n, ast.Num): 
			tup[0]=str(n.n)
			tup[2]='python_int' #could be float?			
		elif isinstance(n, ast.Str):# TO SUPPORT: initial one may indicate var name
			tup[0]=n.s.encode('ascii','backslashreplace').decode('ascii')
			tup[2]='python_str'			
		elif isinstance(n, ast.Bytes):
			tup[0]=str(n.s)
			tup[2]='python_bytes'			
		elif isinstance(n, ast.NameConstant):#boolean or none type check
			tup[0]=str(n.value)
			if n.value == True or n.value == False:
				tup[2]='python_bool'
			elif n.value==None:
				tup[2]='python_NoneType'

		elif isinstance(n, ast.List):#indicates list type input
			s='['
			for e in n.elts:
				s=s+self.parse_types(e,['','',''])[0]+', '#assumes no nested list or tuple in list occurs
			s=s[:-2]+']'#-2 to remove last ', '
			tup[0]=s			
			tup[2]='python_list'

		elif isinstance(n, ast.Tuple):
			s='('
			for e in n.elts:
				s=s+self.parse_types(e,['','',''])[0]+', '
			s=s[:-2]+')'#-2 to remove last ', '
			tup[0]=s		
			tup[2]='python_tuple'
		
		elif isinstance(n,ast.Dict):
			s='{'
			for k,v in zip(n.keys,n.values):
				s=s+self.parse_types(k,['','',''])[0]+': '+ self.parse_types(v,['','',''])[0]+', '#assumes no nested list cases
			s=s[:-2]+'}'#-2 to remove last ', '
			tup[0]=s
			tup[2]='python_dict'

		elif isinstance(n,ast.Set):
			s='{'
			for e in n.elts:
				s=s+self.parse_types(e,['','',''])[0]+', '
			s=s[:-2]+'}'#-2 to remove last ', '
			tup[0]=s
			tup[2]='python_set'

		return tup
		
		
at=ProcessAst()
at.traverseFunctionDef(tree)
#at.traverse()
