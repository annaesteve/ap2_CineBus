from typing import TypeAlias, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass, asdict
import urllib.request as ur
import requests

BusesGraph: TypeAlias = nx.Graph()

@dataclass
class Stop:
    name: str
    line: list[str]
    coordinate: Tuple[float, float]
    node: int

@dataclass
class Line:
    nom: str
    stops: list[Stop]

def create_stop(parada: dict[str, int|str], num_node:int) -> Stop:
    node_nom = parada['Nom']
    node_linies: list[str] = list() 
    for l in parada['Linies'].split(' - '):
        node_linies.append(l)
    node_coordenades = (parada['UTM_Y'], parada['UTM_X'])
    node = Stop(node_nom, node_linies, node_coordenades, num_node)

    return node


def define_nodes() -> BusesGraph:
    Buses_graph: BusesGraph() = BusesGraph
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
                i = 0
                for parada in line['Parades']['Parada']:
                    node = create_stop(parada, num_node)
                    node_dict = asdict(node)
                    if len(node.line) == 1 or node.name not in llista_nodes_afegits:
                        Buses_graph.add_node(num_node, **node_dict)
                        llista_nodes_afegits.append(node.name)
                        num_node += 1
                    
                    linia.stops.append(node)
                    if i > 0 and linia.stops[i-1].node != linia.stops[i].node:
                        Buses_graph.add_edge(linia.stops[i-1].node, linia.stops[i].node)

                    i += 1
                linia.nom = line['Nom']
    
    return Buses_graph

def show(g: BusesGraph) -> None:
    node_positions = nx.get_node_attributes(g, 'coordinate')
    #nx.draw_networkx_edges(g, pos=node_positions )
    nx.draw(g, pos=node_positions, with_labels=True, edge_color='gray')
    plt.show()

def main() -> None:
    g = define_nodes()
    show(g)


if __name__ == '__main__':
    main()

#def get_buses_graph() -> BusesGraph:




#def plo(g: BusesGraph, nom_fitxer:str) -> None
