from gensim.models import KeyedVectors
from src.clean_documentation import (get_function_explanation, drop_urls, drop_example, drop_special_chars)
from src.train_embeddings import STOP_WORDS
import os
path_sep=os.path.sep
MODEL_PATH = 'models'+path_sep+'w2v_crosslib.bin'

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
# Load vectors directly from the file
model = KeyedVectors.load(MODEL_PATH)
print('Number of tokens '+str(len(model.vocab)))
print(model.similarity('string', 'str'))

docs=['Adds a new entry to the compressed archive, takes care of duplicates as well','Helper function to zip up a file into an open zip archive']

#docs=['1 - Connect to the FTP server. 2 - Log in with user name and password','Connects to ftp server']


#docs=['Detect the blob\'s language using the Google Translate API. Requires an internet connection','Checks if the language is supported']

#docs=['Convert a snake case string into a case one. (The original string is returned if is not a valid snake case string)','Splits a String by Character type as returned by Groups of contiguous characters of the same type are returned as complete tokens, with the following exception the character of type code Character.UPPERCASE_LETTER}, if any, immediately      preceding a token of type {code Character.LOWERCASE_LETTER}      will belong to the following token rather than to the preceding, if any,      {code Character.UPPERCASE_LETTER} token.']


#docs=['Return a list of tokens, using this blob\'s tokenizer object (defaults to :class:`WordTokenizer <text.blob.tokenizer.WordTokenizer>`).','Constructs a new TokenizerFactory that Word objects and treats carriage as normal whitespace. THIS METHOD IS INVOKED BY REFLECTION BY SOME OF THE JAVA NLP CODE TO LOAD A TOKENIZER FACTORY. IT SHOULD BE PRESENT IN A TokenizerFactory. @return A TokenizerFactory that returns Word objects']

cleaned_docs_as_list=[]

for docstring in docs:
	cleaned_doc = drop_special_chars(drop_urls(drop_example(get_function_explanation(docstring))))
	cleaned_doc = cleaned_doc.lower()
	cleaned_docs_as_list.append(unique_list([word for word in cleaned_doc.lower().split() if word not in STOP_WORDS]))
	cleaned_docs_list = [doc for doc in cleaned_docs_as_list if doc]

if len(cleaned_docs_list[0])>len(cleaned_docs_list[1]): # take longer text on outer loop later
	sl=cleaned_docs_list[0]
	ss=cleaned_docs_list[1]
else:
	sl=cleaned_docs_list[1]
	ss=cleaned_docs_list[0]
total_score=0
mappings=[]
for w1 in sl:
	maxval=0
	maxpair=()	
	for w2 in ss:
		sim=model.similarity(w1,w2)
		if(sim)>=maxval:
			maxval=sim
			maxpair=(w1,w2)

	total_score+=maxval
	mappings.append((maxval,maxpair))

print(cleaned_docs_list)
print(mappings)
print(total_score/len(sl))




