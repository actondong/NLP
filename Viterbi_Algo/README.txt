PART1
Run Time:
real 1m12.235s
user 1m11.092s
sys  0m0.300s


A.1

A.2_Perplexity Report
python perplexity.py A2.uni.txt Brown_train.txt
The perplexity is 1104.83292814

python perplexity.py A2.bi.txt Brown_train.txt
The perplexity is 57.2215464238

python perplexity.py A2.tri.txt Brown_train.txt
The perplexity is 5.89521267642

A.3_Perplexity Report
python perplexity.py A3.txt Brown_train.txt
The perplexity is 13.0759217039

A.4
The interpolation perplexity is higher than trigram perplexity and lower than unigram perplexity, which makes sense since we are aiming at a compromising point. However, it is far from the trigram perplexity and more close to the unigram perplexity. It is not simply divide the sum of uni,bi,tri_gram perplexity by three, as we can see from the formula, the sum of uni,bi,tri_gram probability is divided by three. The score of interpolation is still a log probabiliy, which leads to the fact that interpolation perplexity is close to unigram perplexity and far from trigram perplexity.

A.5
python perplexity.py Sample1_scored.txt Sample1.txt 
The perplexity is 11.6492786046

python perplexity.py Sample2_scored.txt Sample2.txt
The perplexity is 6.87993973157e+170

Obviously...Sample1 should be the excerpt of the Brown dataset.

PART2
RUN TIME:
real 17m36.714s
user 17m24.937s
sys 0m0.448s

Some general points:

This is my first python experience. I realized later after coding out B.5 that there are some more powerful data structure could be used here to reduce running time. Say default_dict instead of dict, the items() method of dict, and should use  heap data structure to facilitate extracting maximum...

Baiscally 95% of running time goes to B.5, in which I use to many loops unnecessarily to get list from dict and get max from dict. 

Since the required running time is only less than 25min, so I don't rewrite my code.

B.1

B.2

B.3

B.4

B.5

python pos.py B5.txt Brown_tagged_dev.txt  
Percent correct tags: 91.6696308167

My implementation only reaches 91.7 percent correctness.


B.6
python pos.py B6.txt Brown_tagged_dev.txt
Percent correct tags: 96.9288799422

The performance looks better than viterbi algorithm and the method is more efficient.(Though my viterbi implementation has a great potential in time reducing, still it can't be less than one min) 
Simple algorithm in many situations do generate better results, this is not rare in statistic. Different algorithms fit into different situations, we can't just say which one is better or worse.

Viterbi is a HHM model based on statistical analysis, nltk back-off is not quite a statistical way but take advantage of backing off. My guess is that, for more irrelavent documents(compared to training doc), viterbi would perform better.
