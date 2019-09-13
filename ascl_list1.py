#! /usr/bin/env python
#
#   Parser for code.nasa.gov json file
#
#   nov 2018:    1008 code    entries (68 have NONE identifier), 229 unique tags,
#                 454 catalog entries
#   sep 2019:    541/532 codes (312 have NONE)
#
#   Example use:
#   ./ascl_list1.py -h               List help
#   ./ascl_list1.py                  lists all "ID" and "NAME" pairs for mode=1 (code.json)
#   ./ascl_list1.py --mode 2         lists all "NAME" for mode=2 (data/catalog.json)
#
#   
#
#
#   The json looks roughly as follows:

#
import json
import sys
import argparse


# parses arguments for directories, mode, and match ID

parser = argparse.ArgumentParser()

parser.add_argument('-tags',        action='store_true')
parser.add_argument('--codedir',    type = str, default = '../code-nasa-gov',  help = "input directory for code-nasa-gov")
parser.add_argument('--code',       type = str, default = 'code.json',         help = "input json for --mode 1")
parser.add_argument('--catalog',    type = str, default = 'data/catalog.json', help = "input json for --mode 2")
parser.add_argument("--mode",       type = int, default = 2,                   help = "1 (code) 2 (data/catalog)")
parser.add_argument("--matchid",    type = str, default = None,                help = "print json for exact match ID (mode 1 only)")
parser.add_argument("--matchname",  type = str, default = None,                help = "print json for matching NAME")
parser.add_argument("--matchdesc",  type = str, default = None,                help = "print json for matching DESCRIPTION")

args = parser.parse_args()

mode       = args.mode
match_name = args.matchname
match_desc = args.matchdesc
match_id   = args.matchid


f1 = open(args.codedir + '/' + args.code)
d1 = json.load(f1)

f2 = open(args.codedir + '/' + args.catalog)
d2 = json.load(f2)
    
# d1: dict_keys(['version', 'agency', 'measurementType', 'releases'])  where d1['releases'] is a list of dict:
#     ['repositoryURL','name','tags','contact','laborHours','date','organization','permissions','identifier','description']
# d2: a list of dict
#     ['Update_Date','Public Code Repo','Description','License','NASA Center','External Link','Contributors','Labor_Hours','Software','Categories','Categories_NLP']

#if mode is 1 and match id is supplied, this will print the json 
#dumps of the matching identifier
#Otherwise, will print the identifier and name


if mode == 1:    
    r = d1['releases']
    nr = len(r)
    for ri in r:
        name = ri['name']
        tags = ri['tags']
        desc = ri['description']
        if not args.tags:
            if 'identifier' in ri.keys():
                iden = ri['identifier']
            else:
                iden = "NONE"

            if match_name != None:
                if name.find(match_name) < 0: continue
                jstr = json.dumps(ri,indent=4)
                print(jstr)
                break

            elif match_desc != None:
                if desc.find(match_desc) < 0: continue
                jstr = json.dumps(ri,indent=4)
                print(jstr)

            elif match_id == iden:
                jstr = json.dumps(ri,indent=4)
                print(jstr)
                break

            else:
                print("%s %s" % (iden,name))
        else:
            for t in tags:
                print(t)

elif mode == 2:
    for i in range(len(d2)):
        ri = d2[i]
        name = ri['Software']
        desc = ri['Description']
        cat  = ri['Categories']
        
        if not args.tags:
            if match_name != None:
                if name.find(match_name) < 0: continue
                jstr = json.dumps(ri,indent=4)
                print(jstr)
                break
            
            elif match_desc != None:
                if desc.find(match_desc) < 0: continue
                jstr = json.dumps(ri,indent=4)
                print(jstr)
            
            else:
                print("%s" % (ri['Software']))
        else:
            for c in cat:
                print(c)


else:
    sys.exit(1)
