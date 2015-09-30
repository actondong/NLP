import random
import sys
from providedcode import dataset
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition
from providedcode.dependencygraph import DependencyGraph
def parse(argv):
    if len(argv) != 2:
	sys.exit( "python parse.py language.model") 
#    data = dataset.get_english_train_corpus().parsed_sents()
#    random.seed(1234)
#    subdata = random.sample(data, 200)
    language_model = argv[1]
    try:
	sentences = sys.stdin.readlines()
	for i,sentence in enumerate(sentences):
            dg = DependencyGraph.from_sentence(sentence)
            tp = TransitionParser.load(language_model)
            parsed = tp.parse([dg])
            print parsed[0].to_conll(10).encode('utf-8')
#	 tp = TransitionParser(Transition, FeatureExtractor)
#        tp.train(subdata)
#        tp.save('english.model')
#        testdata = dataset.get_swedish_test_corpus().parsed_sents()
#        tp = TransitionParser.load('english.model')

#        parsed = tp.parse(testdata)
	    #open new file for write on first sentence
	    if i == 0:
	    	with open('test.conll', 'w') as f:
                    for p in parsed:
                        f.write(p.to_conll(10).encode('utf-8'))
                        f.write('\n')
	    #append for rest sentences
	    else:
        	with open('test.conll', 'a') as f:
                    for p in parsed:
                        f.write(p.to_conll(10).encode('utf-8'))
                        f.write('\n')
        
#        ev = DependencyEvaluator(testdata, parsed)
#        print "UAS: {} \nLAS: {}".format(*ev.eval())

    except NotImplementedError:
        print """
        This file is currently broken! We removed the implementation of Transition
        (in transition.py), which tells the transitionparser how to go from one
        Configuration to another Configuration. This is an essential part of the
        arc-eager dependency parsing algorithm, so you should probably fix that :)

        The algorithm is described in great detail here:
            http://aclweb.org/anthology//C/C12/C12-1059.pdf

        We also haven't actually implemented most of the features for for the
        support vector machine (in featureextractor.py), so as you might expect the
        evaluator is going to give you somewhat bad results...

        Your output should look something like this:

            UAS: 0.23023302131
            LAS: 0.125273849831

        Not this:

            Traceback (most recent call last):
                File "test.py", line 41, in <module>
                    ...
                    NotImplementedError: Please implement shift!

"""
if __name__ == '__main__':
	parse(sys.argv)
