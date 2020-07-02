Here we document the API that is currently accessible via
https://dev.ascl.net/api/search/ .
The purpose of the API is to provide an interface through which complex queries and searches can be conducted on ASCL data. The API will return results in the JSON format.

# Searchable Fields
The publically available database fields that you can access through the API are:
| field | description |
| ---- | ------------ |
abstract| PLACEHOLDER
ascl\_id |  PLACEHOLDER
bibcode | PLACEHOLDER
citation\_method |  PLACEHOLDER
credit | PLACEHOLDER
described\_in | PLACEHOLDER
keywords | PLACEHOLDER
site\_list | PLACEHOLDER
time\_updated | PLACEHOLDER
title | PLACEHOLDER
used\_in | PLACEHOLDER
views | PLACEHOLDER



# Syntax
The search API for ASCL entries can be accessed through the /api/search/ endpoint. The syntax of a query follows, loosely, the style of Apache Solr. 


## Mandatory Parameters

### q
All queries **must** have the q parameter, which specifies a general search string. It can be empty or contain a string, but it **must** be included in quotation marks (""). Not including this parameter or not including quotation marks will return a 404 error. 


## Optional parameters

### fl
The fl parameter describes the fields of the ASCL entry that will be returned in the call. It must be a string with each field delimited by commas (,). 

### fq
The fq (filter query) parameter allows for further filtering of data through the use of specific operations. The sytax is as follows:

*field-name*[*optional-comparator*]:*value*

There are 4 optional comparators. They are:
| comparator  | description |
| ----------- | ----------- |
| lt | less than |
| lte | less than or equal to |
| gt | greater than |
| gte | greater than or equal to |

The fq parameter can be specified multiple times in a query. The returned result will contain the intersection of the individual queries, or the logical AND of the filters. 

TODO: implement OR filtering


# Examples
1. Example of a general, non-fielded query. This will search all public fields and return codes which contain the phrase "machine learning"
curl 'https://dev.ascl.net/api/search/?q="machine learning"'

2. Example of a query with a filter query attached. This will search for public fields with the phrase "machine learning" whose time updated is greater than X 
(TODO: implement time filter queries)

3. Example of a query with a non-comparator filter query. This will return all codes with "nasa" in the abstract, whose century is exactly 19.
https://dev.ascl.net/api/search/?q=abstract:"nasa"&fq=century:19

3. Example of a query with multiple filter queries. This will search for entries whose century is greater than 19 (meaning in the 21st century) and whose views are greater than 2000
curl 'https://dev.ascl.net/api/search/?q=abstract:"nasa"&fq=century[gt]:19&fq=views[gte]:2300'

4. Example of a query with a return field. This will return the title and the abstract of all entries whose abstracts contain "nasa"
curl "https://dev.ascl.net/api/search/?q=abstract:"nasa"&fl=title,abstract"


5. Example of a query with an invalid return field (should return a 404)
curl 'https://dev.ascl.net/api/search/?q=abstract:"nasa"&fl=abstract,idd'


7. example of a fielded query with multiple fields returned, and a filter query - century, abstract and bibcode of all ASCL entries whose abstract contains "nasa" and whose century is strictly less than 20 (meaning the 21st century in normal parlance)
curl 'https://dev.ascl.net/api/search/?q=abstract:"nasa"&fl=century,abstract,bibcode&fq=century[lt]:20&'
