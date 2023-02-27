import sys
import warnings
import time
import logging
import json
import re
import numpy as np 
import matplotlib.pyplot as plt 

#from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper
from thinkpudding import Thinkpudding

f=open(sys.argv[1])
spek_cs = json.load(f)
#print(type(content))
spek_cs =json.dumps(spek_cs)
f1=open(sys.argv[2])
causal_pathways=json.load(f1)
causal_pathways =json.dumps(causal_pathways)
#print(spek_cs)
tp=Thinkpudding(spek_cs,causal_pathways)
tp.process_causalpathways()
tp.process_spek()
tp.matching()
spek_tp=tp.insert()
op=spek_tp.serialize(format='json-ld', indent=4)
#print(op)
f = open("spek_tp.json", "w")
f.write(op)
f.close()