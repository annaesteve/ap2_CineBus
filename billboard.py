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

    for _ in range(3):  # Iterating through three pages of Sensacine
        urlToScrape = "https://www.sensacine.com/cines/cines-en-72480/"
        req = ur.Request(urlToScrape, headers={'User-Agent': 'Chrome/35.0.1916.47'})
        r = ur.urlopen(req)
        soup = BeautifulSoup(r, "lxml")
        moviesList = soup.find_all('div', class_="item_resa")
        
        for movie in moviesList:
            # Extract film information
            film_data = movie.find('div', class_='j_w').get('data-movie')
            film_info = json.loads(film_data)
            title = film_info['title']
            genre = film_info['genre']
            directors = film_info['directors']
            actors = film_info['actors']

            # Extract cinema and time information
            cinema_data = movie.find('div', class_='j_w').get('data-theater')
            cinema_info = json.loads(cinema_data)
            cinema_name = cinema_info['name']
            cinema_address = cinema_info['city']

            time_element = movie.find('ul', class_='list_hours').find('em')
            times = json.loads(time_element.get('data-times'))

            # Create Film object
            film = Film(title, genre, directors, actors)

            # Create Cinema object
            cinema = Cinema(cinema_name, cinema_address)

            # Create Projection object
            projection = Projection(film, cinema, (times[0].split(':')[0], times[0].split(':')[1]), language='')

            # Add objects to the respective lists
            lfilms.append(film)
            lcinemas.append(cinema)
            lprojections.append(projection)

    print(lprojections)
    # Create Billboard object
    billboard = Billboard(films=lfilms, cinemas=lcinemas, projections=lprojections)
    
    return billboard


#def search_by_name(name: str) -> list[Projection]:
    """ Given a name, returns a list of the projections
        that include this name in the title of the film"""

def main() -> None:
    billboard = read()

if __name__ == '__main__':
    main()
