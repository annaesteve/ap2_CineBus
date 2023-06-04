import billboard
import city
import buses
import yogi
import cinemas
from tabulate import tabulate
from typing import Optional


def authors() -> None:
    """Writes the authors of the project"""
    print('Anna Esteve Gallifa i Cristina Teixidó Cruïlles')


def create_billboard() -> billboard.Billboard:
    """Creates today's billboard"""
    return billboard.read()


def show_billboard(B: billboard.Billboard) -> None:
    """Shows today's billboard"""
    films = [[film.title, film.genre] for film in B.films]
    headers = ['PEL·LÍCULA', 'GÈNERE']
    table = tabulate(
        films,
        headers,
        tablefmt="fancy_grid",
        numalign="center",
        stralign="left")
    print(table)


def browse_billboard(llista: list[billboard.Projection]) -> None:
    """Prints a table with the information of the film choosen"""
    print('Títol: ', llista[0].film.title)
    print('Gènere: ', llista[0].film.genre)
    print('Director: ', ', '.join(llista[0].film.director))
    print('Actors: ', ', '.join(llista[0].film.actors))

    films = [[projection.cinema.name,
              projection.cinema.address,
              str(projection.time[0]) + ':' + str(projection.time[1]),
              projection.language] for projection in llista]
    headers = ['CINEMA', 'SITUACIÓ', 'HORA', 'IDIOMA']
    table = tabulate(
        films,
        headers,
        tablefmt="fancy_grid",
        numalign="center",
        stralign="left")
    print(table)


def create_buses() -> buses.BusesGraph:
    """Crea el graf de les linies de busos de Barcelona"""
    return buses.create_busesgraph()


def get_city() -> city.OsmnxGraph:
    """Return the graph of the streets of Barcelona"""
    return city.get_osmnx_graph()


def create_city(g: city.OsmnxGraph, g1: city.CityGraph,
                g2: buses.BusesGraph) -> city.CityGraph:
    """Crea el graf de la ciutat de Barcelona amb les linies
    de busos corresponents"""
    return city.build_city_graph(g, g1, g2)


def search_cinema_coord(cinema: str) -> Optional[city.Coord]:
    return cinemas.find_cinema_coord(cinema)


def find_path(c: city.OsmnxGraph, City: city.CityGraph,
              src: city.Coord, dst: city.Coord) -> city.Path:
    return city.find_path(c, City, src, dst)


def find_distance(City: city.CityGraph, p: city.Path) -> float:
    return city.calculate_distance_path(City, p)


def introduction(name_user: str) -> None:
    """Prints the introduction of the project"""

    print("""
    Benvigut/da""", name_user, """al projecte:
    ELS 13 MANAMENTS""")

    print("""
    Aquest projecte té les següents funcions possibles:

    1. Autores del projecte
    2. Crear cartellera
    3. Mostrar cartellera
    4. Buscar pel·lícules segons el títol
    5. Crear graf dels busos de Barcelona
    6. Mostrar el graf dels busos de Barcelona
    7. Obtenir i guardar el graf dels carrers de Barcelona
    8. Crear el graf dels carrers i dels busos de Barcelona
    9. Mostrar el graf dels carrers i dels busos de Barcelona
    10. Seleccionar la pel·lícula i el cinema desitjats
    11. Crear el camí més curt per anar fins al cinema escollit
    12. Calcular la distància des de la teva ubicació
       al cinema on fan la pel·lícula escollida
    13. Mostrar el camí per arribar al cinema escollit

    """)

    print("     ", name_user, ",",
          " escrigui el nombre de l'acció "
          "que desitja que aquest projecte faci: ",
          sep="")


def actions(name_user: str) -> None:
    """Does the action that the user selects"""

    for action in yogi.tokens(str):
        if action == '1':
            authors()

        elif action == '2':
            B = create_billboard()
            print('     Cartellera creada')

        elif action == '3':
            try:
                show_billboard(B)

            except BaseException:
                print("     La cartellera encara s'ha creat.",
                      "Pulsi 2 per fer-ho.")

        elif action == '4':
            try:
                print("     ", name_user, ",",
                      " escrigui el títol de la pel·lícula que li interessa",
                      sep="")
                name = input()
                list = billboard.search_by_title(name, B)
                browse_billboard(list)

            except BaseException:
                print("     La cartellera encara s'ha creat.",
                      "Pulsi 2 per fer-ho.")

        elif action == '5':
            Buses: buses.BusesGraph = create_buses()
            print('     Graf dels busos creat')

        elif action == '6':
            try:
                buses.plotB(Buses, 'graf_buses.png')
                city.plot_interactive('graf_buses.png')

            except BaseException:
                print("     Encara no s'ha creat el graf dels busos. "
                      "Pulsi 5 per fer-ho.")

        elif action == '7':
            city.save_osmnx_graph(get_city(), 'graf_barcelona.pickle')
            print('     Graf dels carrers de Barcelona creat')

        elif action == '8':
            try:
                c = city.load_osmnx_graph('graf_barcelona.pickle')
                simple_graph = city.get_simplified_graph(c)
                City = create_city(c, simple_graph, Buses)
                print('     Graf dels carrers i dels busos de Barcelona creat')

            except BaseException:
                print("     Encara no s'ha creat el graf dels carrers "
                      "de Barcelona. Pulsi 7 per fer-ho. ")

        elif action == '9':
            try:
                city.plotC(
                    Buses,
                    city.get_simplified_graph(
                        city.load_osmnx_graph('graf_barcelona.pickle')),
                    'graf_buses_city.png')
                city.plot_interactive('graf_buses_city.png')

            except BaseException:
                print("     Encara no s'ha creat el graf dels carrers i dels "
                      "busos de Barcelona. Pulsi 8 per fer-ho.")

        elif action == '10':
            print("     ", name_user, ",",
                  " escrigui la pel·lícula que destija anar a veure ", sep="")
            selected_film = input()

            print("     ", name_user, ",",
                  " escrigui el cinema on desitja anar a veure la película: ",
                  selected_film, sep="")
            selected_cinema = input()

            cinema: Optional[city.Coord] = search_cinema_coord(selected_cinema)

            while cinema is None:
                print("     ", name_user, ",",
                      " torni a introduir el nom del cinema: ", sep="")
                selected_cinema = input()
                cinema = search_cinema_coord(selected_cinema)

            print('     Cinema i pel·lícula trobats')

        elif action == '11':
            try:
                print("     ", name_user, ",",
                      " escrigui la seva ubicació en coordenades"
                      " (longitud, latitud)", sep="")
                coord: city.Coord = (yogi.read(float), yogi.read(float))
                if cinema is not None:
                    path: city.Path = find_path(c, City, coord, cinema)
                    print('     Camí creat')

            except BaseException:
                print("     Encara no s'ha creat el graf dels carrers i "
                      "dels busos de Barcelona. Pulsi 8 per fer-ho.")

        elif action == '12':
            try:
                print('     La ruta trobada té una distància de ',
                      find_distance(City, path) // 1000, ' km.')

            except BaseException:
                print("     Encara no s'ha creat el camí determinat. "
                      "Pulsi 11 per fer-ho")

        elif action == '13':
            try:
                city.plot_path(City, path, 'path.png')
                city.plot_interactive('path.png')

            except BaseException:
                print("     Encara no s'ha creat el camí determinat")

        else:
            print('     Comanda no correcta')
            print("     ", name_user, ",",
                  " introdueixi un valor vàlid", sep="")


def main() -> None:
    print("     Introdueixi el seu nom: ")
    name_user = input()

    introduction(name_user)
    actions(name_user)


if __name__ == '__main__':
    main()
