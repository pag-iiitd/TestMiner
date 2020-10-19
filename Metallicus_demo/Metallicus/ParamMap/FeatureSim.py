import nltk
import textdistance
import re
#compute similarity score for given pair of string or numeral based on dynamic features
class FeatureSimilarity():
	#takes two lists each of form [type,[len,lentype],abstype]
	def __init__(self,case1, case2):
		self.case1=case1
		self.case2=case2


	def getsimilarity(self):
		if self.case1==None or self.case2==None:
			return 0
		else:
			sim=0
			#for numeric
			if (self.case1[0]=='' and self.case1[2]=='') or (self.case2[0]=='' and self.case2[2]==''):
				#len to lentype to be given 20:80 wt
				if self.case1[1][0]==self.case2[1][0]:
					sim=sim+0.2
				if self.case1[1][1]==self.case2[1][1]:#same lentype- likely if prev condition holds
					sim=sim+0.8
			else:#for string
				if self.case1[0]==self.case2[0]:
					sim=sim+1/3
				if self.case1[1][0]==self.case2[1][0]:
					sim=sim+1/3
				elif self.case1[1][1]==self.case2[1][1]:#same lentype
					sim=sim+0.8/3
				sim=sim+(self.edit_dist_sim(self.case1[2],self.case2[2]))/3
			return sim

	#variant of above treating every sub feature as separate, hence returns a list of 3 scores (chartype,len,struct), instead of equal weight combo       
	def getsimilarity_sep(self):
		score_list=list()        
		if self.case1==None or self.case2==None:
			return [0,0,0]
		else:
			sim=0
			#for numeric
			if (self.case1[0]=='' and self.case1[2]=='') or (self.case2[0]=='' and self.case2[2]==''):
				#len to lentype to be given 20:80 wt
				if self.case1[1][0]==self.case2[1][0]:
					sim=sim+0.2
				if self.case1[1][1]==self.case2[1][1]:#same lentype- likely if prev condition holds
					sim=sim+0.8
				score_list.extend([0,sim,0])
			else:#for string
				if self.case1[0]==self.case2[0]:
					score_list.append(1)
				else:
					score_list.append(0)                    
				if self.case1[1][0]==self.case2[1][0]:#should be given wt for exact lens
					score_list.append(1)
				elif self.case1[1][1]==self.case2[1][1]:#same lentype
					score_list.append(0.8)
				else:
					score_list.append(0)                
				#score_list.append(textdistance.levenshtein.normalized_similarity(self.case1[2],self.case2[2]))
				score_list.append(self.edit_dist_sim(self.case1[2],self.case2[2]))
            
			return score_list
			
	def edit_dist_sim(self,str1,str2):
		if str1.startswith("\"") and str1.endswith("\""):
			str1=str1[1:-1]#remove leading and trailing double quotes
			
		if str2.startswith("\"") and str2.endswith("\""):
			str2=str2[1:-1]#remove leading and trailing double quotes
		
		ed=nltk.edit_distance(str1,str2)
		normalized_dist=ed/max(len(str1),len(str2))
		if normalized_dist>0.85: # most characters changed so higher penalty to scale
			normalized_dist=2*normalized_dist
		sim=1/(1+normalized_dist)
		set1=set()
		set2=set()
		for i in str1:
			if not re.match('[0-9]',i) and not re.match('[a-zA-Z\'"]',i):
				set1.add(i)
		for j in str2:
			if not re.match('[0-9]',j) and not re.match('[a-zA-Z\'"]',j):
				set2.add(j)
		if max(len(set1),len(set2))>0:
			spl_char_score=len(set1.intersection(set2))/max(len(set1),len(set2))#capture overlap in spl char
		else: #no spl char
			return sim
		#print('edit score:',sim)
		if ' ' in set1.intersection(set2) or '\n' in set1.intersection(set2) or '\t' in set1.intersection(set2):#for unstructured (potentially natural language) give a match preference
			return 0.6*sim+0.2*spl_char_score+0.2
		return 0.7*sim+0.3*spl_char_score
