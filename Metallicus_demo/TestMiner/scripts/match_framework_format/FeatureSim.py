import nltk
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

	def edit_dist_sim(self,str1,str2):
		ed=nltk.edit_distance(str1,str2)
		normalized_dist=ed/max(len(str1),len(str2))
		if normalized_dist>0.85: # most characters changed so higher penalty to scale
			normalized_dist=1.5*normalized_dist
		sim=1/(1+normalized_dist)
		#print('edit score:',sim)
		return sim
