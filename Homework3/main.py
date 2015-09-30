from __future__ import division
import nltk
import math
from sklearn import neighbors
from sklearn import svm
from xml.dom import minidom
import json
import codecs
import unicodedata
import sys
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
###NOTICE###
###During this proj, many methods are tried, and commented out because they finally don't contribute to best result####

def finalFeatureTrain(train_file,lan):
	xmldoc = minidom.parse(train_file)
	lex_knn = {}#return dict
	lex_clf = {}#return dict
	lex_unionSet = {}#return dict, this return of unionSet for lexelt will be used in many other functions asking for union set info when testing or calculating relevent scores.
	lex_list = xmldoc.getElementsByTagName('lexelt')
	for lex_node in lex_list:
		clf = svm.LinearSVC()#svm clf
		knn = neighbors.KNeighborsClassifier()#knn clf	
		lexelt = lex_node.getAttribute('item')
		instance_list = lex_node.getElementsByTagName('instance')	
		S,senseid_list = passInstanceList(lan,instance_list,3)
	#Now have processed all instances for a lexelt, we can train the clf now
		union_list = []
		for s in S:
			union_list = list(set(union_list)|set(s))
		#compute comtext vector
		#union_list = synUnion(union_list)
		contxtV = []#a list of lists of contxt vector[contxtv] for each instance
		for s in S:
			contxtv = []
			k=3
			for i in union_list:
				lv = [0]*k*2#location vector
				if i in s:
					index = s.index(i)
					lv[index] = 1
				contxtv.extend(lv)
			contxtV.append(contxtv)
		clf.fit(contxtV,senseid_list)
		knn.fit(contxtV,senseid_list)
		lex_clf[lexelt] = clf
		lex_knn[lexelt] = knn
		lex_unionSet[lexelt] = union_list
	return (lex_clf,lex_knn,lex_unionSet)#both svm and knn is trained, though only report the better one which is svm

def getWordIndex(lan,token_vec,word):#the word index returned by this function will be used to extract context vector of size 2 * window size k.
	word_index = None#In case a instance failed to extract its target word because of bad-format, this will return None
	if lan != 'english':
		try :
			word_index=token_vec.index(word)
		except:
			for i,t in enumerate(token_vec):
				if word in t[0:-1] or word in t[1:] or word in t[2:0] or word in t[0:-2]:#Nocitce for Catalan, say target ' tw ', could be wrapped into form like ' l'tw ' or' tw. '' or ' tw,' and so on. 
					word_index = i
					break
	else:
		word_index = token_vec.index(word)
	return word_index				

def passInstanceList(lan,instance_list,k):# this function is used pass the list of instances for one lexelt
	senseid_list = []#target list for the lexelt 
	S = []#a list of lists of context token within k-distance
	for instance_node in instance_list:
		instance_id = instance_node.getAttribute('id')
		answer = instance_node.getElementsByTagName('answer')[0]
		senseid = answer.getAttribute('senseid')
		senseid = senseid.encode('ascii','ignore')
		#if senseid == 'U':#ignore Unknown case
		#	continue
		context_node = instance_node.getElementsByTagName('context')[0]
		if lan != 'english':
			context_node = context_node.getElementsByTagName('target')[0]
		word_node = context_node.getElementsByTagName('head')
		word = word_node[0].firstChild.nodeValue
		context = (context_node.childNodes[0].nodeValue + context_node.childNodes[1].firstChild.nodeValue + context_node.childNodes[2].nodeValue).replace('\n', '')
		token_vec = context.split(' ')
#		token_vec =rmStop_stem(token_vec,lan,rmStopWords= False) #This three line control whether or not stemming and removing stopwords 
#		stemmer=PorterStemmer()
#		word=stemmer.stem(word)#also stem the target word before locate it in the after-stemming

		word_index = getWordIndex(lan,token_vec,word)
		try:
			s = token_vec[word_index-k:word_index]#s has tokens within k-distance of lexelt[word]
		except:
			continue #in case, word_index never defined in previous precedure, this instance will be skipped
		s.extend(token_vec[word_index+1:word_index+k+1])
		S.append(s)
		senseid_list.append(senseid)#Thus always have same number of labels and objects.
	return S,senseid_list	

def finalFeatureTest(dev_file,lex_clf,lex_knn,lex_featureDict,output,lan,k):#This function the test function of using final best feature
	outfile = codecs.open(output, encoding = 'utf-8', mode = 'w')#though svm, knn both passed in, I will only report svm since it is always the better one
	xmldoc = minidom.parse(dev_file)
	lex_list = xmldoc.getElementsByTagName('lexelt')
	for lex_node in lex_list:
		lexelt = lex_node.getAttribute('item')
		clf = lex_clf[lexelt]#get svm clf for the lexelt
		knn = lex_knn[lexelt]#get knn clf
		feature_list = lex_featureDict[lexelt]#get the union set for the lex
		instance_list = lex_node.getElementsByTagName('instance')
		for instance_node in instance_list:
			context_node = instance_node.getElementsByTagName('context')[0]
			instance_id = instance_node.getAttribute('id')
			if lan != 'english':
				context_node = context_node.getElementsByTagName('target')[0]
			word_node = context_node.getElementsByTagName('head')
			word = word_node[0].firstChild.nodeValue
			context = (context_node.childNodes[0].nodeValue + context_node.childNodes[1].firstChild.nodeValue + context_node.childNodes[2].nodeValue).replace('\n', '')
			token_vec = context.split(' ')
#			token_vec = rmStop_stem(token_vec,lan,rmStopWords=False)
#			stemmer=SnowballStemmer(lan)
#			word=stemmer.stem(word)	
			word_index = getWordIndex(lan,token_vec,word)
			try:
				s = token_vec[word_index-3:word_index]#s has tokens with k-distance of lexelt[word]
			except :
				continue
			s.extend(token_vec[word_index+1:word_index+4])
			contxtv = []
			for i in feature_list:
				lv = [0]*6
				if i in s:
					index = s.index(i)
					lv[index]=1
				contxtv.extend(lv)
			sid_pred = clf.predict(contxtv)
			outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid_pred + '\n'))
	outfile.close()


def rmStop_stem(context_v,lan,rmStopWords = True):#this function will do stemming and/or removing stopwords
	lan = lan.lower()
	stemmer=PorterStemmer()
	if not rmStopWords:
		ans = [stemmer.stem(w) for w in context_v]
	else:
		try:
			stopWords = nltk.corpus.stopwords.words(lan)
			ans = [stemmer.stem(w) for w in context_v if w not in stopWords]
		except :
			ans=  [stemmer.stem(w) for w in context_v] 
			print "lan not supported by nltk.corpus.stopwords"
	
	return ans

def synUnion(union):#this function will expand the union to have synonymous words
	synlist=[]
	for word in union:
		synlist.extend([synset.name().split('.')[0] for synset in wn.synsets(word) ])
	union.extend(set(synlist))
	return union


def lex_train(train_file):#this is a generally training function for step 4, which will combine different features and train and compare results. This doesn't implement relevant score, which is implemented in topRelFeature function.  This doesn't have implementation of the best feature design, which is implemented in previous finalFeatureTrain and finalFeatureTest
	xmldoc = minidom.parse(train_file)
	lex_clf = {}#return dict
	lex_knn = {}#return dict
	lex_unionSet = {}#return dict, this return of unionSet for lexelt will be used in many other functions asking for union set info when testing or calculating relevent scores.
	lex_list = xmldoc.getElementsByTagName('lexelt')
	for lex_node in lex_list:
		clf = svm.LinearSVC(C=100.)#svm clf
		knn = neighbors.KNeighborsClassifier()#knn clf
		lexelt = lex_node.getAttribute('item')
		instance_list = lex_node.getElementsByTagName('instance')
		S,senseid_list = passInstanceList(lan,instance_list,3)
		union_list = []
		for s in S:
			union_list = list(set(union_list)|set(s))
		#compute context vector
#		union_list = synUnion(union_list)#this controls whether or not to extend union list to include syn words
		contxtV = []#a list of lists of contxt vector[contxtv] for each instance
		for s in S:
			contxtv = []
			for i in union_list:
				contxtv.append(s.count(i))
			contxtV.append(contxtv)
		clf.fit(contxtV,senseid_list)
		knn.fit(contxtV,senseid_list)
		lex_clf[lexelt] = clf
		lex_knn[lexelt] = knn
		lex_unionSet[lexelt] = union_list
	return (lex_clf ,lex_knn ,lex_unionSet)


def lex_test(dev_file,lex_clf,lex_knn,lex_featureDict,lan,k):
 	outfile = codecs.open(lan + '.svmpred', encoding = 'utf-8', mode = 'w')
 	outfile2 = codecs.open(lan + '.knnpred', encoding = 'utf-8', mode = 'w')
 	xmldoc = minidom.parse(dev_file)
 	lex_list = xmldoc.getElementsByTagName('lexelt')
 	for lex_node in lex_list:
 		lexelt = lex_node.getAttribute('item')
 		clf = lex_clf[lexelt]#get svm clf for the lexelt
 		knn = lex_knn[lexelt]#get knn clf
 		feature_list = lex_featureDict[lexelt]#get the union set for the lex
 		instance_list = lex_node.getElementsByTagName('instance')
 		for instance_node in instance_list:
 			context_node = instance_node.getElementsByTagName('context')[0]
 			instance_id = instance_node.getAttribute('id')
 			word_node = context_node.getElementsByTagName('head')
 			if lan != 'english':
 				context_node = context_node.getElementsByTagName('target')[0]
 			word_node = context_node.getElementsByTagName('head')
 			word = word_node[0].firstChild.nodeValue
 			context = (context_node.childNodes[0].nodeValue + context_node.childNodes[1].firstChild.nodeValue + context_node.childNodes[2].nodeValue).replace('\n', '')
			token_vec = context.split(' ')
#			token_vec = rmStop_stem(token_vec,lan,rmStopWords = False)
#			stemmer=PorterStemmer()
# 			word=stemmer.stem(word)	

			word_index = getWordIndex(lan,token_vec,word)
			s = token_vec[word_index-k:word_index]#s is s_i, it has tokens with k-distance of lexelt[word]
 			s.extend(token_vec[word_index+1:word_index+k+1])
 			contxtv = []
 			for i in feature_list:
 				contxtv.append(s.count(i))
 			sid_pred = clf.predict(contxtv)
 			outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid_pred + '\n'))
 			sid_pred2 = knn.predict(contxtv)
 			outfile2.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid_pred2 + '\n'))
 	outfile.close()
 	outfile2.close()
 

def replace_accented(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print 'Usage: python main.py [PATHTOTRAINFILE][PATHTOTESTFILE][lan.answer][language]'
		sys.exit(0)
	train = sys.argv[1]
	test = sys.argv[2]
	lan = sys.argv[4]
	output = sys.argv[3]
	lan = lan.lower()
	lex_clf,lex_knn,lex_unionSet  = finalFeatureTrain(train,lan)
	finalFeatureTest(test,lex_clf,lex_knn,lex_unionSet,output,lan,3)
#	lex_clf, lex_knn,lex_unionSet = lex_train(train)
#	lex_test(test,lex_clf,lex_knn,lex_unionSet,lan,3)


# topRelFeature function extract top features based on relevent score. Itself and its train  funciton are all commented out, because of not useful in final feature implementation. skip it. Below are only for verification of implementaion. Notice, when written those functions, I didn't have it facorized into small functionalities. So it is long and bad design


# def topRelFeature(train_file,lex_unionSet):#input is the lexelt -- unionSet dict 
#	xmldoc = minidom.parse(train_file)
#	lex_dict = {}#a dict whose key is lexelt  and value is senseId_dict
#	ReleventFeatureDict = defaultdict(list)#return dict of lexelt --- top features union list
#	lex_list = xmldoc.getElementsByTagName('lexelt')
#	for lex_node in lex_list:
#		senseId_dict = defaultdict(list)#a dict whose key is senseId and value is a list of context for that senseId
#		lexelt = lex_node.getAttribute('item')
#		instance_list = lex_node.getElementsByTagName('instance')
#		senseid_list = []
#		for instance_node in instance_list:
#			instance_id = instance_node.getAttribute('id')
#			answer = instance_node.getElementsByTagName('answer')[0]
#			senseid = answer.getAttribute('senseid')
#			senseid = senseid.encode('ascii','ignore')
#			#if senseid == 'U':#ignore Unknown case
#			#	continue
#			senseid_list.append(senseid)
#			context_node = instance_node.getElementsByTagName('context')[0]
#			word_node = context_node.getElementsByTagName('head')
#			word = word_node[0].firstChild.nodeValue
#			context = (context_node.childNodes[0].nodeValue + context_node.childNodes[1].firstChild.nodeValue + context_node.childNodes[2].nodeValue).replace('\n', '')
#			token_vec = context.split(' ')
#			senseId_dict[senseid].append(token_vec)
#		lex_dict[lexelt] = senseId_dict
#	#calculate relevance scores to a senseId to get top features
#		union = lex_unionSet[lexelt]
#		Nc=defaultdict(int)#a dict : key = word, value = number of occurrences in all instances for the lexe
#		NSc=defaultdict(int)#a dict: key = word, value = number of occurrences in all instances under a specific senseid
#		sId_feature_dict=defaultdict(list)
#		union_top_feature = []
#		for u in union:
#			for txt_l in senseId_dict.values():
#				for txt in txt_l:
#					if u in txt:
#						Nc[u]+=1
#		for sId,txt_l in senseId_dict.items():
#			sid_rscore={}
#			for u in union:
#				for txt in txt_l:
#					if u in txt:
#						NSc[u]+=1
#				try:
#					sid_rscore[u] = (NSc[u]/Nc[u])/(1-NSc[u]/Nc[u])
#				except:
#					sid_rscore[u] = 10000 
#			w_score_l = sid_rscore.items()#a list of (word,score)tuples
#			w_score_l_sorted = sorted(w_score_l,key = lambda item:item[1],reverse=True)
#			sId_top_feature = [w for w,s in w_score_l_sorted]
#			sId_feature_dict[sId] = sId_top_feature
#			union_top_feature=list(set(sId_top_feature)|set(union_top_feature))
#		ReleventFeatureDict[lexelt]=union_top_feature	
#	return ReleventFeatureDict
#

#def lex_train_top_relevent(train_file,ReleventFeatureDict):
# 	xmldoc = minidom.parse(train_file)
# 	lex_clf = {}#return dict
# 	lex_knn = {}#return dict
# 	lex_list = xmldoc.getElementsByTagName('lexelt')
#	for lex_node in lex_list:
# 		clf = svm.LinearSVC()#svm clf
# 		knn = neighbors.KNeighborsClassifier()#knn clf
## 		senseid_list = []#target list for the lexelt 
## 		S = []#a list of lists of context token within k-distance
# 		lexelt = lex_node.getAttribute('item')
# 		instance_list = lex_node.getElementsByTagName('instance')
#		S,senseid_list = passInstanceList(lan,instance_list,10)	
#		
## 		for instance_node in instance_list:
## 			instance_id = instance_node.getAttribute('id')
## 			answer = instance_node.getElementsByTagName('answer')[0]
## 			senseid = answer.getAttribute('senseid')
## 			senseid = senseid.encode('ascii','ignore')
## 			if senseid == 'U':#ignore Unknown case
## 				continue
## 			senseid_list.append(senseid)
## 			context_node = instance_node.getElementsByTagName('context')[0]
## 			word_node = context_node.getElementsByTagName('head')
## 			word = word_node[0].firstChild.nodeValue
## 			context = (context_node.childNodes[0].nodeValue + context_node.childNodes[1].firstChild.nodeValue + context_node.childNodes[2].nodeValue).replace('\n', '')
## 			token_vec = context.split(' ')
## 			token_vec =rmStop_stem(token_vec)#remove stop words and stem
## 			stemmer=nltk.stem.snowball.EnglishStemmer()
## 			word=stemmer.stem(word)
## 			word_index = token_vec.index(word)
## 			s = token_vec[word_index-3:word_index]#s is s_i, it has tokens with k-distance of lexelt[word]
## 			s.extend(token_vec[word_index+1:word_index+4])
## 			S.append(s)
## 		#Now have processed all instances for a lexelt, we can train the clf now
## 		#compute comtext vector
# 		contxtV = []#a list of lists of contxt vector[contxtv] for each instance
# 		for s in S:
# 			contxtv = []
# 			for i in ReleventFeatureDict[lexelt] :
# 				contxtv.append(s.count(i))
# #				if i in s:
## 					contxtv.append(1)
# #				else:
# #					contxtv.append(0)
# 			contxtV.append(contxtv)
# 		clf.fit(contxtV,senseid_list)
# 		try:
# 			knn.fit(contxtV,senseid_list)
# 		except:
# 			pass
# 		lex_clf[lexelt] = clf
# 		lex_knn[lexelt] = knn
# 	return (lex_clf ,lex_knn)
 	


