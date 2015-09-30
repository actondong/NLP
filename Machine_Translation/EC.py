# TODO: (Optional) Improve the BerkeleyAligner.
from __future__ import division
import nltk
import A
from collections import defaultdict
from nltk.corpus import comtrans
from nltk.align import AlignedSent
import math
from sys import maxint

class BetterBerkeleyAligner():
    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    # an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
	new_mots =[None]+ align_sent.mots
	words = align_sent.words
	new_words = [None] + align_sent.words
	l = len(align_sent.mots)
	m = len(words)
	new_align = []
	for i in xrange(0,m+1):
		match = ()
		qt = -maxint
		for j in xrange(0,l+1):
			if(math.log(self.q[(j,i,l,m)]*self.t[(new_mots[j],new_words[i])]) > qt):
				qt = math.log(self.q[(j,i,l,m)]*self.t[(new_mots[j],new_words[i])]) 
				if j == 0 or i == 0:
					continue#do not record (i,null) (null,j) (null,null)cases
				
				else :
				#justify i,j to correspond to right index of the word
					match = (i-1,j-1)
		if match:
			new_align.append(match)		
	
	#print l-1,m-1, new_align, words, new_mots
	new_align_sent = AlignedSent(align_sent.words,align_sent.mots,new_align)
	return new_align_sent 
	    
    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}
	cout_dict = defaultdict(float)
	cout_dict2 = defaultdict(float)#count dict for reverse model
	#In my code below, f(rench) stands for source lan and e(nglish) stands for target lan.
	#For reverse model, f(rench) stands for target and e(nglish) stands for source.
 	#initialize t...
	#First get those counts
	f_obj = defaultdict(list)#key is a french(source) word, value is a list of alignedSent obj.
	for aligned_sent in aligned_sents:
		for word in[None] + aligned_sent.words:
			f_obj[(word)].append(aligned_sent)
	
	e_obj = defaultdict(list)#key is a english(source for reverse model) word, value is a list of alignedSent obj.
	for aligned_sent in aligned_sents:
		for mot in [None] + aligned_sent.mots:
			e_obj[(mot)].append(aligned_sent)
	
	
	#Then, get t	
	for f,obj_list in f_obj.items():
		all_e= []
		for obj in obj_list:
			all_e.extend(obj.mots)
		num_e = len(set(all_e))
		for obj in obj_list:
			for mot in[None]+ obj.mots:
				t[(mot,f)] = (1/(num_e+1))
	t2 ={} 
	#Then, get t for reverse model
	for e,obj_list in e_obj.items():
		all_f= []
		for obj in obj_list:
			all_f.extend(obj.words)
		num_f = len(set(all_f))
		for obj in obj_list:
			for word in [None] + obj.words:
				t2[(word,e)]  = (1/(num_f+1))
#				temp  = 1/(num_f+1)
#				t2[(word,e)] = 0.7*temp + 0.3*t[(e,word)]
#				t[(e,word)] = 0.7*t[(e,word)] + 0.3*temp
#

	#initialize q ...
	for aligned_sent in aligned_sents:
		l = len(aligned_sent.mots)
		m = len(aligned_sent.words)
		for i in xrange(0,m+1):
			for j in xrange(0,l+1):
				q[(j,i,l,m)] = (1/(m+1))
	
	q2 = {}#q parameter for reverse model
	#initialize q ...for the reverse model
	for aligned_sent in aligned_sents:
		l = len(aligned_sent.mots)
		m = len(aligned_sent.words)
		for j in xrange(0,l+1):
			for i in xrange(0,m+1):
				q2[(i,j,m,l)] = (1/(l+1))
		#		temp = 1/(l+1)
		#		q2[(i,j,m,l)] = 0.7*temp + 0.3*q[(j,i,l,m)]
		#		q[(j,i,l,m)] = 0.7*q[(j,i,l,m)] + 0.3*temp
	
	#now EM
	for ite in xrange(num_iters):
		print "ite = " + str(ite)
		for aligned_sent in aligned_sents:
			for i,f in enumerate([None] + aligned_sent.words):
				deno = 0
				m = len(aligned_sent.words)
				new_mots = [None]+aligned_sent.mots#A source word could be matched into a Null
				for j in xrange(len(aligned_sent.mots)+1):
					e = new_mots[j]
					l = len(aligned_sent.mots)
					deno += q[(j,i,l,m,)]*t[(e,f)]#this is the denominator of delta
				for j,e in enumerate(new_mots):
					l = len(aligned_sent.mots)
					delta = q[(j,i,l,m)]*t[(e,f)]/deno#Calculate delta from t and q and use delta to update counts
					if not delta:#this is for debug, delta should never be 0 if q and t are calculated right
						print "Wrong"
					cout_dict[(e,f)] += delta  
					cout_dict[(e)] += delta
					cout_dict[(j,i,l,m)] += delta
					cout_dict[(i,l,m)] += delta
			for i,f in enumerate([None]+aligned_sent.mots):#Train reverse model.For reverse model, e(which is target before) becomes source, f(which is source before) becomes target
				deno = 0
				m = len(aligned_sent.mots)
				new_words = [None]+aligned_sent.words
				for j in xrange(len(aligned_sent.words)+1):	
					e = new_words[j]
					l = len(aligned_sent.words)
					deno += q2[(j,i,l,m)]*t2[(e,f)]
				for j,e in enumerate(new_words):
					l = len(aligned_sent.words)
					delta = q2[(j,i,l,m)]*t2[(e,f)]/deno#Calculate delta from t and q and use delta to update counts
					if not delta:
						print "wrong"
					cout_dict2[(e,f)] += delta
				#	cout_dict2[(e,f)] =(cout_dict2[(e,f)] + cout_dict[(f,e)])/2#average count
					cout_dict2[(e,f)] = math.sqrt(cout_dict2[(e,f)]*cout_dict[(f,e)])#average count
					cout_dict[(f,e)] = cout_dict2[(e,f)]
					cout_dict2[(e)] += delta
					cout_dict2[(j,i,l,m)] += delta
					#cout_dict2[(j,i,l,m)] = (cout_dict2[(j,i,l,m)] + cout_dict[(i,j,m,l)])/2#average count
					cout_dict2[(j,i,l,m)] = math.sqrt(cout_dict2[(j,i,l,m)]*cout_dict[(i,j,m,l)])#average count
					cout_dict[(i,j,m,l)] = cout_dict2[(j,i,l,m)]
					cout_dict2[(i,l,m)] += delta

		#Recalculate t,q parameters after updating counts
		for t_key in t.keys():
			t[t_key] = cout_dict[t_key]/cout_dict[t_key[0]]
		for t_key in t2.keys():
			t2[t_key] = cout_dict2[t_key]/cout_dict2[t_key[0]]
		for q_key in q.keys():
			q[q_key] = cout_dict[q_key]/cout_dict[q_key[1:]]
		for q_key in q2.keys():
			q2[q_key] = cout_dict2[q_key]/cout_dict2[q_key[1:]]
        return (t,q)
def main(aligned_sents):
    ba = BetterBerkeleyAligner(aligned_sents, 30)
    if ba.t is None:
        print "Better Berkeley Aligner Not Implemented"
    else:
        avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

        print ('Better Berkeley Aligner')
        print ('---------------------------')
        print('Average AER: {0:.3f}\n'.format(avg_aer))

if __name__ == "__main__":
    aligned_sents = comtrans.aligned_sents()[:350]
    main(aligned_sents)
#    ba = BerkeleyAligner(aligned_sents, 20)
#    A.save_model_output(aligned_sents,ba,"ba.txt")
#    avg_aer = A.compute_avg_aer(aligned_sents,ba,50)
#    print ('Berkeley Aligner')
#    print ('---------------------------')
#    print('Average AER: {0:.3f}\n'.format(avg_aer))
#
