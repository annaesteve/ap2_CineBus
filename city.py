from typing import TypeAlias, Tuple
import matplotlib.pyplot as plt 
import networkx as nx
import osmnx as ox
import pickle
import os
import staticmap
import matplotlib.image as mpimg

CityGraph : TypeAlias = nx.Graph
BusesGraph: TypeAlias = nx.Graph
OsmnxGraph: TypeAlias = nx.MultiDiGraph
Coord : TypeAlias = Tuple[float, float]   # (longitude, latitude)
Path: TypeAlias = list[int]         # list of nodes


def get_osmnx_graph() -> OsmnxGraph:
    graph = ox.graph_from_place("Barcelona, Spain", network_type='all', truncate_by_edge=True)
    graph.graph['crs'] = 'EPSG:32631' #we determine coordinate's system 
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


def plot_city(g:nx.Graph, filename: str) -> None:
    """Saves g in a file named filename as an image with a map of the city as backgroung"""
    map = staticmap.StaticMap(800,800)
    #We go through all nodes to draw the crosses
    for _, data in g.nodes(data=True): 
        coordinate = (data['x'], data['y'])
        map.add_marker(staticmap.CircleMarker(coordinate, 'red', 1))

    #We go through all edges to draw the streets
    for source, destination in g.edges():
        coord_source = (g.nodes[source]['x'], g.nodes[source]['y'])
        coord_destination = (g.nodes[destination]['x'], g.nodes[destination]['y'])
        map.add_line(staticmap.Line([coord_source, coord_destination], 'blue', 1))

    image = map.render() #We save the image in a file named 'filename'
    image.save(filename)


def build_city_graph(g: OsmnxGraph, g1: nx.Graph, g2: BusesGraph) -> CityGraph:
    """Returns the graph of composing g1 and g2"""
    g1.add_nodes_from(g2.nodes(data=True))
    g1.add_edges_from(g2.edges(data=True))

    for node, atributtes in g2.nodes(data=True):
        nearest_node = ox.distance.nearest_nodes(g, atributtes['coordinate'][0], atributtes['coordinate'][1])
        g1.add_edge(node, nearest_node, length= 0.0)

    print(g1.nodes(data = True))
    return g1


def show(g: CityGraph) -> None:
    """Displays g in an interactive way""" 
    nx.draw(g, with_labels=True, node_color='red', node_size=400)
    plt.show()


#def plot_city_buses(g: CityGraph, filename: str) -> None:
#   """Saves city and buses in a file named filename as an image with a map of the city as backgroung"""


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """Finds the shorter path to go from src to dst"""
    start_node = ox.distance.nearest_nodes(ox_g, src[0], src[1])
    end_node = ox.distance.nearest_nodes(ox_g, dst[0], dst[1])

    path: Path = nx.shortest_path(g, source=start_node, target=end_node, weight= 'lenght')

    return path


def calculate_distance_path(g: CityGraph, path: Path) -> float:
    """Return the distance of path"""
    distance = 0.0

    node = 1
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
        plt.axis('off')
        plt.show()

    except FileNotFoundError:
        print("Arxiu no trobat")
    except IOError:
        print("Error durant la lectura de l'arxiu.")
