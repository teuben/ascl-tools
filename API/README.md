Here we document the API that is currently accessible via
https://ascl.net/api/search/ .
The purpose of the API is to provide an interface through which complex queries and searches can be conducted on ASCL data. The API will return results in the JSON format.

# Searchable Fields
The publically available database fields that you can access through the API are:
| field | description |
| ---- | ------------ |
abstract| Brief description of the code
ascl\_id |  The human-friendly version of an ASCL id. Format is YYMM.### where YY is the year, MM is the month, and ### is an incrementing integer padded with zeroes.
bibcode | A 19-digit bibliographic code that allows the entry to be uniquely identified in several indexing services such as the SAO/NASA Astrophysics Data System (ADS). More information about this identifier appears on the ADS website (http://doc.adsabs.harvard.edu/abs\_doc/help\_pages/data.html#bibcodes).
citation\_method | How the code should be cited, according to the author(s) or website of the code. As a courtesy to the code author(s), please check the code website to verify the citation preference.
credit | Normalized list of author names, not serialized
described\_in | Paper in which the code is described ("code paper"); this is typically a refereed paper written by the software author(s), though may not be refereed if there is a "used in" paper
keywords | Serialized array in a text field of words or phrases that are associated with the entry. Currently this field is used to identify software that is associated with NASA (National Aeronautics and Space Administration) and HITS (Heidelberg Institute for Theoretical Studies). 
site\_list | Serialized array of websites associated with a code, including a download site
time\_updated | Date/time code was last updated
title | Title of the code, usually with a "short" title to start, followed by a colon and the longer name
used\_in | Refereed paper in which the code is used but not described, which may be, and is often, written by someone other than the software author. This is provided as verification that the software has been used in a refereed research article, particularly when there is no code paper or the code paper has not been refereed.
views | Number of times an individual code page has been visited



# Syntax
The search API for ASCL entries can be accessed through the /api/search/ endpoint. 
The syntax of a query follows, loosely, the style of *Apache Solr*. 


## Mandatory Parameters

### q
All queries **must** have the **q** (query) parameter, which specifies a
general search string. It can be empty or contain a string, but it
**must** be included in quotation marks (""). Not including this
parameter or not including quotation marks will return a 404 error.


## Optional parameters

### fl

The **fl** parameter describes the fields of the ASCL entry that will
be returned in the call. It must be a string with each field delimited
by commas (,).

### fq

The **fq** (filter query) parameter allows for further filtering of data
through the use of specific operations. The sytax is as follows:

*field-name*[*optional-comparator*]:*value*

There are 4 optional comparators. They are:
| comparator  | description |
| ----------- | ----------- |
| lt | less than |
| lte | less than or equal to |
| gt | greater than |
| gte | greater than or equal to |

The **fq** parameter can be specified multiple times in a query. The
returned result will contain the intersection of the individual
queries, or the logical AND of the filters.

@todo implement OR filtering


# Examples
1. Example of a general, non-fielded query. This will search all public fields and return codes which contain the phrase "machine learning".
https://ascl.net/api/search/?q="machine learning")


2. Example of a query with a filter query attached. This will search for public fields with the phrase "machine learning" whose time updated is greater than X 

@todo implement time filter queries

3. Example of a query with a non-comparator filter query. This will return all codes with "nasa" in the abstract, whose century is exactly 19.
https://ascl.net/api/search/?q=abstract:"nasa"&fq=century:19

3. Example of a query with multiple filter queries. This will search for entries whose century is greater than 19 (meaning in the 21st century) and whose views are greater than 2000
curl 'https://ascl.net/api/search/?q=abstract:"nasa"&fq=century[gt]:19&fq=views[gte]:2300'

4. Example of a query with a return field. This will return the title and the abstract of all entries whose abstracts contain "nasa"
curl "https://ascl.net/api/search/?q=abstract:"nasa"&fl=title,abstract"


5. Example of a query with an invalid return field (should return a 404)
curl 'https://ascl.net/api/search/?q=abstract:"nasa"&fl=abstract,idd'


7. example of a fielded query with multiple fields returned, and a filter query - citation method, abstract and bibcode of all ASCL entries whose abstract contains "nasa" and whose views are strictly less than 200 
curl 'https://ascl.net/api/search/?q=abstract:%22nasa%22&fl=citation_method,abstract,bibcode&fq=views[gt]:200'
