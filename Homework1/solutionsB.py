import sys
import nltk
import math
from nltk.corpus import brown as brown2
#this function takes the words from the training data and returns a python list of all of the words that occur more than 5 times
#wbrown is a python list where every element is a python list of the words of a particular sentence
def calc_known(wbrown):
    knownwords = []
    wbrown_c={}#a dict of count of each term in wbrown
    for outitem in wbrown:
	for item in outitem:    
	    try:
	        wbrown_c[item]+=1
	    except:
	        wbrown_c[item]=1
    for outitem in wbrown:
	for item in outitem:
	    if wbrown_c[item]>5:
		knownwords.append(item)
    return knownwords

#this function takes a set of sentences and a set of words that should not be marked '_RARE_'
#brown is a python list where every element is a python list of the words of a particular sentence
#and outputs a version of the set of sentences with rare words marked '_RARE_'
def replace_rare(brown, knownwords):
    rare = []
    knownwords_c={}#dict of count of each item in knownwords
    for item in set(knownwords):
	knownwords_c[item]=1
    for outitem in brown:
	rare_temp=[]# a temporary list for rare word of each sentence
	for item in outitem:	
	    if item in knownwords_c:
		rare_temp.append(item)
	    else:	
		rare_temp.append('_RARE_')
	rare.append(rare_temp)
    return rare

#this function takes the ouput from replace_rare and outputs it
def q3_output(rare):
    outfile = open("B3.txt", 'w')

    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()

#this function takes tags from the training data and calculates trigram probabilities
#tbrown (the list of tags) should be a python list where every element is a python list of the tags of a particular sentence
#it returns a python dictionary where the keys are tuples that represent the trigram, and the values are the log probability of that trigram
def calc_trigrams(tbrown):
    qvalues = {}
    bigram_t=[]#list of bigram tokens
    trigram_t=[]#list of trigram tokens
    bigram_c={}#dict of count of bigram_tokens
    trigram_c={}#dict of count of bigram_tokens
    for item in tbrown:
	bigram_t.extend(tuple(nltk.bigrams(item)))
    	trigram_t.extend(tuple(nltk.trigrams(item)))
    for item in bigram_t:
	if item not in bigram_c:
	    bigram_c[item]=1
        else:
	    bigram_c[item]+=1
    for item in trigram_t:
	if item not in trigram_c:
	    trigram_c[item]=1
        else:
	    trigram_c[item]+=1
    for item in trigram_t:
	try:
	    qvalues[item]=math.log(trigram_c[item],2)-math.log(bigram_c[item[0:2]],2)
	except:
	    qvalues[item]=-1000
    
    return qvalues

#this function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(qvalues):
    #output
    outfile = open("B2.txt", "w")
    for trigram in qvalues:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(qvalues[trigram])])
        outfile.write(output + '\n')
    outfile.close()

#this function calculates emission probabilities and creates a list of possible tags
#the first return value is a python dictionary where each key is a tuple in which the first element is a word
#and the second is a tag and the value is the log probability of that word/tag pair
#and the second return value is a list of possible tags for this data set
#wbrown is a python list where each element is a python list of the words of a particular sentence
#tbrown is a python list where each element is a python list of the tags of a particular sentence
def calc_emission(wbrown, tbrown):
    evalues = {}
    taglist = []
    tag_c={}#count how many occurences for a tag
    wordtag_c={}#count how many occurences for a word/tag combination
    for word_outitem,wordtag_outitem in zip(wbrown,tbrown):
	for word,tag in zip(word_outitem,wordtag_outitem):
	    try: 
		tag_c[tag]+=1
    	    except:
		tag_c[tag]=1
	    try:
		wordtag_c[(word,tag)]+=1
	    except:
		wordtag_c[(word,tag)]=1
	    if tag not in taglist:
		taglist.append(tag)
    for word_outitem,wordtag_outitem in zip(wbrown,tbrown):
	for word,tag in zip(word_outitem,wordtag_outitem):
            evalues[(word,tag)]=math.log(wordtag_c[(word,tag)],2)-math.log(tag_c[tag],2)	
    return evalues, taglist

#this function takes the output from calc_emissions() and outputs it
def q4_output(evalues):
    #output
    outfile = open("B4.txt", "w")
    for item in evalues:
        output = " ".join([item[0], item[1], str(evalues[item])])
        outfile.write(output + '\n')
    outfile.close()


#this function takes data to tag (brown), possible tags (taglist), a list of known words (knownwords),
#trigram probabilities (qvalues) and emission probabilities (evalues) and outputs a list where every element is a string of a
#sentence tagged in the WORD/TAG format
#brown is a list where every element is a list of words
#taglist is from the return of calc_emissions()
#knownwords is from the the return of calc_knownwords()
#qvalues is from the return of calc_trigrams
#evalues is from the return of calc_emissions()
#tagged is a list of tagged sentences in the format "WORD/TAG". Each sentence is a string with a terminal newline, not a list of tokens.

#########
#student's comment

#I didn't implement the algorithm the way as the pseudo code given in Chapter 7. I implemented it my own way, of course the recursion formula is the same.

#Some difference compared to the implementation given in chapter 7 needs to be mentioned: 1.Each sentence is processed without adding " * * " to the head and without adding " STOP "to the end. 2."STOP" is removed from taglist

#Basically, I use a dictionary to store data. To recover best tag sequence, track the backpoints from the last third  to the first tag, the last thirdis obtained through last two and the last two(nth and (n-1)th) tags are got by : tag_n-1,tag_n= argmax_(u,v)(V(n,u,v)*q(STOP|u,v)).

#For details, see below code.
#########
def viterbi(brown, taglist, knownwords, qvalues, evalues):
    tagged = []
    taglist.remove('STOP')#'STOP' is removed since it's gonna be processed independently later
    for outitem in brown:
	outitem=outitem.strip()
	outitem = outitem.split(' ')
	t={}
#t{} is a dictionary, t[(k,u,v)] is the max prob. of a sequence of k tags(y_1 ... y_n) which ends at position k and ending with tag u and v.
	bp={}
#b{}is a dictionary, d[(k,u,v)] is the tag w which right precedes tag u,v, where v is at kth position.And tags w results in t[(k,u,v)].So this dictionary is used to track back the best tag sequence.
	for u in taglist:
# Initialize t[0,u,v]. The assumption is that tag_0 = "*", tag_-1 = "*" 
	    for v in taglist:
	        t[(0,u,v)]=-1000
	t[(0,'*','*')] = 0 
	
	tagged_temp=[]
	for i,item in enumerate(outitem):
	    i+=1# this is only to make the count of words and tags from 1 to n instead of 0 to n-1. For words I mean each word in a sentence and the sentence doesn't have "*" and "STOP"	
	    bptemp={}#is used to update w
	    for u in taglist:
		for v in taglist:		    
			max1=0
			for j,w in enumerate(taglist):
			    try:	
			        part1=t[(i-1,w,u)]
			    except:
				part1=-1000    
			    try:
				part2=qvalues[(w,u,v)]
			    except:
				part2=-1000   
			    try:    
			        part3=evalues[(item,v)]
			    except:
				part3=-1000
			    if j == 1:	
			        max1=part1+part2+part3
				bptemp[(u,v)]=(w,max1)
			    else:
				if part1+part2+part3> max1:
				    max1=part1+part2+part3
				    bptemp[(u,v)]=(w,max1)
			t[(i,u,v)]=max1
			bp[(i,u,v)]=bptemp[(u,v)][0]
	targ2=-2**31# is set to be the mini nega value,which will definitly be updated later at least once. 	    	           
	tags=['_' for i in outitem]# this is the list for tags of a sentence
	for u in taglist:
	    for v in taglist:
		part1=t[(len(outitem),u,v)]
		try:
		    part2=qvalues(u,v,'STOP')
		except:
		    part2=-1000
		if part1+part2  > targ2:
		    targ2=part1+part2
		    tags[len(outitem)-1],tags[len(outitem)-2] = v,u
	for i in range(len(outitem)-3,-1,-1):#recover the tag sequence from the last third to the first one.
	    tags[i]=bp[(i+3,tags[i+1],tags[i+2])]#the index is confusing, because words/tags are counted from 1 to n, but indices are from 0 to n-1 correspondingly.	
	tagged_temp=[]
	for w,t in zip(outitem,tags):
	    tagged_temp.append(w+'/'+t)
    	tagged_temp.append('\n')
	tagged_temp=" ".join(tagged_temp)#make it a string
	tagged.append(tagged_temp)
    return tagged

#this function takes the output of viterbi() and outputs it
def q5_output(tagged):
    outfile = open('B5.txt', 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

#this function uses nltk to create the taggers described in question 6
#brown is the data to be tagged
#tagged is a list of lists of tokens in the WORD/TAG format.
def nltk_tagger(brown):
    tagged = []
    training=brown2.tagged_sents(tagset='universal')
    
    default_tagger = nltk.DefaultTagger('NOUN')
    bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)
    for outitem in brown:
	outitem=outitem.strip()
	outitem=outitem.split(' ')
	trigram_token=trigram_tagger.tag(outitem)
	tagged_temp=[]#for each sentence
	for trig in trigram_token:
	    tagged_temp.append(trig[0]+'/'+trig[1])
	tagged.append(tagged_temp)
	    
    return tagged

def q6_output(tagged):
    outfile = open('B6.txt', 'w')
    for sentence in tagged:
        output = ' '.join(sentence) + '\n'
        outfile.write(output)
    outfile.close()

#a function that returns two lists, one of the brown data (words only) and another of the brown data (tags only)
def split_wordtags(brown_train):
    wbrown = []
    tbrown = []
    for outitem in brown_train:
	outitem = '*/* */* '+outitem.strip() + ' STOP/STOP'
	wbrowninner =[]
        tbrowninner =[]
	for item in outitem.split(' '):
	    R = item.rsplit('/',1)	
	    wbrowninner.append(R[0])
	    tbrowninner.append(R[1])
	wbrown.append(wbrowninner)
	tbrown.append(tbrowninner)
    return wbrown, tbrown

def main():
    #open Brown training data
    infile = open("Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    #split words and tags, and add start and stop symbols (question 1)
    wbrown, tbrown = split_wordtags(brown_train)
    #calculate trigram probabilities (question 2)
    qvalues = calc_trigrams(tbrown)

    #question 2 output
    q2_output(qvalues)

    #calculate list of words with count > 5 (question 3)
    knownwords = calc_known(wbrown)

#    #get a version of wbrown with rare words replace with '_RARE_' (question 3)
    wbrown_rare = replace_rare(wbrown, knownwords)

    #question 3 output
    q3_output(wbrown_rare)

    #calculate emission probabilities (question 4)
    evalues, taglist = calc_emission(wbrown_rare, tbrown)

    #question 4 output
    q4_output(evalues)

    #delete unneceessary data
    del brown_train
    del wbrown
    del tbrown
    del wbrown_rare

    #open Brown development data (question 5)
    infile = open("Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    #format Brown development data here

    #do viterbi on brown_dev (question 5)
    viterbi_tagged = viterbi(brown_dev, taglist, knownwords, qvalues, evalues)

    #question 5 output
    q5_output(viterbi_tagged)

    #do nltk tagging here
    nltk_tagged = nltk_tagger(brown_dev)

    #question 6 output
    q6_output(nltk_tagged)
if __name__ == "__main__": main()
