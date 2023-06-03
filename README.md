# PRÀCTICA 2: CineBus
## Introducció
Aquesta pràctica permet als barcelonins trobar una pel·lícula d'acord a les seves preferències i els ensenya com arribar al cinema que la mostri el més aviat possible en desplaçaments en bus i a peu.
La pràctica consta de 4 mòduls:
- `billboard.py`: conté el codi relacionat amb l'obtenció de la cartellera i cerques relacionades.
- `buses.py`: conté el codi relacionat amb la construcció del graf de busos.
- `city.py`: conté el codi relacionat amb la construcció del graf de la ciutat i la cerca de rutes entre punts de la ciutat.
- `demo.py`: conté un programa de demostració (utilitza els anteriors mòduls).

## Mòdul `Billboard`
La funció principal d'aquest mòdul és llegir les dades de la cartellera de cinemes de Barcelona del dia actual i cercar-les.

### Classes
En aquest mòdul utilitzem 4 classes diferents:
#### Classe `Film`:
Cada pel·lícula la desem en aquest tipus de dada, que consta de 4 atributs:
```ruby
@dataclass
class Film:
    title: str
    genre: str
    director: str
    actors: list[str]
```
#### Classe `Cinema`:
Guardem els diferents cinemes de Barcelona (ciutat) en la classe Cinema:
```ruby
@dataclass
class Cinema:
    name: str
    address: str
```
#### Classe`Projection`:
Per cada pel·lícula creem una Projection on guardem els diferents cines, horaris i idiomes que es fa la pel·lícula:
```ruby
@dataclass
class Projection:
    film: Film
    cinema: Cinema
    time: tuple[int, int]
    language: str
```
#### Classe `Billboard`:
Finalment per crear la cartellara utilitzem la classe Billboard, que consta de 3 llistes: una de Films, una de Cinema i una de Projection.
```ruby
@dataclass
class Billboard:
    films: list[Film]
    cinemas: list[Cinema]
    projections: list[Projection]
```
### Funcions
Dins d'aquest mòdul s'han creat dues funcions:
```ruby
def read() -> Billboard:
```
Aquesta funció extreu les dades de les pel·lícules i cinemes de les següents pàgines webs (web scraping): 
* https://www.sensacine.com/cines/cines-en-72480/?page=1
* https://www.sensacine.com/cines/cines-en-72480/?page=2
* https://www.sensacine.com/cines/cines-en-72480/?page=3

Amb aquestes dades crea un Billboard, amb totes les projeccions, cinemes i pel·lícules del dia actual.

```ruby
def search_by_title(name: str, B: Billboard) -> list[Projection]:
```
La funció search_by_title retorna totes les projeccions de la pel·lícula "name". S'utilitza més endavant, en el mòdul `demo.py`. 

### Consideracions
* Només s'han tingut en compte les pel·lícules i cinemes que es troben a la ciutat de Barcelona (no considerem tota l'Àrea metropolitana de Barcelona).

## Mòdul `Buses`
La funció principal d'aquest mòdul és crear un graf de busos a partir de les dades de la informació de les línies d'autobusos i les seves parades. 

Aquest graf de busos conté informació sobre les parades (els nodes), les línies (les arestes) i els trajectes dels autobusos.

### Classes
En aquest mòdul utilitzem dues classes:
#### Classe `Stop`:
```ruby
@dataclass
class Stop:
    name: str
    line: list[str]
    coordinate: Tuple[float, float]
    node: int
```
Cada node del graf de busos és una dada Stop, on guardem el nom de l'estació, les línies que paren a la parada, les seves coordenades i un "id" del node.

#### Classe `Line`:
```ruby
@dataclass
class Line:
    nom: str
    stops: list[Stop]
```
Aquesta classe representa una línia de bus. Amb el seu nom i totes les parades d'aquesta línia.

### Funcions
Utilitzem cinc funcions:

```ruby
def haversine_distance(src: Tuple[float, float], dst: Tuple[float, float]) -> float:
```
Aquesta calcula la distancia entre dues coordenades (src i dst)

```ruby
def create_stop(parada: dict[str, str], num_node: int) -> Stop:
```
`create_stop` crea cada parada de bus (sense encara atribuir-la com un node del graf de busos).

```ruby
def create_busesgraph() -> BusesGraph:
```
És la funció principal d'aquest mòdul, fa el web scraping i va afegint cada node i aresta en un networkx.Graph (BusesGraph).

```ruby
def show(g: BusesGraph) -> None:
```
Mostra el graf de busos de forma interactiva.

```ruby
def plot_buses(g: BusesGraph, nom_fitxer: str) -> None:
```
Aquesta funció guarda en un fitxer anomenat 'nom_fitxer' el graf de busos amb el mapa de Barcelona de fons.

### Consideracions
* Hem seleccionat les línies de bus de manera que en el graf només apareixin les del municipi de Barcelona. 

## Mòdul `City`
El mòdul city és el responsable de proporcionar el graf de ciutat que representa tota la informació necessària per saber anar d'una cruïlla de la ciutat de Barcelona a una altre de la forma més ràpida possible a peu o en bus. El graf de ciutat és un graf no dirigit resultat de la fusió de dos altres grafs: el graf dels carrers de Barcelona (proporcionat pel mòdul osmnx) i el graf de busos (proporcionat pel mòdul buses). El graf de ciutat és del tipus networkx.Graph.

### Funcions
En aquest mòdul hem creat diverses funcions:
### Funcions pel graf de carrers de Barcelona
```ruby
def get_osmnx_graph() -> OsmnxGraph:
def get_simplified_graph(g: OsmnxGraph) -> nx.Graph:
def save_osmnx_graph(g: OsmnxGraph, file_name: str) -> None:
def load_osmnx_graph(file_name: str) -> OsmnxGraph:
def plot_city(g:nx.Graph, filename: str) -> None:

```
Aquestes serveixen per crear, simplificar el graf (passar d'un graf d'osmnx a un de networkx) , guardar-lo a l'ordinado, pujar-lo i guardar-lo amb el mapa de Barcelona de fons, respectivament.

### Funcions pel graf de ciutat
```ruby
def build_city_graph(g: OsmnxGraph, g1: nx.Graph, g2: BusesGraph) -> CityGraph:
def show(g: CityGraph) -> None:
def plot_city_buses(g: CityGraph, filename: str) -> None:
```
La primera crea el graf de la fusió dels altres dos, la següent mostra interectivament el graf i finalment, `plot_city_buses` mostra el graf amb el mapa de Barcelona de fons.


### Funions pel path
```ruby
def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
def calculate_distance_path(g: CityGraph, path: Path) -> float:
def plot_path(g: CityGraph, p: Path, filename: str) -> None:
```
Aquestes, creen, calculen la distància i mostren el camí més curt des de src (l'actual ubicació) a dst (l'ubicació del cinema).

### Altres funcions
```ruby
def plot_interactive(filename:str)-> None:
```
Aquesta funció serveix per mostrar de manera interactiva un dels anteriors graf (de qualsevol mòdul).

## Mòdul `demo`
El mòdul demo conté un programa per provar les funcionalitats dels altres mòduls utilitzant un simple sistema de menús. Té les següents funcionalitats:

* Mostrar el nom del les autores del projecte.
* Crear la cartellera.
* Mostrar el contingut de la cartellera.
* Cercar a la cartellera (segons el títol).
* Crear el graf de busos.
* Mostrar el graf de busos.
* Crear i guardar el graf dels carrers de Barcelona.
* Crear el graf de ciutat (busos + carrers).
* Mostrar el graf de ciutat.
* Crear el camí més curt 
* Calcular la distància del camí més curt.
* Mostrar el camí més curt.

## Autores
Anna Esteve Gallifa i Cristina Teixidó
