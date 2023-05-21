from typing import TypeAlias, Tuple
import networkx as nx
import osmnx as ox
import matplotlib as plt 
import pickle
import os
import buses
from dataclasses import dataclass

CityGraph : TypeAlias = nx.Graph()
BusesGraph: TypeAlias = nx.Graph()
OsmnxGraph: TypeAlias = nx.MultiDiGraph()
Coord : TypeAlias = Tuple[float, float]   # (latitude, longitude)

@dataclass
class Path:
    initial_position: Coord
    final_position: Coord
    distance: int

def get_osmnx_graph() -> OsmnxGraph:
    graph = ox.graph_from_place("Barcelona, Spain", network_type='all')
    return graph


def save_osmnx_graph(g: OsmnxGraph, file_name: str) -> None:
    # guarda el graf g al fitxer filename
    #ox.plot_graph(ox.project_graph(g))
    #plt.show()
    with open(file_name, 'wb') as file:
        pickle.dump(g, file)

    if os.path.exists(file_name):
        print("The file {} exists".format(file_name))
    
    else:
        print("The file {} doesn't exist".format(file_name))


def load_osmnx_graph(file_name: str) -> OsmnxGraph:
    # retorna el graf guardat al fitxer filename

    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            loaded_graph = pickle.load(file)

    return loaded_graph

def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2

    graf = nx.compose(g1,g2)
    ox.plot_graph(ox.project_graph(graf))
    plt.show()

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:

    graph = nx.from_edgeslist(ox_g[['u', 'v', 'key']].values.tolist(), create_using=nx.MultiDiGraph)
    start_node = ox.distance.nearest_nodes(g, src[0], src[1], method='haversine')
    end_node = ox.distance.nearest_nodes(g, dst[0], dst[1], method='haversine')

    path = nx.shortest_path(graph, source=start_node, target = end_node, weight = 'lenght')

    return path

def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    
    ox.plot_graph(ox.project_graph(g))
    plt.show()

#def plot(g: CityGraph, filename: str) -> None: ...
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename

#def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename

def main() -> None:
    g = get_osmnx_graph()
    save_osmnx_graph(g, 'graf_barcelona.pickle')
    #build_city_graph(load_osmnx_graph('graf_barcelona.pickle'), buses.define_nodes())
    

if __name__ == '__main__':
    main()
