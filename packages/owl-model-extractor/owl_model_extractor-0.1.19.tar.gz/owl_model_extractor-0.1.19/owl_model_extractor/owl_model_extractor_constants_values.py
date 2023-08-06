PREFERRED_PREFIX = ["http://purl.org/vocab/vann/preferredNamespacePrefix"]
LICENSE = ["http://purl.org/dc/terms/license","https://creativecommons.org/ns#license", "http://creativecommons.org/ns#license"]
TITLE = ["http://purl.org/dc/terms/title", "http://purl.org/dc/elements/1.1/title"]
VERSION = ["http://www.w3.org/2002/07/owl#versionIRI"]
NS_OWL = "http://www.w3.org/2002/07/owl#"
RDFS_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
SKOS_PREF_LABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
RDFS_COMMENT = "http://www.w3.org/2000/01/rdf-schema#comment"
SKOS_DEFINITION = "http://www.w3.org/2004/02/skos/core#definition"

SPARQL_STR = "SELECT ?o WHERE {?s <##PH1##> ?o}"

SPARQL_METADATA_EXTRACT = "select distinct ?p where { <##PH1##> ?p ?o . }"

SPARQL_LABEL_EXTRACT = """
select distinct ?s where { 
        ?s a owl:Class . 
        ?s rdfs:label ?label .
}
"""
