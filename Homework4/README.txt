################################################
#                 NLP HW4  		       #	
# sd2810 				       #
# running time expected for A.py --  2min55sec #
# running time expected for B.py --  29sec     #
# running time expected for CE.py -- 1min20sec #
################################################



Part1:
1) 2)

A.py
IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

Results are reported in ibm1.txt and ibm2.txt 

3)
Source sentence  [u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
Target Sentence  [u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']"'"]


ibm1 , aer of sentence: 5 0.75
Alignments  [0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1]
ibm2 , aer of sentence : 5 0.666666666667
Alignments  [0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0]


Generally, ibm2 should outperform ibm1(at least this is true when testing on training data), in ibm1 we don't have a dynamic distortion variable which encodes position information as ibm2 does. We don't have information about alignment between ith position and jth position in pair of sentences. In other words, we lose information which could be taken advantage of in ibm1.

In above example, both alighments suck but ibm2 at least try to match 0th and 9th position  from germany to 0th position of english sentence , while ibm1 has no matchces to 0. Though I don't know germany, I can imagine there must be some word in germany sentence which matches to 'please' in english sentence. This is finally revealed in ibm2 by using postion information. We tends to have the word 'please' at beginning or end of a sentence, which is exactly the way ibm2 deals with this problem here.
4)
The experiment takes as many as 30 iterations and converges around 20-24 iterations.
And finally reach 0.659 for ibm1 and 0.648 for ibm2

Part2:
1),2),3)

Berkeley Aligner
---------------------------
Average AER: 0.578
Results are stored in ba.txt

4)
Compared to ibm2,
AER is reduced by 10%

5)
Same sentence as we analyze in partA:
ba , aer of sentence 5 0.5
Alignments  [0-1 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0 10-11]
ibm2 , aer of sentence : 5 0.666666666667
ibm1 , aer of sentence: 5 0.75

Here ba performs best, ba is intuitively a good attempt, it is more tolerant to
mis-judgement by taking vote between model and reverse model. AGAIN, i dont speak germany, i can't tell why certain mapping is right or not, but the philosophy behind this is simple, by taking reverse model into consideration, we get more information from the data. Our model alone is not symmetric but the translation process is, take advantage of this fact and implement reverse model could gain us more information. 

6)
Credit:
My solution is 1)use geometry mean to replace arithmetic mean when averaging.
	        This is reasonable, when two models disagree a lot on one pair of matching, we should favor the less one, while two models agree on the count,geometry mean is the same as arithmetic mean.
	       2)use 30 ite instead of 10
		When ite = 30, my mode converges
Better Berkeley Aligner
---------------------------
Average AER: 0.552

Compared to Berkeley in B.py, AER is reduced by 5%

