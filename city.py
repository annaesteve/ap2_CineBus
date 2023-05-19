from typing import TypeAlias, Tuple
import networkx as nx
from networkx import MultiDiGraph as MDG
import osmnx as ox
import matplotlib as plt 


CityGraph : TypeAlias = nx.Graph()
OsmnxGraph: TypeAlias = MDG()
Coord : TypeAlias = Tuple[float, float]   # (latitude, longitude)

def get_osmnx_graph() -> None:
    graph = ox.graph_from_place("Barcelona, Spain", network_type='all')
    ox.plot_graph(ox.project_graph(graph))
    plt.show()


#def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None: ...
    # guarda el graf g al fitxer filename
#def load_osmnx_graph(filename: str) -> OsmnxGraph: ...
    # retorna el graf guardat al fitxer filename

#def build_city_graph(g1: OsmnxGraph, g2: CityGraph) -> CityGraph: ...
    # retorna un graf fusió de g1 i g2

#def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...

#def show(g: CityGraph) -> None: ...
    # mostra g de forma interactiva en una finestra
#def plot(g: CityGraph, filename: str) -> None: ...
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
#def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename

def main() -> None:
    get_osmnx_graph()

if __name__ == '__main__':
    main()
