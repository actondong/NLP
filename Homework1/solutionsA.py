from __future__ import division
import math
import nltk 
import string
from string import maketrans 
#a function that calculates unigram, bigram, and trigram probabilities
#brown is a python list of the sentences
#this function outputs three python dictionaries, where the key is a tuple expressing the ngram and the value is the log probability of that ngram
#make sure to return three separate lists: one for each ngram
def calc_probabilities(brown):
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    unigram_t=[]
    bigram_t=[]
    trigram_t=[]
    lenb = len(brown)
    ##calculate unigram_p
    for item in brown:
	    tl = nltk.word_tokenize(item)
	    tl.append("STOP")
	    unigram_t.extend(tl)	
	    bigram_t_temp = ["*"]+tl+["STOP"]
	    bigram_t.extend(tuple(nltk.bigrams(bigram_t_temp)))
	    trigram_t_temp=["*","*"]+tl+["STOP"]
    	    trigram_t.extend(tuple(nltk.trigrams(trigram_t_temp)))
    ##count
    unigram_c = {}
    for item in unigram_t:
	try:
	    unigram_c[(item,)]+= 1
        except:
            unigram_c[(item,)]=1
    
    unigram_c[("*",)]= lenb
    bigram_c={}
    for item in bigram_t:
 	try:
	    bigram_c[item]+= 1
        except:
            bigram_c[item]=1

    bigram_c[("*","*")]= lenb
    trigram_c={}
    for item in trigram_t:
  	try:
	    trigram_c[item]+= 1
        except:
            trigram_c[item]=1

    ulen=len(unigram_t)
    unigram_p = {(item,):math.log(unigram_c[(item,)],2)-math.log(ulen,2) for item in set(unigram_t)}
    bigram_p = {item:math.log(bigram_c[item],2)-math.log(unigram_c[(item[0],)],2) for item in set(bigram_t)}
    trigram_p = {item:math.log(trigram_c[item],2)-math.log(bigram_c[tuple(item[0:2])],2) for item in set(trigram_t)}
    return unigram_p, bigram_p, trigram_p

#each ngram is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams):
    #output probabilities
    outfile = open('A1.txt', 'w')
    for unigram in unigrams:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')
    for bigram in bigrams:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')
    for trigram in trigrams:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')
    outfile.close()
    
#a function that calculates scores for every sentence
#ngram_p is the python dictionary of probabilities
#n is the size of the ngram
#data is the set of sentences to score
#this function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, data):
    scores = [0 for item in data]
    #trantab =  maketrans("","")
    #data = [s.translate(trantab,string.punctuation) for s in data]
    #data = [s+" STOP " for s in data]
    data_tokens = [nltk.word_tokenize(item + " STOP ") for item in data]
    if n == 1:   
	for i,outitem in enumerate(data_tokens):
            for item in outitem:
		if (item,) not in ngram_p:
		    ngram_p[(item,)] = -1000
	        scores[i]+= ngram_p[(item,)]	

    if n == 2: 
        data_tokens2 = [["*"]+ item for item in data_tokens]
	data_bigram_tokens =[tuple(nltk.bigrams(item)) for item in data_tokens2]
	for i,outitem in enumerate(data_bigram_tokens):
            for item in outitem:
		if item not in ngram_p:
   		    ngram_p[item] = -1000
	        scores[i] += ngram_p[item]	
    if n == 3:
	data_tokens3 = [["*","*"] + item for item in data_tokens]
	data_trigram_tokens = [tuple(nltk.trigrams(item)) for item in data_tokens3]
	for i,outitem in enumerate(data_trigram_tokens):
            for item in outitem:
		if item not in ngram_p:
		    ngram_p[item] = -1000
	        scores[i] += ngram_p[item]	
    return scores


#this function outputs the score output of score()
#scores is a python list of scores, and filename is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()


#this function scores brown data with a linearly interpolated model
#each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
#like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, brown):
    scores = []
    lenb = len(brown)
    unigrams[('*',)]= math.log(lenb,2)-math.log(705086,2)
    bigrams[('*','*')] = math.log(lenb,2)-math.log(lenb,2)
    data_tokens = [nltk.word_tokenize(" * * "+ item + " STOP ") for item in brown]
    data_trigram_tokens = [tuple(nltk.trigrams(item)) for item in data_tokens]
	
    for i,outitem in enumerate(data_trigram_tokens):
	scores.append(0)
        for item in outitem:
	    if (item[2],) not in unigrams:
		unigrams[(item[2],)] = -1000		
	    if item[1:3] not in bigrams:
		bigrams[item[1:3]] = -1000
	    if item not in trigrams:
		trigrams[item] = -1000
	    scores[i]= scores[i]+ math.log(1/3,2)+math.log((2**(unigrams[(item[2],)])+2**(bigrams[item[1:3]])+2**(trigrams[item])),2)	
    return scores

def main():
    
    #open data
    infile = open('Brown_train.txt', 'r')
    brown = infile.readlines()
    infile.close()
    #calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(brown)

    #question 1 output
    q1_output(unigrams, bigrams, trigrams)

    #score sentences (question 2)
    uniscores = score(unigrams, 1, brown)
    biscores = score(bigrams, 2, brown)
    triscores = score(trigrams, 3, brown)
    #question 2 output
    score_output(uniscores, 'A2.uni.txt')
    score_output(biscores, 'A2.bi.txt')
    score_output(triscores, 'A2.tri.txt')

    #linear interpolation(question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, brown)

    #question 3 output
    score_output(linearscores, 'A3.txt')

    #open Sample1 and Sample2 (question 5)
    infile = open('Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open('Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    #score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    #question 5 output
    score_output(sample1scores, 'Sample1_scored.txt')
    score_output(sample2scores, 'Sample2_scored.txt')

if __name__ == "__main__": main()
