Name: shiyu dong
Uni : sd2810
Problem1:
a.
Works well

b.
A dependency graph is projective,
where the presence of an arc (i, l, j) entails that there is directed
path from i to every node k such that min(i, j) < k < max(i, j).

c.
Projective:
Coms4705's midterm is very difficult!

non-Projective:
I saw the girl who loves you.

Problem2:
a.
Works well

b.Examine the performance of your parser using the provided
badfeatures.model.

I got the same results as mentioned in comments in text.py
UAS: 0.23023302131 
LAS: 0.125273849831
As we can tell from above results,the performance is very poor.


Problem3:
a. Add at least three feature types and describe
their implementation, complexity, and performance 
Features added :

1. Distance.
One type of feature that has often been used is the distance between two words, typically
the word on top of the stack and the first word in the input buffer. This can be measured by the
number of words intervening, possibly restricted to words of a certain type such as verbs

2. No. of left/right children:
Another common type of feature is the number of children of a particular word, possibly divided into left
children and right children.

3. buffer[1] + word
   buffer[1] + tag
   buffer[2] + tag
   buffer[3] + tag

b.

Wokrs well

c.Score your models against the test data sets 

Summary:
I have tested each language for 5 times:
english is between 6.8 and 7.0 
korean is between 6.3 and 6.4
swedish is between 6.8 and 6.9
danish is between 7.0 and 7.1

Bleow are results of last test:

english:
  Number of training examples : 200
  Number of valid (projective) examples : 200
  Training support vector machine...
  done!
  UAS: 0.733333333333 
  LAS: 0.693827160494

korean:
  Number of training examples : 200
  Number of valid (projective) examples : 200
  Training support vector machine...
  done!
  UAS: 0.753959057551 
  LAS: 0.633835457706
swedish:
  Number of training examples : 200
  Number of valid (projective) examples : 200
  Training support vector machine...
  done!
  UAS: 0.723456790123 
  LAS: 0.683950617284
danish:
  Number of training examples : 200
  Number of valid (projective) examples : 174
  Training support vector machine...
  done!
  UAS: 0.79001996008 
  LAS: 0.709780439122

d.discuss in a few sentences the complexity of the arc-eager
shift-reduce parser, and what tradeoffs it makes.

The time complexity of arc-eager stack-based algorithm is O(n). 
Both SHIFT and RIGHT-ARC
decrease the length of β and increase the height of σ, while both REDUCE and LEFTARC decrease the height of σ. Hence, the combined number of SHIFT and RIGHT-ARC
transitions, as well as the combined number of REDUCE and LEFT-ARC transitions, are
bounded by n.
The spave complexity of arc-eager stack-based algorithm is also O(n)

When doing feature extraction, the time complexity is not included in above complexity analysis. 

Static parsing oracles are only correct as functions from gold-trees to transition sequences, and not as functions from configurations to transitions.

We also restrict only  on dependency graphs which are projective. 

Regarding to features, it is not the more the better, there classes of features which complement each other and which kind of undermine each other.

And if we include too many features, definitely will slow our program.
Prolem4:
My problem4 works well.
