from dataclasses import dataclass
from bs4 import BeautifulSoup
import urllib.request as ur
import requests
import json

@dataclass
class Film:
    title: str
    genre: str
    director: str
    actors: list[str]

@dataclass
class Cinema:
    name: str
    address: str

@dataclass
class Projection:
    film: Film
    cinema: Cinema
    time: tuple[int, int]
    language: str

@dataclass
class Billboard:
    films: list[Film]
    cinemas: list[Cinema]
    projections: list[Projection]

def read() -> Billboard:
    lfilms: list[Film] = list()
    lcinemas: list[Cinema] = list()
    lprojections: list[Projection] = list()

    for i in range(3):  # Iterating through three pages of Sensacine
        urlToScrape = "https://www.sensacine.com/cines/cines-en-72480/"
        req = ur.Request(urlToScrape, headers={'User-Agent': 'Chrome/35.0.1916.47'})
        r = ur.urlopen(req)
        soup = BeautifulSoup(r, "lxml")
        moviesList = soup.find_all('div', class_="item_resa")
        
        for moviesListItem in moviesList:
            # Extract theater name
            try:
                movieTheater = moviesListItem["data-theater"]
                theaterName = movieTheater["name"]
                cinema = Cinema(theaterName, '')
                lcinemas.append(cinema)
            except KeyError:
                theaterName = ""
            
            # Extract movie data
            try:
                movieData = moviesListItem["data-movie"]
                movieTitle = movieData["title"]
                movieGenre = movieData["genre"]
                movieDirector = movieData["directors"][0]
                movieActors = movieData["actors"]
                film_ = Film(movieTitle, movieGenre, movieDirector, movieActors)
                lfilms.append(film_)
            except KeyError:
                print("aqui")
                movieTitle = ""
            
            # Extract data time
            print(lfilms)
            try:
                movieTime = json.loads(moviesListItem.find('em')['data-times'])
                hour, minute = movieTime[0].split(':')
                hour = int(hour)
                minute = int(minute)
                time_tuple = hour, minute
            except (KeyError, json.JSONDecodeError, AttributeError):
                time_tuple = 0,0
            
            # Create objects and add to the projections list
           
            projection = Projection(film_, cinema, time_tuple, '')
            lprojections.append(projection)

    return Billboard(lfilms, lcinemas, lprojections)

def search_by_name(name: str) -> list[Projection]:
    """ Given a name, returns a list of the projections
        that include this name in the title of the film"""

def main() -> None:
    billboard = read()

if __name__ == '__main__':
    main()
