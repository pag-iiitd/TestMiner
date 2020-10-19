import pickle
import random
import sys
import Function
import pandas as pd
import numpy as np
from gensim.models import (Word2Vec, KeyedVectors)
import re
from nltk.stem import PorterStemmer
from gensim.utils import lemmatize
import string
from gensim.corpora import Dictionary
from gensim.models import Word2Vec, WordEmbeddingSimilarityIndex
from gensim.similarities import SoftCosineSimilarity, SparseTermSimilarityMatrix

#compute sparsetermsimilaritymatrix for each cluster, this is a one time exercise to prepare data

lemmatizer = PorterStemmer() 
translator = str.maketrans('', '', string.punctuation)

STOP_WORDS = {'few', 'their', 'then', 'mustn', 'off', "you'll", 'not', 'own',
			  'with', 'out', 'there', 'most', 'shouldn', 'aren', "hasn't",
			  'all', 'his', "weren't", 'each', 'had', 'are', 'up',
			  'very', 'mightn', 'our', "doesn't", 're', 'again', 'who',
			  'yourself', 'but', 'when', 'me', 'while', 'yours', 'haven',
			  'more', 've', 'above', 'shan', 'if', 'was', 'were', 'himself',
			  'theirs', 'didn', "you're", 'other', 'will', 'these', 'hers',
			  'should', 'have', 'some', 'through', "shan't", 'am', 'has',
			  'why', "couldn't", 'this', 'a', 'yourselves', 'during',
			  'nor', 'my', 'won', 'here', "mustn't", 't', 'been',
			  'such', 'after', 'from', 'did', 'does', 'only', 'below', 'just',
			  'ain', 'it', 'ourselves', 'until', 'isn', 'down', "didn't",
			  'hadn', "isn't", 'how', 'herself', 'about', 'do', "needn't",
			  "wouldn't", 'd', 'themselves', 'same', 'weren', 'its', "aren't",
			  'what', "that'll", "wasn't", 'that', 'at', 'couldn', 'against',
			  "it's", 'further', 'doing', "don't", 'him', 'too', 'she',
			  "shouldn't", 'll', 'ma', 'than', 'being', 'no', 'needn',
			  'itself', 'where', 'm', 'wasn', "won't", 'hasn', 'ours',
			  "hadn't", 'before', 'having', "mightn't", 'is', 'which', 'those',
			  'myself', 'he', 'them', 's', "should've", 'an', 'over',
			  'they', "she's", 'whom', 'i', 'y', 'on', 'don', 'etc', '<p>',
			  'you', 'can', "you've", 'o', "haven't", 'into', 'be', 'the',
			  'between', 'so', 'your', 'as', 'wouldn', 'under', 'doesn',
			  'once', 'now', 'we', 'her', 'by', "you'd", 'because', 'any'}


def get_function_explanation(docstring):

	rs = re.findall('(.*?)(Args|args|Usage|usage|Example|<pre>|param|@return|rtype\:|return\:|type\:|throws|\Z)', docstring)[0][0]
	rs = remove_html_tags(drop_special_chars(drop_urls_filepath(drop_example(rs))))
	#print(rs)
	if rs.strip()=='':
		rs=docstring
	return rs


def remove_punctuations(sentence):
	return sentence.translate(translator).strip()


def drop_urls_filepath(sentence):
	return re.sub(r'\S*(\\|/)+\S*','',re.sub(r'http\S+', '', sentence))

def drop_tags(sentence):
	return re.sub('<[^<]+>', "", sentence)


def drop_example(sentence):
	return re.sub(r'(Example|Usage|code:|Code)(.*?)(param|return|\Z)', '', sentence)

def remove_html_tags(sentence):
	return re.sub(r'<.*?>', '', sentence)

def drop_special_chars(sentence):
	return re.sub(r"[^a-zA-Z0-9]+", ' ', sentence)


def lemmatize_doc(doc):
	#print(doc)
	return ' '.join([lemmatizer.stem(word) for word in doc.split()])


def _drop_stop_words(sentence):
	return ' '.join([word for word in sentence.split() if len(word)>1 and word not in STOP_WORDS])

#if hyphen between long words then split words. If text before hyphen of len<=2 then merge with word following  (example e-mail to email)	
def treat_hyphen(sentence):
	sentence=sentence.split()
	sent2=list()
	for word in sentence:
		if '-' in word:
			w=word.split('-')
			
			if len(w[0])<=2:
				w=''.join(w)
			else:
				w=' '.join(w)
			
			sent2.append(w)
		else:
			sent2.append(word)
	return ' '.join(sent2)
	
def get_cleaned_doc(doc, lemmatize=True):
	doc=doc.replace('\n',' ')
	doc=treat_hyphen(doc)
	
	doc = drop_special_chars(drop_urls_filepath(drop_example(drop_tags(get_function_explanation(doc)))))
	cleaned_doc = ' '.join([' '.join(camel_case_split2(word)).lower() for word in doc.split() if len(word)>1 and word not in STOP_WORDS])
	#print(doc)
	
	return lemmatize_doc(cleaned_doc) if lemmatize else cleaned_doc


def get_cleaned_sentences_word_list(docstring):
	cleaned_docs_as_list = []
	if not isinstance(docstring,str):
		#print(type(docstring))
		return None
	doc=get_cleaned_doc(docstring).split()
	if doc:
		return doc
	else:
		return None
		
#takes list of Functions of Function Type	
def get_cleaned_param_desc_list(Funclist):
	cleaned_param_docs = []
	for row in Funclist:
		fn_sig = get_fn_sig_from_code(row.source)
		doc_dict = get_param_docs_dict(row.doc, fn_sig)
		if doc_dict:
			param_docs = [_drop_stop_words(doc).split() for doc in doc_dict.values() if doc]
			if param_docs:
				cleaned_param_docs.append(param_docs[0])
	return cleaned_param_docs
	

def get_params(fn_signature):
	params = fn_signature[fn_signature.find("(")+1:fn_signature.find(")")]
	params = [param.split('=')[0].strip() for param in params.split(',')]
	return [param.split(' ')[-1] if ' ' in param else param for param in params]


def get_cleaned_param_doc(param, docstring):
	docstring = drop_tags(docstring)
	docstring = docstring.replace('@', '.')
	sentences = docstring.split('.')
	for sentence in sentences:
		if ('param' in sentence or ':' in sentence) and param in sentence:
			sentence = sentence[sentence.find(param)+(len(param)):]
#			 sentence = sentence[sentence.find(param):]
			sentence = ' '.join([lemmatizer.stem(' '.join(camel_case_split2(word)).lower()) for word in sentence.split()])
			return remove_punctuations(sentence)
	return ''



def get_cleaned_doc_as_list(doc):

	doc = drop_special_chars(drop_urls_filepath(drop_example(get_function_explanation(doc))))

	return ' '.join([lemmatizer.stem(' '.join(camel_case_split2(word)).lower()) for word in doc.split() if len(word)>1 and word not in STOP_WORDS])

def get_param_docs_dict(sentence, fn_signature):
    params_doc_dict = {}
    fn_signature = str(fn_signature)
    sentence=sentence.replace('\t','\n')
    params_doc = re.findall(r'param (.*)(return:|@return|type|rtype|Example|Usage|.|\Z)', str(sentence))
    if not params_doc:
        params_doc = re.findall(r'Args:(.*)(return:|@return|type|rtype|Example|Usage|.|\Z)', str(sentence))
	#print(fn_signature,params_doc)
    if params_doc and params_doc[0][0]:
        params = get_params(fn_signature)
        for param in params:
            param=param.strip()
            for pdoc in params_doc:
                if param and param in pdoc[0][:25]:
                    params_doc_ = 'param '+ pdoc[0]
                    params_doc_dict[param] =get_cleaned_param_doc(param, params_doc_)
                    break
        #print(params_doc_dict)
        return params_doc_dict

def camel_case_split2(string):
	# set the logic for creating a "break"
	def is_transition(c1, c2):
		if c1.isdigit(): #should split on digit
			return True
		return c1.islower() and c2.isupper()

	# start the builder list with the first character
	# enforce upper case
	bldr = [string[0].upper()]
	for c in string[1:]:
		# get the last character in the last element in the builder
		# note that strings can be addressed just like lists
		previous_character = bldr[-1][-1]
		if is_transition(previous_character, c):
			# start a new element in the list
			bldr.append(c)
		else:
			# append the character to the last string
			bldr[-1] += c
	return bldr

def get_fn_sig_from_code(code):
	for line in code.split('\n'):
		if 'def' in line and '(' in line and ')' in line and ':' in line:
			return line[line.find('def')+3: line.find(':')].strip()
		elif '(' in line and ')' in line and '{' in line:
			s_idx = line[:line.find('(')].rfind(' ')
			return line[s_idx:line.find('{')].strip()
		elif '(' in line and ')' in line and ';' in line:
			s_idx = line[:line.find('(')].rfind(' ')
			return line[s_idx:line.find(';')].strip()
	return None
	

if __name__ == "__main__":	
	model=KeyedVectors.load('w2v_crosslib_120k_skipgram_oov.bin')
	termsim_index = WordEmbeddingSimilarityIndex(model.wv)

	pname='dataset_nlp'
	MapDict=dict()
	themecode='N'
	with open(pname+'_cluster.txt', "rb") as myFile:
		MapDict = pickle.load(myFile)
	for ind in MapDict:
		param_desc_list=get_cleaned_param_desc_list(MapDict[ind])
		docs_list=[]
		origdocs_list=[]
		origfuncs_list=[]
		for func in MapDict[ind]:
			if isinstance(func.doc,str) and len(get_cleaned_doc(func.doc).split())>0:
				origdocs_list.append(func.doc)
				origfuncs_list.append(func.source)#split should have been on sig but stored incorrectly(exchanged) in Function object
				word_list=get_cleaned_sentences_word_list(func.doc)
				if word_list:
					docs_list.append(word_list)
		"""cloneorigdocs_list=list(origdocs_list)
		for i in cloneorigdocs_list:#to make indices in sync with bow
			if not isinstance(i,str) or len(get_cleaned_doc(i).split())==0:
				origdocs_list.remove(i)#############TODO: get index to remove from funclist too"""
				
		docs_list.extend(param_desc_list)
		#print(docs_list)
		dictionary = Dictionary(docs_list)
		bow_corpus = [dictionary.doc2bow(document) for document in docs_list]
		#adds dumps of original doc as well
		with open(themecode+'_'+str(ind)+'_origfunc'+'.pkl', "wb") as myFile:
			pickle.dump(origfuncs_list, myFile)			
		with open(themecode+'_'+str(ind)+'_origdoc'+'.pkl', "wb") as myFile:
			pickle.dump(origdocs_list, myFile)
		with open(themecode+'_'+str(ind)+'_dict'+'.pkl', "wb") as myFile:
			pickle.dump(dictionary, myFile)
		with open(themecode+'_'+str(ind)+'_bow'+'.pkl', "wb") as myFile:
			pickle.dump(bow_corpus, myFile)
		#print('bow_corpus done',ind)
		similarity_matrix = SparseTermSimilarityMatrix(termsim_index, dictionary)  # construct similarity matrix
		#print('sparseterm done',ind)
		with open(themecode+'_'+str(ind)+'_matrix'+'.pkl', "wb") as myFile:
			pickle.dump(similarity_matrix, myFile)

	
	
		
	
