from typing import TypeAlias, Tuple
import matplotlib.pyplot as plt 
import networkx as nx
import osmnx as ox
import pickle
import os

CityGraph : TypeAlias = nx.Graph()
BusesGraph: TypeAlias = nx.Graph()
OsmnxGraph: TypeAlias = nx.MultiDiGraph()
Coord : TypeAlias = Tuple[float, float]   # (longitude, latitude)
Path: TypeAlias = list[int]         # list of nodes

def get_osmnx_graph() -> OsmnxGraph:
    graph = ox.graph_from_place("Barcelona, Spain", network_type='all', truncate_by_edge=True)
    return graph


def get_simplified_graph_x(g: OsmnxGraph) -> nx.Graph:
    epsg_code = 'EPSG:32631'

    graph_simplified = nx.Graph()
    
    graph_simplified.g['crs'] = epsg_code

    for node, data in g.nodes(data=True):
        x = data['x']
        y = data['y']

        new_node_data = {'x': x, 'y': y}

        graph_simplified.add_node(node, **new_node_data)

    attributes = ["length", "geometry"]

    for u, v, data in g.edges(data=True):
        selected_attributes = {key: data[key] for key in attributes if key in data}
        graph_simplified.add_edge(u, v, **selected_attributes )

    return graph_simplified

def save_osmnx_graph(g: OsmnxGraph, file_name: str) -> None:
    """guarda el graf g al fitxer filename"""

    with open(file_name, 'wb') as file:
        pickle.dump(g, file)

    if os.path.exists(file_name):
        print("The file {} exists".format(file_name))
    
    else:
        print("The file {} doesn't exist".format(file_name))


def load_osmnx_graph(file_name: str) -> OsmnxGraph:
    #retorna el graf guardat al fitxer filename
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            loaded_graph = pickle.load(file)
            return loaded_graph
    return None

def build_city_graph(g: OsmnxGraph, g1: nx.Graph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2

    g1.add_nodes_from(g2.nodes(data=True))
    g1.add_edges_from(g2.edges(data=True))


    for node, atributtes in g2.nodes(data=True):
        nearest_node = ox.distance.nearest_nodes(g, atributtes['coordinate'][0], atributtes['coordinate'][1])
        g1.add_edge(node, nearest_node, length= 0.0)

    return g1

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    start_node = ox.distance.nearest_nodes(ox_g, src[0], src[1])
    end_node = ox.distance.nearest_nodes(ox_g, dst[0], dst[1])

    path: Path = nx.shortest_path(g, source=start_node, target=end_node, weight= 'lenght')

    return path

def calculate_distance_path(g: CityGraph, path: Path) -> float:
    distance = 0.0

    node = 1
    while node < len(path):
        distance += g.edges[path[node - 1], path[node]]['length']
        node += 1
    
    return distance

def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    nx.draw(g, with_labels=True, node_color='red', node_size=400)
    print('nono')
    plt.show()
    print('bueno potser')



#def plot(g: CityGraph, filename: str) -> None: ...
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename

#def show_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename
