#! /usr/bin/env python
#



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
            codes[code] = id
            print 'ascl:'+id,code
    print 'Found %d code entries' % len(codes)
    return codes

def parse2(file,codes):
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    for line in lines:
        print line

codes = parse1('ascl.php')

parse2('sample.tex',codes)
