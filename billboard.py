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
    for i in range(3):  # Iterating through three pages of Sensacine
    # Read and open the URL to scrape
        urlToScrape = "https://www.sensacine.com/cines/cines-en-72480/ " + str(i * 10 + 1)
        r = ur.urlopen(urlToScrape).read()
        soup = BeautifulSoup(r, "lxml")
        
        moviesList = soup.find_all('div', class_="item_resa")
        
        for moviesListItem in moviesList:
            # Extract theater name
            try:
                movieTheater = moviesListItem['data-theater']
                theaterName = movieTheater['name']
            except KeyError:
                theaterName = ''
            
            # Extract movie data
            try:
                movieData = moviesListItem['data-movie']
                movieTitle = movieData['title']
            except KeyError:
                movieTitle = ''
            
            # Extract data time
            try:
                movieTime = moviesListItem.find('em')['data-times']
            except KeyError:
                movieTime = ''

            # Print the extracted data
            print("Theater Name:", theaterName)
            print("Movie Title:", movieTitle)
            print("Movie Time:", movieTime)
            print("---")

