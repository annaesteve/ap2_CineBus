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
from shapely.ops import transform
from functools import partial
import pyproj


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

    epsg_code = 'EPSG:32631'

    graph = ox.graph_from_place("Barcelona, Spain", network_type='all', truncate_by_edge=True)

    graph_simplified = nx.Graph()
    
    graph_simplified.graph['crs'] = epsg_code

    for node, data in graph.nodes(data=True):
        x = data['x']
        y = data['y']

        new_node_data = {'x': x, 'y': y}

        graph_simplified.add_node(node, **new_node_data)

    attributes = ["length", "geometry"]

    for u, v, data in graph.edges(data=True):
        selected_attributes = {key: data[key] for key in attributes if key in data}
        graph_simplified.add_edge(u, v, **selected_attributes )

    build_city_graph(graph_simplified, buses.define_nodes())
    return graph

def simplify_graph_x(g: OsmnxGraph) -> nx.Graph:
    simple_g = nx.Graph()
    
    for node, data in g.nodes(data=True):
        x, y = data['x'], data['y']
        simple_g.add_node(node, coordinate_x= x, coordinate_y = y)

    
    for u, v, data in g.edges(data=True):
        distance = data['length']
        simple_g.add_edge(u, v, distance= distance)

    build_city_graph(simple_g, buses.define_nodes())

    return simple_g

def save_osmnx_graph(g: OsmnxGraph, file_name: str) -> None:
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

def build_city_graph(g1: nx.Graph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2

    g1.add_nodes_from(g2.nodes(data=True))
    g1.add_edges_from(g2.edges(data=True))


    for node, atributtes in g2.nodes(data=True):
        nearest_node = ox.distance.nearest_nodes(g1, atributtes['coordinate'][0], atributtes['coordinate'][1])
        g1.add_edge(node, nearest_node)
   
    print('pas6')

    #target_crs = pyproj.CRS('EPSG:32631')
    #project = partial(
    #    pyproj.transform,
    #    pyproj.Proj(g1.graph['crs']),
    #    target_crs
    #)


    #graph_proj = ox.project_graph(g1, to_crs=target_crs)
    
    #fig, ax = ox.plot_graph(graph_proj, show=False, close=False)

    #ax.set_title('OSMnx Graph in EPSG:32631')

    nx.draw(g1, with_labels=True, node_color='lightblue', edge_color='gray')

    plt.show()

    print('pas7')

    return g1

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
    #s_g = simplify_graph(g)
    #save_osmnx_graph(g, 'graf_barcelona.pickle')
    #build_city_graph(load_osmnx_graph('graf_barcelona.pickle'), buses.define_nodes())

    #show(s_g)

if __name__ == '__main__':
    main()
