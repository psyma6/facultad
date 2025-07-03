# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user



# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP (Pokemon).
def getAllImages():
    
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    imagenescrudas = transport.getAllImages()  # La variable imagenescrudas llama a la funcion getAllImages del modulo transport
    cards = []
    
    # 2) convertir cada img. en una card.
    for crudo in imagenescrudas:   #recorre cada Pokémon crudo (crudo) de la lista imagenescrudas
        card = translator.fromRequestIntoCard(crudo)  # se conviente cada "crudo" que esta en formato JSON, en Card (tarjeta)
        
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
        cards.append(card)
    return cards #cuando el bucle termina de analizar todos los archivos crudo, devuelve las tarjetas



# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():  # se define un bucle for que para cada card en la funcion getAllImages
    # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():
            filtered_cards.append(card)#Si es true se agrega la card a la variable filtered_cards
    return filtered_cards



# función que filtra las cards según su tipo: agua, fuego, ...
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():     # debe verificar si el elemento de la card coincide con el parametro solicitado.
        if type_filter.lower() in [t.lower() for t in card.types]: #lo convierte a minusculas para evitar errores,y
                                                                    #verifica si esta en el listado de tipo de Pokemons.
            filtered_cards.append(card)   #Si sale true, se agrega las tarjetas al listado filtered cards.
    return filtered_cards



# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)