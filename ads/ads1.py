#! /usr/bin/env python
#
#  https://github.com/adsabs/ads-examples
#  https://ads.readthedocs.io/en/latest/
#  https://github.com/adsabs/adsabs-dev-api     curl
#  Needs: ~/.ads/dev_key
#

import os
import sys

#  - sandbox doesn't seem to work (jan 2021)
#import ads.sandbox as ads
import ads


#  listing with code names
arg1 = sys.argv[1]

codes = open(arg1).readlines()
for code in codes:
    code = code.strip()
    if code[0] == '#':
        continue

    print("# CODE:",code)

    # lazy loading (expensive)
    #q = ads.SearchQuery(full=code, sort=year)

    # loading with fields ahead of time
    q = ads.SearchQuery(full=code, fl=['title','first_author','year','citation_count','bibcode'],sort='year', rows=10)

    n1 = 0
    for paper in q:
        print("%s\t%s\t%s\t%s\t%s" % (paper.year, paper.citation_count, paper.bibcode, paper.first_author, paper.title[0]))
        n1 = n1 + 1

    q1=q.response.get_ratelimits()
    print('# %d %s\n' % (n1,q1['remaining']))
