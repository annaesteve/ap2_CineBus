from typing import TypeAlias, Tuple, Optional
import networkx as nx
from dataclasses import dataclass
from bs4 import BeautifulSoup
import urllib.request as ur
import requests
import json

BusesGraph: TypeAlias = nx.Graph()

@dataclass
class Node:
    nom: str
    coordenades: Tuple[int, int]

def define_nodes() -> BusesGraph:
    Parades: BusesGraph = ()
    urlToScrape = "https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json"
    req = requests.get(urlToScrape, headers={'User-Agent': 'Chrome/35.0.1916.47'})
    r = ur.urlopen(req)
    soup = BeautifulSoup(r, "lxml")
    
    return BusesGraph

def get_buses_graph() -> BusesGraph:


def show(g: BusesGraph) -> None:

def plo(g: BusesGraph, nom_fitxer:str) -> None:
