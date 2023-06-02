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

#### Classe `Stop`:
```ruby
@dataclass
class Line:
    nom: str
    stops: list[Stop]
```
Aquesta classe representa una línia de bus. Amb el seu nom i totes les parades d'aquesta línia.

### Funcions

## Mòdul City
## Mòdul Demo
