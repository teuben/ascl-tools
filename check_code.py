#! /usr/bin/env python
#
#  read a txt file (.e.g. or PDF obtained via pdftotext)
#  mark words
#  learn from the description vector which papers contain code references
#  a human then still needs to review results
#

#from __future__ import division  # Python 2 users only
#from __future__ import print_function
import sys, os
import codecs
import nltk, re, pprint

#from nltk import word_tokenize
#from nltk import FreqDist

my1 = ['compile','install',
       'http','ftp','url',
       'code','package','library','github','sourceforge','download','link','file','table','image',
       'fits','hdf',
       'fortran','c++','python',
       'software','algorithm','program','routine','recipe','procedure','script',
       'numeric','model','pipeline',
       'IDL','CASA','IRAF','AIPS','MIRIAD','GIPSY','NEMO','ASCL']






def try1(txtfile):
    #f = open('1408.6846v1.txt')
    f = codecs.open(txtfile, encoding='utf-8')
    raw = f.read()
    #
    tokens = nltk.word_tokenize(raw)
    text   = nltk.Text(tokens)
    words  = [w.lower() for w in text]
    vocab  = sorted(set(words))
    #
    fdist1 = nltk.FreqDist(words)
    vocab  = fdist1.keys()
    return (fdist1,vocab)



if __name__ == '__main__':
    sumn = range(len(my1))
    for i in range(len(sumn)):
        sumn[i] = 0
    for tfile in sys.argv[1:]:
        (f,v) = try1(tfile)
        sys.stdout.write("%-20s" % tfile)
        sum = 0
        i = 0
        for w in my1:
            sum = sum + f[w]
            sumn[i] = sumn[i] + f[w]
            i = i + 1
            sys.stdout.write(" %3d" % f[w])
        sys.stdout.write("     %4d\n" % sum)
    #
    sys.stdout.write("\n%-20s" % "sum")    
    for i in range(len(my1)):
        sys.stdout.write(" %3d" % sumn[i])
    sys.stdout.write("\n")
    #
    sys.stdout.write("\n%-20s" % " ")
    for i in range(len(my1)):
        sys.stdout.write(" %3d" % (i+1))
    sys.stdout.write("\n")
    #
    for i in range(len(my1)):
        print "  %2d %-12s" % (i+1,my1[i])
