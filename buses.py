from dataclasses import dataclass, asdict
from math import sin, cos, sqrt, asin, radians
from typing import TypeAlias, Tuple
import matplotlib.pyplot as plt
import networkx as nx 
import requests
import staticmap


BusesGraph: TypeAlias = nx.Graph


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


def haversine_distance(
        src: Tuple[float, float], dst: Tuple[float, float]) -> float:
    """Returns the distance between src and dst using haversine method"""

    dlat = radians(dst[1]) - radians(src[1])
    dlon = radians(dst[0]) - radians(src[0])

    a = sin(dlat / 2)**2 + cos(src[1]) * cos(dst[1]) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    r = 6371
    distance = c * r

    return distance


def create_stop(parada: dict[str, str], num_node: int) -> Stop:
    """Creates a node (class Stop) of BusesGraph"""

    node_nom = parada['Nom']
    node_linies: list[str] = list()
    for linia in str(parada['Linies']).split(' - '):
        node_linies.append(linia)
    node_coordenades = (float(parada['UTM_X']), float(parada['UTM_Y']))
    node = Stop(node_nom, node_linies, node_coordenades, num_node)

    return node


def create_busesgraph() -> BusesGraph:
    """It creates the BusesGraph doing web scraping"""

    Buses_graph: BusesGraph = BusesGraph()
    urlToScrape = "https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json"
    response = requests.get(urlToScrape)
    data = response.json()

    num_node = 0
    llista_nodes_afegits: list[str] = list()  # auxiliary list
    if 'ObtenirDadesAMBResult' in data:
        lines = data['ObtenirDadesAMBResult']['Linies']['Linia']
        for line in lines:
            if line['Parades']['Parada'][0]['Municipi'] == 'Barcelona':
                linia: Line = Line('0', [])
                i = 0
                for parada in line['Parades']['Parada']:
                    node = create_stop(parada, num_node)
                    # Convert node from class Stop to a dictionary
                    node_dict = asdict(node)
                    # Adds nodes that only have one line, because we surely
                    # know that they aren't in the graph and if not examines 
                    # if the node is in the graph
                    if len(node.line) == 1 or node.name \
                            not in llista_nodes_afegits:
                        Buses_graph.add_node(num_node, **node_dict)
                        llista_nodes_afegits.append(node.name)
                        num_node += 1

                    linia.stops.append(node)
                    # Adds the edges between all the stops in a line with 
                    # time and length attributes
                    if i > 0 and linia.stops[i -
                                             1].node != linia.stops[i].node:
                        length = haversine_distance(
                            linia.stops[i - 1].coordinate,
                            linia.stops[i].coordinate)

                        Buses_graph.add_edge(linia.stops[i - 1].node,
                                             linia.stops[i].node,
                                             length=length,
                                             time=0.05 * length)

                    i += 1
                linia.nom = line['Nom']

    return Buses_graph


def show(g: BusesGraph) -> None:
    """Shows g using networkx.draw"""
    node_positions = nx.get_node_attributes(g, 'coordinate')
    nx.draw(g, pos=node_positions, with_labels=True, edge_color='gray')
    plt.show()


def plot_buses(g: BusesGraph, map: staticmap.StaticMap) -> None:
    """Draws nodes and edges in a staticmap"""

    # We go through all nodes to draw the stops
    for node in g.nodes():
        stop_data = g.nodes[node]
        coordinate = (stop_data['coordinate'][1], stop_data['coordinate'][0])
        map.add_marker(staticmap.CircleMarker(coordinate, 'red', 1))

    # We go through all edges to draw the lines
    for source, destination in g.edges():
        coord_source = (
            g.nodes[source]['coordinate'][1],
            g.nodes[source]['coordinate'][0])
        coord_destination = (
            g.nodes[destination]['coordinate'][1],
            g.nodes[destination]['coordinate'][0])
        map.add_line(staticmap.Line(
            [coord_source, coord_destination], 'blue', 1))


def plotB(g1:BusesGraph, filename: str) -> None:
    """Saves g1 as an image with the map of the city as background
    in a file named filename"""
    map = staticmap.StaticMap(800, 800)
    plot_buses(g1, map)
    image = map.render()  # We save the image in a file named filename
    image.save(filename)
