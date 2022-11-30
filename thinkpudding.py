import json
import sys
import warnings
import time
import logging
import json
#from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper
import collections

from load import read,process_causalpathways,process_spek,matching
from insert import insert

spek_cs=read(sys.argv[1])
causal_pathways=read(sys.argv[2])

spek_out_dicts = {}

caus_out_dict={}
final_dict={}

caus_out_dict=process_causalpathways(causal_pathways)
spek_out_dicts=process_spek(spek_cs)

final_dict=matching(caus_out_dict,spek_out_dicts)

spek_tp=insert(final_dict,spek_cs)


print(spek_tp.serialize(format='json-ld', indent=4))   


#print(final_dict)          

