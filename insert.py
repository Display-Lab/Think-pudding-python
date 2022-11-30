import warnings
import time
import logging

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

def insert(final_dict,spek_cs):
    p=URIRef("slowmo:acceptable_by")
    for key, value in final_dict.items():
    #print(value)
        for i in value:
        
            s=i
            o=key
            spek_cs.add((s, p, o,))

    return spek_cs
