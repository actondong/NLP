from __future__ import division
import nltk
from nltk.corpus import comtrans
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2
# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
	ibm1 = IBMModel1(aligned_sents,10)
 	return ibm1	
# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
	ibm2 = IBMModel2(aligned_sents,10)
	return ibm2
# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
	avg = 0
	for a_sent in aligned_sents[:n]:
		a_result = model.align(a_sent)
		avg += a_result.alignment_error_rate(a_sent)
	avg /= n
	return avg

# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
	output_file = open(file_name,'w')
	for a_sent in aligned_sents[:20]:
		a_result = model.align(a_sent)
		word_str = str(a_result.words)	
		mot_str = str(a_result.mots)
		al_str = str(a_result.alignment)
		output_str = 'Source sentence  '+ word_str+'\n'+'Target Sentence  '+mot_str+'\n'+'Alignments  '+'['+al_str+']'+'\n'+'\n'
		output_file.write(output_str)
	
	output_file.close()

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    #report aer of each sentence of first 20 sentences based on ibm1 model
    for i, a_sent in enumerate(aligned_sents[:20]):
	print "ibm1 , aer of sentence: "+ str(i)+" " +str(compute_avg_aer([a_sent],ibm1,1))
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)
    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    #report aer of each sentence of first 20 sentences based on ibm2 model
    for i , a_sent in enumerate(aligned_sents[:20]):
	print "ibm2 , aer of sentence : "+ str(i)+ " "+ str(compute_avg_aer([a_sent],ibm2,1))
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

if __name__ == "__main__":
	aligned_sents = comtrans.aligned_sents()[:350]
	main(aligned_sents)
