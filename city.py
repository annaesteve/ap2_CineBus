from typing import TypeAlias, Tuple
from math import sin, cos, sqrt, asin, radians, atan2
import matplotlib.pyplot as plt 
import networkx as nx
import osmnx as ox
import pickle
import os
import staticmap
import matplotlib.image as mpimg
import buses

CityGraph : TypeAlias = nx.Graph
BusesGraph: TypeAlias = nx.Graph
OsmnxGraph: TypeAlias = nx.MultiDiGraph
Coord : TypeAlias = Tuple[float, float]   # (longitude, latitude)
Path: TypeAlias = list[int]         # list of nodes


def haversine_distance(
        src: Tuple[float, float], dst: Tuple[float, float]) -> float:
    """Returns the distance between src and dst using haversine method"""

    # Convert degrees to radians
    lat1 = radians(src[0])
    lon1 = radians(src[1])
    lat2 = radians(dst[0])
    lon2 = radians(dst[1])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius = 6371  # Radius of the Earth in kilometers. Use 3956 for miles.
    distance = radius * c

    return distance

def get_osmnx_graph() -> OsmnxGraph:
    """Creates the graph of Barcelona streets"""

    graph = ox.graph_from_place("Barcelona, Spain", network_type='all', truncate_by_edge=True)
    graph.graph['crs'] = 'EPSG:32631' #we determine coordinate's system 
    return graph


def get_simplified_graph(g: OsmnxGraph) -> nx.Graph:
    """Converts g to a networkx.graph"""

    epsg_code = 'EPSG:32631'
    graph_simplified = nx.Graph()
    graph_simplified.graph['crs'] = epsg_code

    # From nodes information we only take the coordinate
    for node, data in g.nodes(data=True): 
        x = data['x']
        y = data['y']
        new_node_data = {'x': x, 'y': y}
        graph_simplified.add_node(node, **new_node_data)

    #From the edges we only take the length and geometry information needed in further functions
    attributes = ["length", "geometry"]

    for u, v, data in g.edges(data=True): 
        selected_attributes = {key: data[key] for key in attributes if key in data}
        graph_simplified.add_edge(u, v, **selected_attributes)
        length = graph_simplified.edges[u, v]['length']
        graph_simplified.edges[u, v]['time'] = 0.15 * length

    return graph_simplified


def save_osmnx_graph(g: OsmnxGraph, file_name: str) -> None:
    """Saves g in a file named filename"""

    with open(file_name, 'wb') as file:
        pickle.dump(g, file)

    # Controls if the file_name given exists
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


def plot_city(g:nx.Graph, map: staticmap.StaticMap) -> None:
    """Draws all edges and nodes in the staticmap"""

    #We go through all nodes to draw the crosses
    for _, data in g.nodes(data=True): 
        coordinate = (data['y'], data['x'])
        map.add_marker(staticmap.CircleMarker(coordinate, 'red', 1))

    #We go through all edges to draw the streets
    for source, destination in g.edges():
        coord_source = (g.nodes[source]['y'], g.nodes[source]['x'])
        coord_destination = (g.nodes[destination]['y'], g.nodes[destination]['x'])
        map.add_line(staticmap.Line([coord_source, coord_destination], 'blue', 1))



def build_city_graph(g: OsmnxGraph, g1: nx.Graph, g2: BusesGraph) -> CityGraph:
    """Returns the graph of composing g1 and g2"""

    # We add all stops of g2 to the simplified graph (g1)
    g1.add_nodes_from(g2.nodes(data=True))

    # We link each stop node to nearest cross node (with length 0)
    for node, atributtes in g2.nodes(data=True):
        nearest_node = ox.distance.nearest_nodes(g, atributtes['coordinate'][1], atributtes['coordinate'][0])
        length = haversine_distance(nearest_node['y'], nearest_node['x']), (atributtes['coordinate'][1], atributtes['coordinate'][0])
        g1.add_edge(node, nearest_node, length = length, time= length * 0.15 )

    return g1


def show(g: CityGraph) -> None:
    """Displays g in an interactive way""" 
    nx.draw(g, with_labels=True, node_color='red', node_size=400)
    plt.show()


def plotC(g1: buses.BusesGraph, g2: nx.Graph, filename: str) -> None:
    """Plots the CityGraph using g1 and g2"""
    map = staticmap.StaticMap(800, 800)
    buses.plot_buses(g1, map)
    plot_city(g2, map)
    image = map.render()  # We save the image in a file named filename
    image.save(filename)


def find_path_bus(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """Finds the shorter path to go from src to dst using time parameter"""

    start_node = ox.distance.nearest_nodes(ox_g, src[1], src[0])
    end_node = ox.distance.nearest_nodes(ox_g, dst[1], dst[0])

    path: Path = nx.shortest_path(g, source=start_node, target=end_node, weight= 'time')

    return path


def find_path_walk(ox_g: OsmnxGraph, g: nx.Graph, src: Coord, dst: Coord) -> Path:
    """Finds the shorter path to go from src to dst using time parameter"""

    start_node = ox.distance.nearest_nodes(ox_g, src[1], src[0])
    end_node = ox.distance.nearest_nodes(ox_g, dst[1], dst[0])

    path: Path = nx.shortest_path(g, source=start_node, target=end_node, weight= 'time')

    return path


def calculate_distance_path(g: CityGraph, path: Path) -> float:
    """Return the distance of path"""

    distance = 0.0
    node = 1
    # Go through all nodes in path
    while node < len(path): 
        distance += g.edges[path[node - 1], path[node]]['length']
        node += 1
    
    return distance


def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    """Saves an image named 'filename' with the plot of the path"""

    map = staticmap.StaticMap(800,800)
    index = 1
    while index < len(p):
        #We go through the nodes of the path
        dict_node = g.nodes[p[index]]
        coordinate_nodes = (dict_node['x'], dict_node['y'])
        map.add_marker(staticmap.CircleMarker(coordinate_nodes, 'red', 1))

        #We go through the edges of the path
        coord_source = (g.nodes[p[index - 1]]['x'], g.nodes[p[index-1]]['y'])
        coord_destination = (g.nodes[p[index]]['x'], g.nodes[p[index]]['y'])
        map.add_line(staticmap.Line([coord_source, coord_destination], 'blue', 1))
        index += 1

    image = map.render()
    image.save(filename)


def plot_interactive(filename:str)-> None:
    """Displays the file 'filename'"""
    try:
        plt.imshow(mpimg.imread(filename))
        plt.axis('off') # Removes the axis 
        plt.show()

    except FileNotFoundError:
        print("Arxiu no trobat")
    except IOError:
        print("Error durant la lectura de l'arxiu.")

def main() -> None:
    Busos = buses.create_busesgraph()
    Os = get_osmnx_graph()
    simple = get_simplified_graph(load_osmnx_graph('graf_barcelona.pickle'))

    City = build_city_graph(Os, simple, Busos)
    path1 = find_path_bus(Os, City, (2.2165149, 41.41027), (2.1981756, 41.3906222))
    path2 = find_path_walk(Os, simple, (2.2165149, 41.41027), (2.1981756, 41.3906222))


    print('1:', path1)
    print('2:', path2)


if __name__ == '__main__':
    main()
