from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import urllib.request as ur
import networkx
import osmnx
import haversine
import staticmap

@dataclass 
class Film: 
    title: str
    genre: str
    director: str
    actors: list[str]
    ...

@dataclass 
class Cinema: 
    name: str
    address: str
    ...

@dataclass 
class Projection: 
    film: Film
    cinema: Cinema
    time: tuple[int, int]   # hora:minut
    language: str
    ...


@dataclass 
class Billboard: 
    films: list[Film]
    cinemas: list[Cinema]
    projections: list[Projection]

def read() -> Billboard:

    for i in range(0,2):        #recorrem les tres pàgines de Sensacine d'on treuem la informació
        #read and open url to scrape
        urlToScrape = "https://https://www.sensacine.com/cines/cines-en-72480/ " + str(i * 10 + 1)"
        r = ur.urlopen(urlToScrape).read()
        soup = BeautifulSoup(r, "lxml")

def search_by_name(name: str) -> list[Projection]:
    """ Given a name, returns a list of the projections
        that include this name in the title of the film"""
    
