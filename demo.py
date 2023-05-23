import requests
import bs4
import networkx
import osmnx
import haversine
import staticmap
import billboard
import city
import buses


def autors() -> None:
    """Escriu els noms dels autors"""
    print('Anna Esteve Gallifa i Cristina Teixidó Cruïlles')


def crear_cartellera()-> billboard.Billboard:
    """Crea la cartellera del dia d'avui"""
    return billboard()


def mostrar_contingut_cartellera(B: Billboard)-> None:
    """Mostra el contingut de la cartellera B"""


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
