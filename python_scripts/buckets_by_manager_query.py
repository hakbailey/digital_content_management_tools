#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
buckets_by_manager_query.py: Writes SPARQL queries to a 4store HTTP server and converts
results to json.
"""

from SPARQLWrapper import SPARQLWrapper
import json

# Update endpoint as needed for local 4store server
endpoint = "http://localhost:8080/sparql/"

# Change to local path to output file
local_output_file = "/Users/melonbreath/Dropbox/Programming/MIT Projects/digital_content_management_tools/visualizations/data/buckets_by_manager.json" # path/to/file.json

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
def getManagers():
    queryString = 'SELECT ?manager WHERE { \n\
        ?manager rdf:type foaf:Organization . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()
    
# Query to get all buckets in a content type
def getBuckets(manager):
    queryString = 'SELECT ?bucketName ?size ?timeline WHERE { \n\
        ?bucket dcm:is_managed_by dcm:' + manager + ' .\n\
        ?bucket rdfs:label ?bucketName . \n\
        ?bucket dcm:relative_size ?size . \n\
        ?bucket dcm:has_acquisition_timeline ?timeline . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()

# Run the queries and convert results to json
sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat("json")
managers = getManagers()
results = []
for result in managers["results"]["bindings"]:
    m = result["manager"]["value"]
    tempResult = getBuckets(m[60:])
    if tempResult["results"]["bindings"]:
        results.append([m[60:], tempResult])
    
# Convert JSON results to new JSON hierarchical tree formatted for d3 circle-packing layout
tree = {'name': "All Digital Content", 'children': []}

def formatResults(manager, buckets):
    d = {}
    d['name'] = manager.replace("_", " ")
    d['children'] = []
    for bucket in buckets:
        n = bucket['bucketName']['value']
        s = bucket['size']['value']
        t = bucket['timeline']['value']
        d['children'].append({'name': n, 'size': s, 'timeline': t})
    return d
    
for item in results:
    m = str(item[0])
    b = item[1]['results']['bindings']
    j = formatResults(m, b)
    tree['children'].append(j)
    
# Write json output to file for D3 visualization
data = open(local_output_file, 'w')
data.write(json.dumps(tree, indent=4))
data.close()