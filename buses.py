from typing import TypeAlias, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import urllib.request as ur
import requests
import json

BusesGraph: TypeAlias = nx.Graph()

@dataclass
class Stop:
    name: str
    line: list[str]
    coordinate: Tuple[float, float]

@dataclass
class Line:
    id: int
    stops: list[Stop]

def create_stop(parada: dict[str, int|str]) -> Stop:
    node_nom = parada['Nom']
    node_linies: list[str] = list() 
    for l in parada['Linies'].split(' - '):
        node_linies.append(l)
    node_coordenades = (parada['UTM_X'], parada['UTM_Y'])
    node = Stop(node_nom, node_linies, node_coordenades)

    return node


def define_nodes() -> BusesGraph:
    Buses_graph = BusesGraph
    urlToScrape = "https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json"
    response = requests.get(urlToScrape)
    data = response.json()
    
    num_node = 0
    llista_nodes_afegits:list[str] = list()
    if 'ObtenirDadesAMBResult' in data:
        lines = data['ObtenirDadesAMBResult']['Linies']['Linia']
        for line in lines:
            if line['Parades']['Parada'][0]['Municipi'] == 'Barcelona':
                linia: Line = Line(0,[])
                for parada in line['Parades']['Parada']:
                    node = create_stop(parada)
                    node_dict = asdict(node)
                    if len(node.line) == 1 or node.name not in llista_nodes_afegits:
                        Buses_graph.add_node(num_node, **node_dict)
                        llista_nodes_afegits.append(node.name)
                        num_node += 1

                    linia.stops.append(node)
                linia.id = parada['IdLinia']

    return Buses_graph

def show(g: BusesGraph) -> None:
    nx.draw(g, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.show()

def main() -> None:
    g = define_nodes()
    show(g)


if __name__ == '__main__':
    main()

#def get_buses_graph() -> BusesGraph:


#def plo(g: BusesGraph, nom_fitxer:str) -> None:
