#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sparql_query_to_json.py: Writes SPARQL queries to a 4store HTTP server and converts
results to json.
"""

from SPARQLWrapper import SPARQLWrapper
import json

# Update endpoint as needed for local 4store server
endpoint = "http://localhost:8080/sparql/"

# Change to local path to output file
local_output_file = "/Users/melonbreath/Dropbox/Programming/MIT Projects/digital_content_management_tools/visualizations/data/results.json" # path/to/file.json

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

# Query to get all buckets in a content type
def getContentTypeBuckets(contentType):
    queryString = 'SELECT ?bucketName ?size WHERE { \n\
        dcm:' + contentType + ' dcm:has_collection_type ?bucket .\n\
        ?bucket rdfs:label ?bucketName . \n\
        ?bucket dcm:relative_size ?size . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()

# Query to get all buckets in a content type
def getBucketProperties(bucket):
    queryString = 'SELECT ?bucketName ?predicate ?object WHERE { \n\
        dcm:' + bucket + ' ?predicate ?object .\n\
        dcm:' + bucket + ' rdfs:label ?bucketName . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()

# Query to get all buckets managed by an organization
def getBucketsInOrganization(organization):
    queryString = 'SELECT ?bucketName WHERE { \n\
        ?bucket dcm:is_managed_by dcm:' + organization + ' .\n\
        ?bucket rdfs:label ?bucketName . }'
    sparql.setQuery(prefixes + queryString)
    return sparql.query().convert()

# Run the query and conversion
sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat("json")
results = getContentTypeBuckets('Theses')

# Write json output to file for D3 visualization
data = open(local_output_file, 'w')
data.write(json.dumps(results, indent=4))
data.close()