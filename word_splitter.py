import nltk, re, pprint, sys, random
from nltk import word_tokenize
from collections import defaultdict

if __name__ == '__main__':
    texts = ['positiveb', 'negativeb']
    for text in texts:
        file = open(text + '.txt', 'rU')
        raw = ''.join([word for word in file])
        #split into lines by presence of newline character
        lines = raw.split('\n')
        lines = [line for line in lines if line != '']
        #print(lines)
        word_num = 1

        for line in lines:
            output_file = open(text+'_word_b'+str(word_num)+'.txt', 'w')
            print(str(line), file= output_file)
            word_num+=1
