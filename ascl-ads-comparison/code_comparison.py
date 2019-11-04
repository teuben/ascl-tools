import sys
import os
import re


f = open(os.path.join(sys.path[0], "ads_codes"), "r")

converted_dict = {}

for line in f.readlines():
    x = re.match("^\d\d(\d\d)ascl\.soft(\d\d)(\d\d\d)\D$", line)    
    if x:
        converted_dict[("ascl." + x.group(1)+x.group(2)+"."+x.group(3)).strip()] = line.strip()
    else:
        print(line)


g = open(os.path.join(sys.path[0], "ascl_codes"), "r")

ascl_lines = g.readlines()
ascl_lines = [line.strip() for line in ascl_lines]

print(len(ascl_lines))

keys = converted_dict.keys()

matches = 0
non_matches = 0

for line in keys:
    if line in ascl_lines:
        matches += 1
        continue
        #print("found match " + line)
    else:
        non_matches += 1
        print("found non-match " + line + " " + converted_dict[line])
print("matches " + str(matches))
print("non matches " + str(non_matches))
