#! /usr/bin/env python
#
#   nov 2018:    1008 code    entries (68 have NONE identifier), 229 unique tags,
#                 454 catalog entries
#
#   Intended use:
#
#   ascl_list1.py                    lists all "ID" and "NAME" pairs
#   ascl_list1.py ID                 dumps the wole JSON
#
#
#   The json looks roughly as follows:

#
import json
import sys

mode = 2

f1 = open('code.json')
d1 = json.load(f1)

f2 = open('data/catalog.json')
d2 = json.load(f2)
    

# dict_keys(['version', 'agency', 'measurementType', 'releases'])

if len(sys.argv) > 1:
    match_id = sys.argv[1]
else:
    match_id = None


if mode == 1:    
    r = d1['releases']
    nr = len(r)
    for ri in r:
        name = ri['name']
        tags = ri['tags']
        if True:
            if 'identifier' in ri.keys():
                iden = ri['identifier']
            else:
                iden = "NONE"
            if match_id == None:
                print("%s %s" % (iden,name))
            elif match_id == iden:
                jstr = json.dumps(ri,indent=4)
                print(jstr)
                break
        else:
            for t in tags:
                print(t)
elif mode == 2:
    for i in range(len(d2)):
        r = d2[i]
        if match_id == None:
            print("%s" % (r['Software']))
else:
    sys.exit(1)
