from typing import TypeAlias, Tuple

Coord : TypeAlias = Tuple[float, float]   # (longitude, latitude)

def find_cinema_coord(cinema: str) -> Coord:
    if cinema == "Arenas Multicines 3D":
        return (2.149245, 41.3764221)
    
    elif cinema == "Aribau Multicines":
        return (2.162593, 41.386125)
    
    elif cinema == "Bosque Multicines":
        return (2.1518736, 41.4014918)

    elif cinema == "Cinema Comedia":
        return (2.1675839, 41.3895914)

    elif cinema == "Cinemes Girona":
        return (2.1645592, 41.3996576)
    
    elif cinema == "Cines Verdi Barcelona":
        return(2.1568812, 41.4040137)
    
    elif cinema == "Cinesa Diagonal 3D":
        return(2.1362351, 41.3938123)

    elif cinema == "Cinesa Diagonal Mar 18":
        return(2.2165149, 41.41027)

    elif cinema == "Cinesa La Maquinista 3D":
        return(2.1983539, 41.4395825)

    elif cinema == "Cinesa SOM Multiespai":
        return(2.1807818, 41.4354238)

    elif cinema == "Glòries Multicines":
        return(2.1926764, 41.4052789)

    elif cinema == "Gran Sarrià Multicines":
        return(2.1340126, 41.3948315)

    elif cinema == "Maldá Arts Forum":
        return(2.1738965, 41.3831691)

    elif cinema == "Renoir Floridablanca":
        return(2.1625471, 41.3816986)

    elif cinema == "Sala Phenomena Experience":
        return(2.1718111, 41.4090888)

    elif cinema == "Yelmo Cines Icaria 3D":
        return(2.1981756, 41.3906222)

    elif cinema == "Boliche Cinemes":
        return(2.1536348, 41.3953189)

    elif cinema == "Zumzeig Cinema":
        return(2.14507, 41.377347)

    elif cinema == "Balmes Multicine":
        return(2.1386111, 41.4072222)

    elif cinema == "Cinesa La Farga 3D":
        return(2.1047766, 41.3631793)

    elif cinema == "Filmax Gran Via 3D":
        return(2.1284869, 41.3583703)

    else:
        print("El cinema introduït és incorrecte.")
