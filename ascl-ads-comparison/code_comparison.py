import sys
import os
import re


f = open(os.path.join(sys.path[0], "ads_codes"), "r")

converted_dict = {}

conv = []

for line in f.readlines():
    x = re.match("^\d\d(\d\d)ascl\.soft(\d\d)(\d\d\d)\D$", line)    
    if x:
        converted = ("ascl." + x.group(1)+x.group(2)+"."+x.group(3)).strip()
        if converted in conv:
            print("ads inconsistency " + converted + " -\t" + line.strip())
            print("\tother ads entry is \t\t" + converted_dict[converted] + "\n")
        conv.append(converted)
        #dictionary of ascl id to ascl bibcode
        converted_dict[converted] = line.strip()
    else:
        print(line)

'''
g = open(os.path.join(sys.path[0], "ascl_codes"), "r")

ascl_lines = g.readlines()
ascl_lines = [line.strip() for line in ascl_lines]

#print(ascl_lines)

ads_converted = converted_dict.keys()

num_matches = 0
double_matches = 0

matches = []

for line in ads_converted:
    if converted_dict[line] in matches:
        double_matches += 1
        print("double match found: " + line)
    else: 
        num_matches += 1
        matches.append(converted_dict[line])
'''

'''
num_matches = 0 
double_matches = 0
for line in ads_converted:
    #print(line)
    if line not in matches:
        num_matches += 1
        matches.append(line)
        #print("found match " + line)
    else:
        double_matches += 1
        print("found double match " + line)
print("matches " + str(matches))
print("double matches " + str(double_matches))
'''
