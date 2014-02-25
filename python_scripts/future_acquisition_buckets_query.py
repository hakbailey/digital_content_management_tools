#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
library_buckets_query.py: Writes SPARQL queries to a 4store HTTP server and converts
results to json.
"""

from SPARQLWrapper import SPARQLWrapper
import json

# Update endpoint as needed for local 4store server
endpoint = "http://localhost:8080/sparql/"

# Change to local path to output file
local_output_file = "/Users/melonbreath/Dropbox/Programming/MIT Projects/digital_content_management_tools/visualizations/data/future_buckets.json" # path/to/file.json

# List of all prefixes/URIs used in triplestore (update if new prefixes are added)
prefixes = '''PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#>
    PREFIX dcm: <http://www.semanticweb.org/hbailey/ontologies/2013/9/mitorg#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dctype: <http://purl.org/dc/dcmitype/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <http://schema.org/>
    
'''

# Query to get all buckets with anticipated acquisition in the next 3-5 years
def getFiveYearBuckets():
    queryString = 'SELECT ?bucketName ?size ?timeline WHERE { \n\
        ?bucket rdf:type dcm:Collection_Type .\n\
        ?bucket dcm:has_acquisition_timeline dcm:three_to_five_years .\n\
        ?bucket rdfs:label ?bucketName . \n\
        ?bucket dcm:relative_size ?size . \n\
        ?bucket dcm:has_acquisition_timeline ?timeline . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()

# Query to get all buckets with anticipated acquisition in the next 5-10 years
def getTenYearBuckets():
    queryString = 'SELECT ?bucketName ?size ?timeline WHERE { \n\
        ?bucket rdf:type dcm:Collection_Type .\n\
        ?bucket dcm:has_acquisition_timeline dcm:five_to_ten_years .\n\
        ?bucket rdfs:label ?bucketName . \n\
        ?bucket dcm:relative_size ?size . \n\
        ?bucket dcm:has_acquisition_timeline ?timeline . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()
    
# Run the queries and convert results to json
sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat("json")
fiveYear = getFiveYearBuckets()
tenYear = getTenYearBuckets()

# TODO: format results for viz (bubble chart?)

#results = []
#for result in fiveYear["results"]["bindings"]:
#    ct = result["contentType"]["value"]
#    tempResult = fiveYear(ct[60:])
#    results.append([ct[60:], tempResult])
#    
# Convert JSON results to new JSON hierarchical tree formatted for d3 circle-packing layout
tree = {'name': "All Future Content", 'children': []}

def formatResults(parent, buckets):
    d = {}
    d['name'] = parent
    d['children'] = []
    for bucket in buckets:
        n = bucket['bucketName']['value']
        s = bucket['size']['value']
        t = bucket['timeline']['value']
        d['children'].append({'name': n, 'size': s, 'timeline': t})
    return d
    
#for item in results:
#    t = str(item[0])
#    b = item[1]['results']['bindings']
#    j = formatContentType(t, b)

five = formatResults("Five Year", fiveYear['results']['bindings'])
ten = formatResults("Ten Year", tenYear['results']['bindings'])
tree['children'].append(five)
tree['children'].append(ten)
    
# Write json output to file for D3 visualization
data = open(local_output_file, 'w')
data.write(json.dumps(tree, indent=4))
data.close()