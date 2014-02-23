#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get_all_buckets.py: Writes SPARQL queries to a 4store HTTP server and converts
results to json.
"""

from SPARQLWrapper import SPARQLWrapper
import json

# Update endpoint as needed for local 4store server
endpoint = "http://localhost:8080/sparql/"

# Change to local path to output file
local_output_file = "/Users/melonbreath/Dropbox/Programming/MIT Projects/digital_content_management_tools/visualizations/data/all_buckets.json" # path/to/file.json

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

# Query to get all content types
def getContentTypes():
    queryString = 'SELECT ?contentType WHERE { \n\
        ?contentType rdf:type dcm:Digital_Content_Type . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()
    
# Query to get all buckets in a content type
def getContentTypeBuckets(contentType):
    queryString = 'SELECT ?bucketName ?size ?timeline WHERE { \n\
        dcm:' + contentType + ' dcm:has_collection_type ?bucket .\n\
        ?bucket rdfs:label ?bucketName . \n\
        ?bucket dcm:relative_size ?size . \n\
        ?bucket dcm:has_acquisition_timeline ?timeline . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()

# Run the queries and convert results to json
sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat("json")
contentTypes = getContentTypes()
results = []
for result in contentTypes["results"]["bindings"]:
    ct = result["contentType"]["value"]
    tempResult = getContentTypeBuckets(ct[60:])
    results.append([ct[60:], tempResult])
    
# Convert JSON results to new JSON hierarchical tree formatted for d3 circle-packing layout
tree = {'name': "All Digital Content", 'children': []}

def formatContentType(type, buckets):
    d = {}
    d['name'] = type.replace("_", " ")
    d['children'] = []
    for bucket in buckets:
        n = bucket['bucketName']['value']
        s = bucket['size']['value']
        t = bucket['timeline']['value']
        d['children'].append({'name': n, 'size': s, 'timeline': t})
    return d
    
for item in results:
    t = str(item[0])
    b = item[1]['results']['bindings']
    j = formatContentType(t, b)
    tree['children'].append(j)
    
# Write json output to file for D3 visualization
data = open(local_output_file, 'w')
data.write(json.dumps(tree, indent=4))
data.close()