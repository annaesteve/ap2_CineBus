import requests
import bs4
import networkx
import osmnx
import haversine
import billboard
import city
import buses
import yogi
from tabulate import tabulate

def authors() -> None:
    """Writes the authors of the project"""
    print('Anna Esteve Gallifa i Cristina Teixidó Cruïlles')


def create_billboard()-> billboard.Billboard:
    """Creates today's billboard"""
    return billboard.read()


def show_billboard(B: billboard.Billboard)-> None:
    """Shows today's billboard"""
    films = [[projection.film.title, projection.film.genre, projection.cinema.name] for projection in B.projections]
    headers = ['PEL·LÍCULA', 'GÈNERE', 'CINEMA']
    table = tabulate(films, headers, tablefmt = "fancy_grid", numalign = "center", stralign = "left")
    print(table)


def cercar_cartellera():
    ...


def crear_buses()-> buses.BusesGraph:
    """Crea el graf de les linies de busos de Barcelona"""
    return buses.define_nodes()


def mostrar_graf_buses(G_buses: buses.BusesGraph)-> None:
    """Mostra el graf de les linies de busos de Barcelona"""
    buses.show(G_buses)
    #buses.plot(G_buses, )


def crear_ciutat()-> city.CityGraph:
    """Crea el graf de la ciutat de Barcelona amb les linies de busos corresponents"""
    city.build_city_graph(city.load_osmnx_graph(str), buses.crear_buses()) #COMPLETAR STR


def mostrar_cami(ub1: city.Coord, ub2: city.Coord)-> city.Path:
    """Mostra el cami  de ub1 a ub2 (cinema) per arribar a la que comenci abans"""
    city.find_path(g, crear_ciutat()) #QUÈ ÉS G?'

def main()-> None:
    billboard_created = False
    print("""
    1. Autores del projecte 
    2. Mirar cartellera""")
    for action in yogi.tokens(int):
        if action == 1:
            authors()
        elif action == 2:
            B = create_billboard()
            billboard_created = True
        elif action == 3:
            if billboard_created:
                show_billboard(B)
            else:
                print('Cartellera no creada')
        elif action == 2:
            ...
        elif action == 3:
            ...
        elif action == 2:
            ...
        else:
            print('Comanda no correcta')

if __name__ == '__main__':
    main()
