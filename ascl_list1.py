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
import argparse


#parses arguments for directories, mode, and match ID
parser = argparse.ArgumentParser()
parser.add_argument('--codedir', type = str, default = '../code-nasa-gov/code.json', help = "input directory for code.json")
parser.add_argument("--catalogdir", type = str, default = '../code-nasa-gov/data/catalog.json', help = "input directory for data/catalog.json")
parser.add_argument("--mode", type = int, default = 2)
parser.add_argument("--matchid", type = str, default = None)

args = parser.parse_args()

#print(args)


mode = args.mode

f1 = open(args.codedir)
d1 = json.load(f1)

f2 = open(args.catalogdir)
d2 = json.load(f2)
    
match_id = args.matchid

# dict_keys(['version', 'agency', 'measurementType', 'releases'])

#if mode is 1 and match id is supplied, this will print the json 
#dumps of the matching identifier
#Otherwise, will print the identifier and name

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

#incomplete mode 2, needs more exploratory work 
elif mode == 2:
    for i in range(len(d2)):
        r = d2[i]
        if match_id == None:
            print("%s" % (r['Software']))
else:
    sys.exit(1)
