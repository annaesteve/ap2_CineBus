from typing import TypeAlias, Tuple
import networkx as nx
from networkx import MultiDiGraph as MDG
import osmnx as ox
import matplotlib as plt 
import pickle
import os



CityGraph : TypeAlias = nx.Graph()
BusesGraph: TypeAlias = nx.Graph()
OsmnxGraph: TypeAlias = MDG()
Coord : TypeAlias = Tuple[float, float]   # (latitude, longitude)

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

def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph: ...
    # retorna un graf fusió de g1 i g2

#def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...

#def show(g: CityGraph) -> None: ...
    # mostra g de forma interactiva en una finestra
#def plot(g: CityGraph, filename: str) -> None: ...
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
#def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename

def main() -> None:
    g = get_osmnx_graph()
    save_osmnx_graph(g, 'graf_barcelona.pickle')
    ox.plot_graph(ox.project_graph(load_osmnx_graph('graf_barcelona.pickle')))
    plt.show()
    

if __name__ == '__main__':
    main()
