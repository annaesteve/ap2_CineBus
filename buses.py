from dataclasses import dataclass, asdict
from math import sin, cos, sqrt, asin
from typing import TypeAlias, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import requests
import staticmap
import folium

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

def haversine_distance(src: Tuple[float,float], dst: Tuple[float,float]) -> float:
    dlat = dst[1] - src[1]
    dlon = dst[0] - src[0]

    a = sin(dlat/2)**2 + cos(src[1]) * cos(dst[1]) * sin(dlon/2)**2
    c = 2*asin(sqrt(a))

    r = 6371
    distance = c*r

    return distance

def create_stop(parada: dict[str, int|str], num_node:int) -> Stop:
    """Creates each node of BusesGraph"""
    node_nom = parada['Nom']
    node_linies: list[str] = list() 
    for l in parada['Linies'].split(' - '):
        node_linies.append(l)
    node_coordenades = (parada['UTM_Y'], parada['UTM_X'])
    node = Stop(node_nom, node_linies, node_coordenades, num_node)

    return node


def create_busesgraph() -> BusesGraph:
    """It creates a BusesGraph doing web scraping"""
    Buses_graph: BusesGraph() = BusesGraph
    urlToScrape = "https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json"
    response = requests.get(urlToScrape)
    data = response.json()
    
    num_node = 0
    llista_nodes_afegits:list[str] = list() #auxiliary list
    if 'ObtenirDadesAMBResult' in data:
        lines = data['ObtenirDadesAMBResult']['Linies']['Linia'] 
        for line in lines:
            if line['Parades']['Parada'][0]['Municipi'] == 'Barcelona':
                linia: Line = Line(0,[])
                i = 0
                for parada in line['Parades']['Parada']:
                    node = create_stop(parada, num_node)
                    node_dict = asdict(node) #convert node from a class to a dictionary
                    if len(node.line) == 1 or node.name not in llista_nodes_afegits:
                        Buses_graph.add_node(num_node, **node_dict)
                        llista_nodes_afegits.append(node.name)
                        num_node += 1
                    
                    linia.stops.append(node)
                    if i > 0 and linia.stops[i-1].node != linia.stops[i].node:
                        Buses_graph.add_edge(linia.stops[i-1].node, linia.stops[i].node, length = haversine_distance(linia.stops[i-1].coordinate, linia.stops[i].coordinate)  )

                    i += 1
                linia.nom = line['Nom']

    Buses_graph.edges(data=True)
    return Buses_graph


def show(g: BusesGraph) -> None:
    """Shows g using networkx.draw"""
    node_positions = nx.get_node_attributes(g, 'coordinate')
    nx.draw(g, pos=node_positions, with_labels=True, edge_color='gray')
    plt.show()


def plot(g: BusesGraph, nom_fitxer:str) -> None:
    """Saves g as an image with the map of the city as background in a file named nom_fitxer"""
    map = staticmap.StaticMap(800,800)
    
    #We go through all nodes to draw the stops
    for node in g.nodes(): 
        stop_data = g.nodes[node]
        coordinate = (stop_data['coordinate'][0], stop_data['coordinate'][1])
        map.add_marker(staticmap.CircleMarker(coordinate, 'red', 3))

    #We go through all edges to draw the lines
    for source, destination in g.edges():
        coord_source = (g.nodes[source]['coordinate'][0], g.nodes[source]['coordinate'][1])
        coord_destination = (g.nodes[destination]['coordinate'][0], g.nodes[destination]['coordinate'][1])
        map.add_line(staticmap.Line([coord_source, coord_destination], 'blue', 1))
    
    #We save the image in a file named nom_fitxer
    image = map.render()
    image.save(nom_fitxer)


def plot2(g: BusesGraph, nom_fitxer: str) -> None:
    """Saves g as an interactive map with the map of the city as background in an HTML file named nom_fitxer"""
    # Create a folium map centered on the first stop's coordinates
    first_stop = g.nodes[1]
    map_center = first_stop['coordinate'][::-1]  # Reverse the coordinates for folium
    m = folium.Map(location=map_center)

    # Add markers for all stops
    for node, stop_data in g.nodes.items():
        coordinate = stop_data['coordinate'][::-1]  # Reverse the coordinates for folium
        folium.Marker(location=coordinate).add_to(m)

    # Add lines for all edges
    for source, destination in g.edges:
        source_coord = g.nodes[source]['coordinate'][::-1]  # Reverse the coordinates for folium
        dest_coord = g.nodes[destination]['coordinate'][::-1]  # Reverse the coordinates for folium
        folium.PolyLine(locations=[source_coord, dest_coord], color='blue', weight=1).add_to(m)

    # Save the map as an HTML file
    m.save(nom_fitxer)


def main() -> None:
    g = create_busesgraph()
    plot(g, 'mapa_buses.png')


if __name__ == '__main__':
    main()
