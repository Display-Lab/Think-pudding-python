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
start_time1 = time.time()
start_time = time.time()
spek_cs=read(sys.argv[1])
logging.critical(" reading spek graph--- %s seconds ---" % (time.time() - start_time)) 
start_time = time.time()
causal_pathways=read(sys.argv[2])
logging.critical(" reading causal pathways graph--- %s seconds ---" % (time.time() - start_time))
spek_out_dicts = {}

caus_out_dict={}
final_dict={}
start_time = time.time()
caus_out_dict=process_causalpathways(causal_pathways)
logging.critical(" processing causal pathways--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
spek_out_dicts=process_spek(spek_cs)
logging.critical(" processing spek_cs--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
final_dict=matching(caus_out_dict,spek_out_dicts)
logging.critical(" processing matching--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
spek_tp=insert(final_dict,spek_cs)
logging.critical(" inserting acceptable by--- %s seconds ---" % (time.time() - start_time))

print(spek_tp.serialize(format='json-ld', indent=4))   
logging.critical("complete thinkpudding--- %s seconds ---" % (time.time() - start_time1))
#print(caus_out_dict) 
#print(spek_out_dicts) 
#print(final_dict)          

