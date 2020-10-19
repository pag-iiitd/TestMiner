import ast,copy,astunparse
from filterFunctions import *
import sys

#fname="InsertionTest_sample.py"
#fname="unittestSample_adv2.py"
fname=sys.argv[1] #file name of test suite
funcname=sys.argv[2]
signature=sys.argv[3]
with open(fname,'r',encoding='latin-1') as f:
	tree=ast.parse(f.read())
	#print(ast.dump(tree))


"""Module(body=[FunctionDef(name='sampletest', args=arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[Assign(targets=[Name(id='x', ctx=Store())], value=Num(n=4)), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Str(s='x'), Str(s=','), Name(id='x', ctx=Load()), Str(s=','), Call(func=Name(id='type', ctx=Load()), args=[Name(id='x', ctx=Load())], keywords=[]), Str(s=';')], keywords=[keyword(arg='sep', value=Str(s=''))])), If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Lt()], comparators=[Num(n=3)]), body=[Return(value=NameConstant(value=True))], orelse=[Return(value=NameConstant(value=False))])], decorator_list=[], returns=None)])
"""

#funcname='get_host'
#signature='get_host(url)'

#funcname='is_url'
#signature='is_url(string, allowed_schemes=None)'

#funcname='wrap'
#signature='wrap(text, width=70,  **kwargs)'

"""
#node insertion sample
for nd in ast.walk(tree):
	if isinstance(nd,ast.FunctionDef):
		c=0
		for n in nd.body:
			if isinstance(n, ast.Assign):
				newnode=ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[ast.Str(s='Hello')], keywords=[]))
					
			c=c+1
		nd.body.insert(c,newnode)
print(astunparse.unparse(tree))
"""

"""Samples:
>>> r=ast.parse('mad(d).host(e)')
>>> ast.dump(r)
"Module(body=[Expr(value=Call(func=Attribute(value=Call(func=Name(id='mad', ctx=Load()), args=[Name(id='d', ctx=Load())], keywords=[]), attr='host', ctx=Load()), args=[Name(id='e', ctx=Load())], keywords=[]))])"
>>> print('fish','root',4)
fish root 4
>>> r=ast.parse("print('fish','root',4)")
>>> ast.dump(r)
"Module(body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Str(s='fish'), Str(s='root'), Num(n=4)], keywords=[]))])"
"""


assertion_template={'assertEqual':'*','assertTrue':ast.NameConstant(value=True), 'assertFalse':ast.NameConstant(value=False), 'assertIsNone':ast.NameConstant(value=None)}#maintain mapping to assertion name and expected output, if available, else '*'


def traverseNode():
	rel_func=getRelFunctions(tree,funcname, signature)
	for nd in ast.walk(tree):
		if isinstance(nd,ast.FunctionDef) and nd in rel_func:
			ctr=0 #maintain index of body element/statement
			printnode_to_index=dict()#maps newnode to position to insert
			for n in nd.body:#insertion to body not possible during its iteration- store mappings- loop body and if else indexing differnt; insert at end of walk iteration
				if isinstance(n, ast.Assign) and isinstance(n.value,ast.Call): #ignore operations in rhs as they may introduce redundancy- derived will likely be used in target function
					nodes=analyseCall(n.value)
					if nodes:
						#print(nodes)
						printnode_to_index[ctr+1]=getPrintNode(nodes)
				elif isinstance(n, ast.Expr):#ignore other expr i.e operations and function calls other han assertion as they may ony introduce redundancy. Useful calls in assign stmt
					if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr and 'assert' in n.value.func.attr:
						nodes=analyseCall(n.value)
						if nodes:
							#print(nodes)
							printnode_to_index[ctr+1]=getPrintNode(nodes)
					elif isinstance(n.value,ast.Call):#explore case of target function being passed to expr call invoke eg. check(wrap(text), expect)
						for a in n.value.args:
							if isinstance(a, ast.Call) and ((isinstance(a.func,ast.Name) and a.func.id==funcname) or (isinstance(a.func,ast.Attribute) and a.func.attr==funcname)):#check direct function call in argument or onelevel attribute function call
								nodes=analyseCall(a)
								if nodes:
									#print(nodes)
									printnode_to_index[ctr-1]=getPrintNode(nodes)#-1 as exp_op should be printed later
								break

				
				ctr=ctr+1
			cn=0
			for pn in printnode_to_index:
				nd.body.insert(pn+cn,printnode_to_index[pn])
				cn=cn+1
	print(astunparse.unparse(tree).encode('ascii','backslashreplace').decode('ascii','backslashreplace'))


#print statement formulation for different data types and collections, should print tuple of val,name,type. Takes list of nodes input for which to print in single line- node could be Expr or Name ref or constants of Str, Num, List, Dict, Tuple, Set- assume lists etc. will not contain name refs.
def getPrintNode(nodestoprint):
	arglist=list()
	for n in nodestoprint:
		tmplist=list()
		tmplist.append(ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[n], keywords=[]))
		tmplist.append(ast.Str(nodestoprint[n]))
		#tmplist.append(ast.Call(func=ast.Name(id='type', ctx=ast.Load()), args=[n], keywords=[]))
		tmplist.append(ast.BinOp(left=ast.Str(s='python_'), op=ast.Add(), right=ast.Subscript(value=ast.Call(func=ast.Attribute(value=ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[ast.Call(func=ast.Name(id='type', ctx=ast.Load()), args=[n], keywords=[])], keywords=[]), attr='split', ctx=ast.Load()), args=[ast.Str(s="\'")], keywords=[]), slice=ast.Index(value=ast.Num(n=1)), ctx=ast.Load())))
		listnode=ast.List(elts=tmplist, ctx=ast.Load)
		arglist.append(listnode)
		if nodestoprint[n] and 'EXP_' in nodestoprint[n]:
			arglist.append(ast.Str(s='], ['))
		else:
			arglist.append(ast.Str(s=', '))

	newnode=ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=arglist, keywords=[ast.keyword(arg='sep', value=ast.Str(s='')),ast.keyword(arg='end', value=ast.Str(s=''))]))

	return newnode


#precondition: call coming 1 level down from assign(rhs) or expr with assert. Should return info tuple on nodes to print.
def analyseCall(callNode):
	nodestoprint=dict()#dict of node whose node to args name to print- specially needed for constants
	if isinstance(callNode.func,ast.Attribute) and callNode.func.attr and 'assert' in callNode.func.attr:
		#process assertion stmt and expected val by template
		if callNode.func.attr in assertion_template:		
			expected_node=assertion_template[callNode.func.attr]#else assertion not supported
			exp='EXP_op'#argname of expected value of assert with EXP
			ele=callNode.args[0] #ignore if ele a nameref type as of no use, hence only considered call type
			if expected_node == '*':		
				expected_node=callNode.args[1]#Name ref or constant type
			
			if isinstance(ele, ast.Call):#checks if target function and signature to get defaults and keywords, assume atmost one level of attribute
				if isinstance(ele.func, ast.Attribute):#attributed call#fetch args/keywords
					if ele.func.attr==funcname or (isinstance(ele.func.value,ast.Attribute) and ele.func.value.attr==funcname):#one level attribute or two level attribute- send for sig mapping
						keywords_map=dict()						
						if ele.keywords:
							for k in ele.keywords:
								keywords_map[k.arg]=k.value
						nodestoprint=merge(nodestoprint,map_sig_to_par(ele.args,keywords_map))
						nodestoprint[expected_node]=exp	
					elif isinstance(ele.func.value, ast.Call) and ele.func.attr==funcname:#extract args/keywords of parent function of form a(x).target(y)--> if x Name ref then use it for argname, else unknown, assume keyword arg names distinct across parent and child calls
						keywords_map=dict()						
						if ele.keywords:
							for k in ele.keywords:
								keywords_map[k.arg]=k.value
						nodestoprint=merge(nodestoprint,map_sig_to_par(ele.args,keywords_map))	
						#process parent attributes:
						for a in ele.func.value.args:
							if isinstance(a,ast.Name):
								nodestoprint[a]=a.id
							else:
								nodestoprint[a]='arg'#name not known,if constants or could be expr also
						if ele.func.value.keywords:
							for k in ele.func.value.keywords:
								nodestoprint[k.arg]=k.value
						nodestoprint[expected_node]=exp
				elif isinstance(ele.func,ast.Name) and ele.func.id==funcname:#straightforward call- extract args, keywords from map to sig
					keywords_map=dict()						
					if ele.keywords:
						for k in ele.keywords:
							keywords_map[k.arg]=k.value
					nodestoprint=merge(nodestoprint, map_sig_to_par(ele.args,keywords_map))	
					nodestoprint[expected_node]=exp	
			
			elif isinstance(ele, ast.Name): #ignore as name ref will not get args- would have been captured from assignment stmt where target function called. but need to capture expected value
				nodestoprint[expected_node]=exp
	
	else:# in value to assgn
		#similar logic as above, except no check on whether call on target func
		if isinstance(callNode.func,ast.Name):#straightforward call to method: x=y(z)
			keywords_map=dict()						
			if callNode.keywords:
				for k in callNode.keywords:
					keywords_map[k.arg]=k.value
							
			if callNode.func.id==funcname:
				nodestoprint=merge(nodestoprint, map_sig_to_par(callNode.args,keywords_map))	
			else:
				for a in callNode.args:
					if isinstance(a,ast.Name):
						nodestoprint[a]=a.id
					else:
						nodestoprint[a]='arg'#name not known,if constants or could be expr also
				for k in callNode.keywords:
					nodestoprint[k.value]=k.arg
		elif isinstance(callNode.func,ast.Attribute):
			if not isinstance(callNode.func.value,ast.Call): #supports x=y.z(a) or x=y.z.a(b)
				keywords_map=dict()						
				if callNode.keywords:
					for k in callNode.keywords:
						keywords_map[k.value]=k.arg
							
				if callNode.func.attr==funcname:
					nodestoprint=merge(nodestoprint, map_sig_to_par(callNode.args,keywords_map))	

				else:
					for a in callNode.args:
						if isinstance(a,ast.Name):
							nodestoprint[a]=a.id
						else:
							nodestoprint[a]='arg'#name not known,if constants or could be expr also			
					for k in callNode.keywords:
						nodestoprint[k.value]=k.arg
			
			elif isinstance(callNode.func.value,ast.Call):#x=y(a).z(b)
				if callNode.func.attr==funcname:
					keywords_map=dict()						
					if callNode.keywords:
						for k in callNode.keywords:
							keywords_map[k.arg]=k.value
					nodestoprint=merge(nodestoprint, map_sig_to_par(callNode.args,keywords_map))	
						#process parent attributes:
					for a in callNode.func.value.args:
						if isinstance(a,ast.Name):
							nodestoprint[a]=a.id
						else:
							nodestoprint[a]='arg'#name not known,if constants or could be expr also
					if callNode.func.value.keywords:
						for k in callNode.func.value.keywords:
							nodestoprint[k.value]=k.arg
				else:
					if callNode.keywords:
						for k in callNode.keywords:
							nodestoprint[k.value]=k.arg
					for a in callNode.args:
						if isinstance(a,ast.Name):
							nodestoprint[a]=a.id
						else:
							nodestoprint[a]='arg'#name not known,if constants or could be expr also
					if callNode.keywords:
						for k in callNode.keywords:
							nodestoprint[k.value]=k.arg

						#process parent attributes:
					for a in callNode.func.value.args:
						if isinstance(a,ast.Name):
							nodestoprint[a]=a.id
						else:
							nodestoprint[a]='arg'#name not known,if constants or could be expr also
					if callNode.func.value.keywords:
						for k in callNode.func.value.keywords:
							nodestoprint[k.value]=k.arg
	return nodestoprint

#Assumes this function used for only target function. maps argument nodes and keyword (name:node) dict to arg names and add new nodes of leftover keywords
def map_sig_to_par(argnode, keyword_map):
		pars=signature.split('(')[1].split(')')[0].split(',')
		name_map=dict()#node to name mapping
		to_remove=list()#record args already used in invocation that can later be removed to process left overs to add to tuples
		ctr=0
		for a in argnode:#argnode list would be smaller or equal to pars
			actual=pars[ctr]
			ctr=ctr+1
			if '=' not in actual: # such cases expected to appear before else case
				if not '**' in actual:
					name_map[a]=actual # some actual may be left that could be traversed and added after
			else:
				lhs=actual.split('=')[0].strip()
				if lhs in keyword_map:
					name_map[keyword_map[lhs]]=lhs
				else:#if passed without default assignment but is actually default				
					name_map[a]=lhs
			to_remove.append(actual) # later removed from pars to process left overs
		for k in keyword_map:
			actual=pars[ctr]
			#if '=' in actual:#should hold always- extra check
			name_map[keyword_map[k]]=k#actual.split('=')[0].strip()		
			to_remove.append(actual)
		to_process=[x for x in pars if x not in to_remove]#assumes will all be with =
		
		for i in to_process:#default keywords
			if not '**' in i:
				tmp=i.split('=')
				arg_val=eval(tmp[1].strip())#all vals expected as constant primitives or basic collections
				arg_name=tmp[0].strip()
				#arg_type=str(type(arg_val)).split("'")[1].strip()
				node=nodecreater(arg_val)
				name_map[node]=arg_name

		return name_map

#returns ast node equivalent of value based on its type. Assumes value is a constant of primitive type or collection
def nodecreater(val):
	if isinstance(val,int) or isinstance(val,float):
		return ast.Num(n=val)
	elif isinstance(val,str):
		return ast.Str(s=val)
	elif isinstance(val,bool):
		return ast.NameConstant(value=val)
	elif isinstance(val,list):#need recursive call
		lt=[]
		for i in val:
			lt.append(nodecreator(val))
		return ast.List(elts=lt,ctx=ast.Load())
	elif isinstance(val,dict):
		lk=[]
		lv=[]
		for i in val:
			lk.append(nodecreator(i))
			lv.append(nodecreator(val[i]))
		return ast.Dict(keys=lk, values=lv)
	elif isinstance(val,set):
		lt=[]
		for i in val:
			lt.append(nodecreator(val))
		return ast.Set(elts=lt)
	elif isinstance(val,tuple):
		lt=[]
		for i in val:
			lt.append(nodecreator(val))
		return ast.Tuple(elts=lt,ctx=ast.Load())
	
	elif val==None:
		return ast.NameConstant(value=val)

def merge(dict1, dict2):
	return {**dict1, **dict2}

traverseNode()
