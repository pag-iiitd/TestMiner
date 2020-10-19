import ast,copy,astunparse

"""#fname="InsertionTest_sample.py"
fname="unittestSample_adv2.py"
with open(fname,'r') as f:
	tree=ast.parse(f.read())
	#print(ast.dump(tree))

funcname='wrap'
signature='wrap(text, width=70)'
"""


#get functiondef node to functionname mapping in a file
def getAllFunctions(tree, funcname, signature):
	func_map=dict()#maps func name to funcdef node
	target_users=list()#lists all functions that directly call target function-use as src to connect to 
	for nd in ast.walk(tree):
		if isinstance(nd,ast.FunctionDef):
			func_map[nd.name]=nd
			for n in ast.walk(nd):
				if isinstance(n, ast.Call):
					#check if call is on target then update target_users
					if isinstance(n.func, ast.Name) and n.func.id==funcname:
						target_users.append(nd)
					elif isinstance(n.func, ast.Attribute) and n.func.attr==funcname:
						target_users.append(nd)

	return (func_map,target_users)

#traverse all funcDef nodes to populate adj_list based on func_map obtained
def prepare_adj_list(tree, funcname, signature):
	adj_list=dict()#maps funcdef node to list of functions from file being invoked inside it
	(func_map, target_users)=getAllFunctions(tree, funcname, signature)
	for nd in ast.walk(tree):
		if isinstance(nd,ast.FunctionDef):
			adj_list[nd]=list()
			for n in ast.walk(nd):
				if isinstance(n, ast.Call):
					#check if call is on one of the functions then add to list
					if isinstance(n.func, ast.Name) and n.func.id in func_map:
						adj_list[nd].append(func_map[n.func.id])
					elif isinstance(n.func, ast.Attribute) and n.func.attr in func_map:
						adj_list[nd].append(func_map[n.func.attr])
	return (func_map, target_users, adj_list)			


#TODO: for given target function-fetch target users as srces and run bfs- treating undirected.Use queue. Populate get_funcs pass
def getRelFunctions(tree, funcname, signature):
	get_funcs=set()#get list of all relevant functions for a given target
	(func_map, target_users, adj_list)=prepare_adj_list(tree, funcname, signature)
	q1=list(target_users)#used to run bfs- fetch downward
	q2=list(target_users)#used to run bfs- fetch upward
	for f in target_users:#all possible sources
		#have 2 queues- one to mark functions that have target_user in adj list-move upwards, other to fetch all functions adj to target_user- move downwards 
		get_funcs.add(f)

	while len(q1)>0:
		val=q1[0]
		q1.remove(q1[0])
		for n in adj_list[val]:
			if n not in get_funcs:
				get_funcs.add(n)
			if n not in q1 and n not in get_funcs:	
				q1.append(n)

	while len(q2)>0:
		val=q2[0]
		q2.remove(q2[0])
		for k in adj_list:
			if val in adj_list[k] and k not in q2 and k not in get_funcs:
				get_funcs.add(k)
				q2.append(k)
	return get_funcs

#for i in getRelFunctions('wrap','wrap(text, width=70)'):
#	print(i.name)
