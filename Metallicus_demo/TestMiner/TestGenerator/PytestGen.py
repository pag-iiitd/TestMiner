import ast
import astunparse
#For given list of assertion inputs and expected value, 
#parses the template and inserts values in pytest args

"""
Module(body=[Import(names=[alias(name='pytest', asname=None)]),
 FunctionDef(name='test_ipaddress', args=arguments(args=[arg(arg='string', annotation=None),
 arg(arg='op', annotation=None)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
 body=[Assert(test=Compare(left=Call(func=Name(id='is_ip', ctx=Load()), 
 args=[Name(id='string', ctx=Load())], keywords=[]), ops=[Eq()], 
 comparators=[Name(id='op', ctx=Load())]), msg=None)], 
 decorator_list=[Call(func=Attribute(value=Attribute(value=Name(id='pytest', ctx=Load()), 
 attr='mark', ctx=Load()), attr='parametrize', ctx=Load()), 
 args=[Str(s='string,op'), 
 List(elts=[Tuple(elts=[Str(s='127.0.0.1'), NameConstant(value=True)], ctx=Load()), 
 Tuple(elts=[Str(s='23::56:1235::22'), NameConstant(value=False)], ctx=Load())], ctx=Load())], 
 keywords=[])], returns=None)])
"""
	
def genpythontest(testlist_forgen,templatefp):
	with open(templatefp,'r',encoding='utf-8') as f:
		tree=ast.parse(f.read())
		#print(ast.dump(tree))
		f.close()
	tuple_nodes=list()
	#iterate testlist value and call prepare node store in list
	for test in testlist_forgen:
		tuple_nodes.append(prepareNode(test))
	for nd in ast.walk(tree):
		if isinstance(nd,ast.FunctionDef):
			for n in nd.decorator_list:
				if isinstance(n,ast.Call) and isinstance(n.args[1],ast.List):
					list_where_add=n.args[1].elts
					for test_tup in tuple_nodes:
						list_where_add.append(test_tup)
	with open(templatefp, 'w',encoding='utf-8') as f:
		f.write(astunparse.unparse(tree))
		f.close()

	#traverse ast to args of call node of decorator_list, where list of nodes could be inserted. Pick List type node and insert to it one by one
		
"""prepare ast node for the given vals to be inserted to assert stmt with pytest arg, 
requires type info too can infer from value support list of vals for multiple args too.
First val in arg_vals is the expected output.
Returns a Tuple node with elements as args as per order and epected value node at the end"""
def prepareNode(arg_vals):
	tmplist=list()
	#print(arg_vals[0], type(arg_vals[0]))
	exp_op=getType(arg_vals[0])
	
	for arg in arg_vals[1:]:
		tmplist.append(getType(str(arg)))
	tmplist.append(exp_op)
	return ast.Tuple(elts=tmplist, ctx=ast.Load)

#infer python type from value and return its ast node
#support: ast.Num, ast.Str, ast.Bytes, tuple, list, Nameconstant(boolean, None), dict, set
def getType(value):
	value=value.encode('ascii','backslashreplace').decode('ascii','backslashreplace')
	if value.startswith("\"") and value.endswith("\""):
		#value="\""+value[1:-1].replace('"','\"')+"\""
		#value= repr(str(value))#.encode('ascii','backslashreplace').decode('ascii')))
		value2=value.encode("unicode_escape").decode("utf-8")
		value2=value2[1:-1].replace('"','\\"')
		
		#value=repr(value)
		if isinstance(eval(repr(value2)),str):
			#print(value,eval(repr(value2)))
			value=value.replace('\n','\\n')
			value=value.replace('\r','\\r')
			value=value.replace('\f','\\f')
			value=value.replace('\u0000','null')
						
			value=eval(value)
			value=value.replace('null','\u0000')
			
			#print(value)
			return ast.Str(s=value)#[1:len(value)-1])
	try:
		if value=='True':
			return ast.NameConstant(value=True)
		elif value=='False':
			return ast.NameConstant(value=False)
		elif value=='None':
			return ast.NameConstant(value=None)
		elif isinstance(eval(value), int) or isinstance(eval(value),float):
			return ast.Num(n=eval(value))
		elif isinstance(eval(value),bytes):
			return ast.Bytes(eval(value))
		elif isinstance(eval(value), list):
			tmplist=list()
			for v in eval(value):
				tmplist.append(getType(str(v)))
			return ast.List(elts=tmplist, ctx=ast.Load)
		elif isinstance(eval(value),dict):
			keylist=list()
			vallist=list()
			dc=eval(value)
			for k in dc:
				keylist.append(getType(str(k)))
				vallist.append(getType(str(dc[k])))
				
			return ast.Dict(keys=keylist,values=vallist) 
		elif isinstance(eval(value),set):
			tmplist=list()
			for v in eval(value):
				tmplist.append(getType(str(v)))
			return ast.Set(elts=tmplist)
		elif isinstance(eval(value),tuple):
			tmplist=list()
			for v in eval(value):
				tmplist.append(getType(str(v)))
			return ast.Tuple(elts=tmplist, ctx=ast.Load)
		else:#default as string form
			return ast.Str(s=value)
	except:
		return ast.Str(s=value)
