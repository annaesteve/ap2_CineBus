from typing import TypeAlias, Tuple
import networkx as nx
import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt 
import spicy as sp
import pickle
import os
import buses
from dataclasses import dataclass
from queue import Queue


CityGraph : TypeAlias = nx.Graph()
BusesGraph: TypeAlias = nx.Graph()
OsmnxGraph: TypeAlias = nx.MultiDiGraph()
Coord : TypeAlias = Tuple[float, float]   # (latitude, longitude)


@dataclass
class Cross:
    id: int
    coordinate: tuple[float, float]

@dataclass
class Path:
    initial_position: Coord
    final_position: Coord
    distance: int


def get_osmnx_graph() -> OsmnxGraph:
    graph = ox.graph_from_place("Barcelona, Spain", network_type='all', simplify=True)
    
    for u, v, key, geom in graph.edges(data = "geometry", keys = True):
        if geom is not None:
            del(graph[u][v][key]["geometry"])

    return graph

def simplify_graph(g: OsmnxGraph) -> CityGraph:
    simple_g = nx.Graph()
    
    for node, data in g.nodes(data=True):
        x, y = data['y'], data['x']
        simple_g.add_node(node, coordinate_x= x, coordinate_y = y)

    
    for u, v, data in g.edges(data=True):
        distance = data['length']
        simple_g.add_edge(u, v, distance= distance)

    return simple_g

def save_osmnx_graph(g: CityGraph, file_name: str) -> None:
    """guarda el graf g al fitxer filename"""

    with open(file_name, 'wb') as file:
        pickle.dump(g, file)

    if os.path.exists(file_name):
        print("The file {} exists".format(file_name))
    
    else:
        print("The file {} doesn't exist".format(file_name))


def load_osmnx_graph(file_name: str) -> CityGraph:
    #retorna el graf guardat al fitxer filename
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            loaded_graph = pickle.load(file)
            return loaded_graph
    return None


def build_city_graph(g1: CityGraph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2
    graf = nx.compose(g1,g2)


    for node, atributtes in g2.nodes(data=True):
        nearest_node = ox.distance.nearest_nodes(g1, atributtes['coordinate'][0], atributtes['coordinate'][1])
        graf.add_edge(node, nearest_node)

    nx.draw_networkx(graf)
    plt.show()

    return graf

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    graph = nx.from_edgeslist(ox_g[['u', 'v', 'key']].values.tolist(), create_using=nx.MultiDiGraph)
    start_node = ox.distance.nearest_nodes(g, src[0], src[1], method='haversine')
    end_node = ox.distance.nearest_nodes(g, dst[0], dst[1], method='haversine')

    path = nx.shortest_path(graph, source=start_node, target = end_node, weight = 'lenght')

    return path


def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    nx.draw(g, with_labels=True, node_color='red', node_size=400)
    print('nono')
    plt.show()
    print('bueno potser')



#def plot(g: CityGraph, filename: str) -> None: ...
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename

#def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename

def main() -> None:
    g = get_osmnx_graph()
    s_g = simplify_graph(g)
    #save_osmnx_graph(s_g, 'graf_barcelona.pickle')
    print('si')
    #show(load_osmnx_graph('graf_barcelona.pickle'))
    show(s_g)

if __name__ == '__main__':
    main()
