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

warnings.filterwarnings("ignore")


def read(file):
    start_time = time.time()
    g = Graph()
    g.parse(file)
    logging.critical(" reading graph--- %s seconds ---" % (time.time() - start_time)) 
    return g

def process_causalpathways(causal_pathways):
    causal_dicts={}
    caus_type_dicts={}
    caus_out_dict={}
    caus_o = URIRef("http://purl.obolibrary.org/obo/cpo_0000029")
    caus_s=[]
    for s, p, o in causal_pathways.triples((None,  RDF.type, caus_o)):
    # print(s)
    # print(type(s))
            caus_s.append(s)
    for x in range(len(caus_s)):
    #caus_s[x]=f'"{caus_s[x]}"'
    #print (caus_s[x])
        s=caus_s[x]
    #print(s)
        p=URIRef("http://example.com/slowmo#HasPrecondition")
        for s,p,o in causal_pathways.triples( (s, p, None) ):
            causal_dicts[o]=s

#print(causal_dicts.values())

    ids= list(causal_dicts.values())
    ids = [*set(ids)]
    types=[]
    for x in range(len(ids)):
    #caus_s[x]=f'"{caus_s[x]}"'
    #print (ids[x])
        y=[k for k,v in causal_dicts.items() if v == ids[x] ]  
        for i in range(len(y)):
            s=y[i]
            for s,p,o in causal_pathways.triples((s,RDF.type,None)):
                y[i]=o
            #print(ids[x])
            #print(y[i])
        caus_type_dicts[ids[x]]=y        
            
# caus_out_dict[ids[x]]=blist
# print(caus_out_dict)

    return caus_type_dicts

def process_spek(spek_cs):

    spek_out_dicts={}
    BL=[]
    s=URIRef("http://example.com/app#mpog-aspire") 
    #s=URIRef("http://example.com/app#display-lab")
    p=URIRef("http://example.com/slowmo#HasCandidate")
    p1=URIRef("slowmo-HasPrecondition")
    #s1=BNode("cee24ddd0e27fbb94e1e6d278189e1d2e")
    p1=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
    slowmo_precndtn=URIRef("http://purl.obolibrary.org/obo/psdo_0000117")
    comparator_type=URIRef("http://purl.obolibrary.org/obo/psdo_0000094")

    i=0
    for s,p,o in spek_cs.triples( (s, p, None) ):
#     #print(triple)
        s1= o
    #print(s1+" ")
    
        y=[o for s,p,o in spek_cs.triples((s1,p1,None))]
        # s2=o
        # #print(o)
        for i in range(len(y)):
            s=y[i]

            for s,p,o in spek_cs.triples((s,RDF.type,None)):
                # if o != comparator_type:
                y[i]=o
        # y.pop(0)
        spek_out_dicts[s1] = y
    return spek_out_dicts

def matching(caus_out_dict,spek_out_dicts):
    final_dict={}
    fg=list(caus_out_dict.values())
    fr=list(spek_out_dicts.values())
 
    for i in range(len(fg)):
   
        for x in range(len (fr)):
            result =  all(elem in fr[x]  for elem in fg[i])
            if result == True:
       
       #print(result)
      # l=list(spek_out_dicts.keys())[list(spek_out_dicts.values()).index(fr[x])]
                l=[k for k,v in spek_out_dicts.items() if v == fr[x]]
       #print(l)
                y=list(caus_out_dict.keys())[list(caus_out_dict.values()).index(fg[i])]
       #blist.append(y)
       #print(y)
                final_dict[y]=l
    return final_dict