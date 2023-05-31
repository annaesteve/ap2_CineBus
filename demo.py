import requests
import bs4
import networkx
import osmnx
import haversine
import billboard
import city
import buses
import yogi
import cinemas
from tabulate import tabulate

def authors() -> None:
    """Writes the authors of the project"""
    print('Anna Esteve Gallifa i Cristina Teixidó Cruïlles')


def create_billboard() -> billboard.Billboard:
    """Creates today's billboard"""
    return billboard.read()


def show_billboard(B: billboard.Billboard)-> None:
    """Shows today's billboard"""
    films = [[film.title, film.genre] for film in B.films]
    headers = ['PEL·LÍCULA', 'GÈNERE']
    table = tabulate(films, headers, tablefmt = "fancy_grid", numalign = "center", stralign = "left")
    print(table)


def browse_billboard(l: list[billboard.Projection]) -> None:
    print('Títol: ', l[0].film.title)
    print('Gènere: ', l[0].film.genre)
    print('Director: ', *l[0].film.director)
    print('Actors: ', *l[0].film.actors, sep=",")

    films = [[projection.cinema.name, projection.cinema.address, str(projection.time[0])+ ':' + str(projection.time[1]), projection.language] for projection in l]
    headers = ['CINEMA', 'SITUACIÓ', 'HORA', 'IDIOMA']
    table = tabulate(films, headers, tablefmt = "fancy_grid", numalign = "center", stralign = "left")
    print(table)

def create_buses()-> buses.BusesGraph:
    """Crea el graf de les linies de busos de Barcelona"""
    return buses.define_nodes()

def show_buses(buses: buses.BusesGraph)-> None:
    """Mostra el graf de les linies de busos de Barcelona"""
    buses.show(buses)
    #buses.plot(G_buses, )

def get_city() -> city.OsmnxGraph:
    return city.get_osmnx_graph()

def create_city(g: city.OsmnxGraph, g1: city.CityGraph, g2: buses.BusesGraph) -> city.CityGraph:
    """Crea el graf de la ciutat de Barcelona amb les linies de busos corresponents"""
    return city.build_city_graph(g, g1, g2)

def show_city(g: city.CityGraph) -> None:
    city.show(g)

def search_cinema_coord(cinema: str) -> city.Coord:
    return cinemas.find_cinema_coord(cinema)
def find_distance(c: city.OsmnxGraph, City: city.CityGraph, src: city.Coord, dst: city.Coord) -> float:
    p: city.Path = city.find_path(c, City, src, dst)

    return city.calculate_distance_path(City, p)

def show_path(p: city.Path)-> None:
    """Mostra el cami  de ub1 a ub2 (cinema) per arribar a la que comenci abans"""
    city.show_path(p)

def main()-> None:
    billboard_created = False
    print("""
    1. Autores del projecte 
    2. Crear cartellera
    3. Mostrar cartellera
    4. Buscar pel·lícules segons el títol
    5. Crear graf dels busos de Barcelona
    6. Mostrar el graf dels busos de Barcelona
    7. Obtenir i guardar el graf dels carrers de Barcelona
    8. Mostrar el graf dels carrers de Barcelona
    9. Crear el graf dels carrers i dels busos de Barcelona
    10. Seleccionar la pel·lícula i el cinema desitjats
    11. Calcular la distància des de la teva ubicació
       al cinema on fan la pel·lícula escollida
    12. Mostrar el camí per arribar al cinema escollit""")
    
    for action in yogi.tokens(int):
        if action == 1:
            authors()

        elif action == 2:
            B = create_billboard()
            billboard_created = True
            print('Cartellera creada')

        
        elif action == 3:
            if billboard_created:
                show_billboard(B)
            else:
                print('Cartellera no creada')
        
        elif action == 4:
            if billboard_created:
                print("Escriu el títol de la pel·lícula que t'interessa")
                name = input()
                list = billboard.search_by_title(name, B)
                browse_billboard(list)
            
        elif action == 5:
            Buses: buses.BusesGraph= create_buses()
            print('Graf dels busos creat')

        
        elif action == 6:
            show_buses(Buses)

        elif action == 7:
            city.save_osmnx_graph(get_city(), 'graf_barcelona.pickle')
            print('Graf dels carrers de Barcelona creat')

        elif action == 8:
            show_city(City)

        elif action == 9:
            c = city.load_osmnx_graph('graf_barcelona.pickle')
            simple_graph = city.get_simplified_graph(c)
            City = create_city(c, simple_graph, Buses)
            print('Graf dels carrers i dels busos de Barcelona creat')

        elif action == 10:
            print('Escriu la pel·lícula que destija anar a veure ')
            selected_film = input()

            print('Escriu el cinema on desitja anar a veure la película: ', selected_film)
            selected_cinema = input()

            cinema: city.Coord = search_cinema_coord(selected_cinema)
            print('Cinema i pel·lícula trobats')

        
        elif action == 11:
            print('Escriu la teva ubicació en coordenades (UTM)')
            coord: city.Coord = (yogi.read(float), yogi.read(float))
            print('La ruta trobada té una distància de ', find_distance(c, City, coord, cinema)//1000, ' km.')

        elif action == 12:
            show_path
        else:
            print('Comanda no correcta')

if __name__ == '__main__':
    main()
