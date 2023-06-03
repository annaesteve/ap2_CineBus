from typing import TypeAlias, Tuple
import matplotlib.pyplot as plt 
import networkx as nx
import osmnx as ox
import staticmap
import pickle
import buses
import os

CityGraph : TypeAlias = nx.Graph()
BusesGraph: TypeAlias = nx.Graph()
OsmnxGraph: TypeAlias = nx.MultiDiGraph()
Coord : TypeAlias = Tuple[float, float]   # (longitude, latitude)
Path: TypeAlias = list[int]         # list of nodes


def get_osmnx_graph() -> OsmnxGraph:
    graph = ox.graph_from_place("Barcelona, Spain", network_type='all', truncate_by_edge=True)
    return graph


def get_simplified_graph(g: OsmnxGraph) -> nx.Graph:
    """Converts g to a networkx.graph"""
    epsg_code = 'EPSG:32631'

    graph_simplified = nx.Graph()
    
    graph_simplified.graph['crs'] = epsg_code

    for node, data in g.nodes(data=True):
        x = data['x']
        y = data['y']

        new_node_data = {'x': x, 'y': y}

        graph_simplified.add_node(node, **new_node_data)

    attributes = ["length", "geometry"]

    for u, v, data in g.edges(data=True):
        selected_attributes = {key: data[key] for key in attributes if key in data}
        graph_simplified.add_edge(u, v, **selected_attributes )
        length = graph_simplified.edges[u,v]['length'] 
        graph_simplified.edges[u,v]['time'] = 0.15*length

    return graph_simplified


def save_osmnx_graph(g: OsmnxGraph, file_name: str) -> None:
    """Saves g in a file named filename"""

    with open(file_name, 'wb') as file:
        pickle.dump(g, file)

    if os.path.exists(file_name):
        print("The file {} exists".format(file_name))
    
    else:
        print("The file {} doesn't exist".format(file_name))


def load_osmnx_graph(file_name: str) -> OsmnxGraph:
    """Returns the graph saved in file_name"""
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            loaded_graph = pickle.load(file)
            return loaded_graph

    return None


def build_city_graph(g: OsmnxGraph, g1: nx.Graph, g2: BusesGraph) -> CityGraph:
    """Returns the graph of composing g1 and g2"""
    g1.add_nodes_from(g2.nodes(data=True))
    g1.add_edges_from(g2.edges(data=True))

    for node, atributtes in g2.nodes(data=True):
        nearest_node = ox.distance.nearest_nodes(g, atributtes['coordinate'][0], atributtes['coordinate'][1])
        g1.add_edge(node, nearest_node, length= 0.0, time=0.0)

    return g1


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """Finds the shorter path to go from src to dst"""
    start_node = ox.distance.nearest_nodes(ox_g, src[0], src[1])
    end_node = ox.distance.nearest_nodes(ox_g, dst[0], dst[1])

    path: Path = nx.shortest_path(g, source=start_node, target=end_node, weight= 'time')

    return path


def calculate_distance_path(g: CityGraph, path: Path) -> float:
    """Return the distance of path"""
    distance = 0.0

    node = 1
    while node < len(path):
        distance += g.edges[path[node - 1], path[node]]['length']
        node += 1
    
    return distance


def show(g: CityGraph) -> None:
    """Shows g in an interactive way in another window""" 
    nx.draw(g, with_labels=True, node_color='red', node_size=400)
    print('nono')
    plt.show()
    print('bueno potser')


def plot(g:nx.Graph, filename: str) -> None:
    """Saves g in a file named filename as an image with a map of the city as backgroung"""
    map = staticmap.StaticMap(800,800)
    
    #We go through all nodes to draw the stops NODE: (ID, {x: float, y: float} 
    for _, data in g.nodes(data=True): 
        coordinate = (data['x'], data['y'])
        map.add_marker(staticmap.CircleMarker(coordinate, 'red', 3))

    #print(g.edges(data=True))
    #We go through all edges to draw the lines EDGES : [ID_source, ID_dest, {lenght: , geometry:merda})
    for source, destination in g.edges(data=True):
        coord_source = (g.nodes[source]['x'], g.nodes[source]['y'])
        coord_destination = (g.node[destination]['x'], g.node[destination]['y'])
        map.add_line(staticmap.Line([coord_source, coord_destination], 'blue', 1))
    
    #We save the image in a file named nom_fitxer
    image = map.render()
    image.save(filename)


#def show_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename


def main()-> None:
    g = get_osmnx_graph()
    g1 = get_simplified_graph(g)
    #g2: buses.BusesGraph = buses.create_busesgraph()
    save_osmnx_graph(g, 'bcn.pickle')
    plot(g1, "ciutat.png")

if __name__ == '__main__':
    main()
