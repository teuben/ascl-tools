Here we document the API that is currently accessible via
http://dev.ascl.net/api/search/ .
The purpose of the API is to provide an interface through which complex queries and searches can be conducted on ASCL data, returning JSON.

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

TODO: add support for multiple operations through AND or OR -- need to look into how Solr addresses this.


# Examples

1. example of a fielded query with multiple fields returned, and a filter query - century, abstract, bibcode, and id of all ASCL entries whose abstract contains "nasa" and whose century is strictly less than 20 (meaning the 21st century in normal parlance)
https://dev.ascl.net/api/search/?q=abstract:"nasa"&fl=century,abstract,bibcode,id&fq=century[lt]:20&


 
