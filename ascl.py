#! /usr/bin/env python
#
#   quick helper code for ASCL editing (Teuben/Allen)
#   is really part of the git module 'teuben/ascl-tools' but placed here
#   for convenience
#

import sys

debug = False
punct = ['.', ',', '/', ':', ';', '{', '}']


def printf(format, *args):
    sys.stdout.write(format % args)

def parse1(file):
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    print "Found %d lines in %s" % (len(lines),file)
    # look for
    #     <tr><td>ascl:1102.023</td><td>21cmFAST:
    magic = '<tr><td>ascl:'
    len1 = len(magic)
    codes = {}
    for line in lines:
        if line[0:len1] == magic:
            line1 = line[len1:80]
            id = line1[0:8]
            tmp     = line1[17:80]
            # print "    ",line1[0:50]
            ic = tmp.find(':')
            code = tmp[0:ic]
            code_words = code.split()
            codes[code] = id
            if len(code_words) > 1:
                print '# ascl:'+id,code
            else:
                print 'ascl:'+id,code
    print 'Found %d code entries' % len(codes)
    return codes

def parse2(file):
    """ read quick index for ADASS """
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    codes = {}
    # file has "ascl:1112.017 ASpec" style lines
    for line in lines:
        if line[0] == '#': continue
        words = line.split()
        if len(words) != 2: continue
        # print words[0], words[1]
        codename = words[1].lower()
        codes[codename] = "\\ooindex{%s, %s}" % (words[1],words[0])
    return codes

def parse3(file,codes):
    """
    codename ->   codename\ooindex{codename, ascl_id}
    """
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    if debug: print codes
    for line in lines:
        print 'LINE: ',line
        line2 = ''
        has_a_code = False
        words = line.split(' ,')
        for word in words:
            print 'WORD: ',word
            if codes.has_key(word):
                has_a_code = True
                line2 = line2 + "%s\\ooindex{%s, %s} " % (word,word,codes[word])
            else:
                line2 = line2 + word + " "
        if has_a_code:
            print "# " + line
            print line2
        else:
            print line


def wclean(word):
    w = word.lower()
    len1 = len(punct)
    for p in punct:
        if w[0] == p:
            w = w[1:]
            break
    len2 = len(w)
    if len2 == 0:
        return w
    for p in punct:
        if w[len2-1] == p:
            w = w[:-1]
            break
    return w


def parse4(file,codes):
    """
    codename ->   codename\ooindex{codename, ascl_id}
    """
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    if debug: print codes
    for line in lines:
        if debug: print 'LINE: ',line
        line2 = ''
        has_a_code = False
        words = line.split()
        for dword in words:
            word = wclean(dword)
            if debug: print 'WORD: ',dword,word
            if codes.has_key(word):
                has_a_code = True
                line2 = line2 +  "%s \n" % (codes[word])
        if has_a_code:
            print "# " + line
            print line2
        else:
            if debug: print line


#parse3('sample.tex',codes)

if __name__ == '__main__':
    file = sys.argv[1]
    #
    if False:
        codes = parse1('ascl.php')
    else:
        codes = parse2('ascl1.txt')
    parse4(file,codes)
