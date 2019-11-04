import sys
import os
import json
import requests

'''
REQUIRES 1 FILE IN YOUR DIRECTORY:
    - .ads_key      : text of your ads api key
'''


f = open(os.path.join(sys.path[0], "../.ads_key"), "r")
key = f.read()
#print("your key is: " + key + "\n")

key = key.strip()

#os.system("cat .ads_key")


headers = {
        "Authorization": "Bearer:" + key,
}

def check_pages(num):
    return_list = []
    curr_result = 0
    for k in range(num):
        #print("starting at resutlt " + str(curr_result))

        params = (
            ('q', 'ascl'),
            ('fl',  'bibcode'),
            ('rows', "3000"),
            ('start', str(curr_result))
        )

        response = requests.get('https://api.adsabs.harvard.edu/v1/search/query', headers=headers, params=params)
        #print(response)
        data = response.json();
        num_results = data["response"]["numFound"]
        
        curr_result = curr_result + num_results

        #print(str(num_results) + " total found on page " + str(k))
        
        new_rel = []         
        for i in data["response"]["docs"]:
            bc = i['bibcode']
            if "ascl.soft" in bc:
                new_rel.append(bc)

        #print(str(len(new_rel)) + " relevant found on page " + str(k))
        
        return_list.extend(new_rel)
    return_list.sort()
    return return_list



lst = check_pages(3)

f = open(os.path.join(sys.path[0], "ads_codes"), "w+")

for i in lst:
    f.write(i + "\n")

