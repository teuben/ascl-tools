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
import hashlib

# parses arguments for directories, mode, and match ID

parser = argparse.ArgumentParser()

parser.add_argument('--list',       action='store_true')
parser.add_argument('--tags',       action='store_true')

parser.add_argument('--codedir',    type = str, default = '../code-nasa-gov',  help = "input directory for code-nasa-gov")
parser.add_argument('--code',       type = str, default = 'code.json',         help = "input json for --mode 1")
parser.add_argument('--catalog',    type = str, default = 'data/catalog.json', help = "input json for --mode 2")
parser.add_argument("--mode",       type = int, default = 2,                   help = "1 (code) 2 (data/catalog)")
parser.add_argument("--matchid",    type = str, default = None,                help = "print json for exact match ID (mode 1 only)")
parser.add_argument("--matchname",  type = str, default = None,                help = "print json for matching NAME")
parser.add_argument("--matchdesc",  type = str, default = None,                help = "print json for matching DESCRIPTION")
parser.add_argument("--matchfield", type = str, default = None,                help = "print the matching fields for both databases")

args = parser.parse_args()

mode       = args.mode
match_name = args.matchname
match_desc = args.matchdesc
match_id   = args.matchid
match_field = args.matchfield
    
# d1: dict_keys(['version', 'agency', 'measurementType', 'releases'])  where d1['releases'] is a list of dict:
#     ['repositoryURL','name','tags','contact','laborHours','date','organization','permissions','identifier','description']
# d2: a list of dict
#     ['Update_Date','Public Code Repo','Description','License','NASA Center','External Link','Contributors','Labor_Hours','Software','Categories','Categories_NLP']

#   code.json fields        catalog.json fields

#   'repositoryURL'         'Public Code Repo',
#   'name'                  'Software',
#   'tags'                  'Categories','Categories_NLP'
#   'contact'               'Contributors',
#   'laborHours'            'Labor_Hours',
#   'date',                 'Update_Date',
#   'organization'          'NASA Center',
#   'permissions'           'License',
#   'identifier'            seems unique, but only appears for < half of codes
#   'description'           'Description',
#


if args.list:
    if mode == 2:
        f1 = open(args.codedir + '/' + args.catalog)
        d1 = json.load(f1)

        output_str = "Ordinal,Hash,Status,Software,Description,Public Code Repo,External Link,Contributors"
        print( output_str )
        for i in range(len(d1)): 
            ri = d1[i]

            s       = ", "
            s2      = "," 

            soft    = "\"" + ri['Software']             + "\""  
            desc    = "\"" + ri['Description']          + "\""  
            pcr     = "\"" + ri["Public Code Repo"]     + "\""  
            el      = "\"" + ri["External Link"]        + "\""  
            cont    = "\"" + s.join(ri["Contributors"]) + "\"" 
           
            output_str = s2.join([str(i), str(0), soft, desc, pcr, el, cont]) 
            print(output_str.encode("utf8"))
    
    elif mode == 1:
        f1 = open(args.codedir + '/' + args.code)
        d1 = json.load(f1)
        r = d1["releases"]
        for i in range(len(r)):
            
            m = hashlib.md5()
            
            ri = r[i]
           
            s       = ", "
            s2      = "," 
            
            el = ("\"" + ri.get("homepageURL") + "\"") if ri.get("homepageURL") != None else ("\"" + "None" + "\"")
            soft    = "\"" + ri['name']                 + "\""  
            desc    = "\"" + ri['description']          + "\""  
            pcr     = "\"" + ri["repositoryURL"]        + "\""  
            cont    = "\"" + ri["contact"].get("email")      + "\"" 
            m = hashlib.md5(bytes((el+soft+desc+pcr+cont))).hexdigest()

            output_str = s2.join([str(i), m, str(0), soft, desc, pcr, el, cont]) 
            print(output_str.encode("utf8"))
            



#if mode is 1 and match id is supplied, this will print the json 
#dumps of the matching identifier
#Otherwise, will print the identifier and name

elif mode == 1:    
    
    f1 = open(args.codedir + '/' + args.code)
    d1 = json.load(f1)
    
    r = d1['releases']

    #prints all the tags sequentially
    if args.tags:
        for i in range(len(r)):
            ri  = r[i]
            tags= ri['tags']

            for t in tags:
                print(t)

    else:
        #if match_name is provided, then print json dump of the name
        if match_name != None:
            for i in range(len(r)):
                ri  = r[i]
                name = ri['name']
                if name.find(match_name) >= 0:
                    jstr = json.dumps(ri,indent=4)
                    print(jstr)
        #same for description
        elif match_desc != None:
            for i in range(len(r)):
                ri  = r[i]
                desc = ri['description']
                if desc.find(match_desc) >= 0: 
                    jstr = json.dumps(ri,indent=4)
                    print(jstr)
        #same for id
        elif match_id != None:
            for i in range(len(r)):
                ri = r[i]
                iden = ri['identifier'] if 'identifier' in ri.keys() else "NONE"

                if match_id == iden:
                    jstr = json.dumps(ri,indent=4)
                    print(jstr)
        #otherwise print out "<identifier> <name>"
        else:
            for i in range(len(r)):
                ri = r[i]
                iden = ri['identifier'] if 'identifier' in ri.keys() else "NONE"
                name = ri['name']
                print("%s %s" % (iden,name))

elif mode == 2:
    f2 = open(args.codedir + '/' + args.catalog, )
    d2 = json.load(f2)
    #prints out all the tags sequentially
    if args.tags:
        for i in range(len(d2)):
            ri = d2[i] 
            cat     = ri['Categories']

            for c in cat:
                print(c)

    #prints out the repo in csv formatting  


    else:
        #if match name is provided, print out all the dumps for matching names
        if match_name != None:
            for i in range(len(d2)): 
                ri = d2[i]
                soft    = ri['Software']

                if soft.find(match_name) >= 0:
                    jstr = json.dumps(ri,indent=4)
                    print(jstr)
        #same for description
        elif match_desc != None:
            for i in range(len(d2)):
                ri = d2[i]
                desc    = ri['Description']
                
                if desc.find(match_desc) >= 0:
                    jstr = json.dumps(ri,indent=4)
                    print(jstr)
        #prints out name of the code    
        else:
            for i in range(len(d2)): 
                ri = d2[i]
                print("%s" % (ri['Software']))

elif mode == 3:
    #MUST supply matchfield and matchname
    #match_name is an exact match with both databases


    #comparison mode
#   code.json fields        catalog.json fields             Our field

#   'repositoryURL'         'Public Code Repo',             repo
#   'name'                  'Software',                     name
#   'tags'                  'Categories','Categories_NLP'   tags -both
#   'contact'               'Contributors',                 who -both
#   'laborHours'            'Labor_Hours',                  labor
#   'date',                 'Update_Date',                  date -code.json
#   'organization'          'NASA Center',                  org
#   'permissions'           'License',                      lic -both
#   'identifier'            ---------------                 id
#   'description'           'Description',                  desc
#   'homepageURL'           'External Link'                 ext
  
    fields = {
        "repo": ["repositoryURL",   "Public Code Repo"],
        "name": ["name",            "Software"],
        "tags": ["tags",            "Categories"],
        "who":  ["contact",         "Contributors"],
        "labor":["laborHours",      "Labor_Hours"],
        "date": ["date",            "Update_Date"],
        "org":  ["organization",    "NASA Center"],
        "lic":  ["permissions",     "License"],
        "id":   ["identifier",  ""],
        "desc": ["description",     "Description"],
        "ext":  ["homepageURL", "External Link"]
    } 
    
    if match_field and match_name:

        f1 = open(args.codedir + '/' + args.code)
        d1 = json.load(f1)

        f2 = open(args.codedir + '/' + args.catalog, )
        d2 = json.load(f2)

        r = d1["releases"]
        code_ans = "name not in code"
        catalog_ans = "name not in catalog"

        #iterates through code.json data structure and finds the first exact 
        #matching name. Sets the result equal to the appropriate field of the 
        #returned object
        for i in range(len(r)):
            ri = r[i]
            if match_name == ri["name"]:
                

                code_ans = str(ri[fields[match_field][0]])
                
                #DOES NOT DISPLAY PROPERLY IF THE match_field IS tags, date, who, lic 
                #BREAKS IF match_field is id
                
                '''
                if match_field == "tags":
                    code_ans = ""
                    for tag in ri["tags"]:
                        code_ans += tag
                '''

                break
        for j in range(len(d2)):
            d2j = d2[j]
            if match_name == d2j["Software"]:
                catalog_ans = str(d2j[fields[match_field][1]])
                break

        print("code.json:\t" + code_ans + "\n" + "catalog.json:\t" + catalog_ans)

    else:
        print("missing matchfield and/or exact matchname")



else:
    sys.exit(1)
