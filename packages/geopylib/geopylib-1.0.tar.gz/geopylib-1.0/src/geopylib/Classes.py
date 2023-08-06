import folium

class Map:
    """
    Essa classe representa um mapa gerado pela biblioteca Folium.
    """
    def __init__(self, center, zoom):
        """
        Construtor que cria uma instância de Map, especificando o centro do mapa e o zoom inicial.
        Parâmetros:
            center (tuple): Tupla com as coordenadas de latitude e longitude do centro do mapa.
            zoom (int): Nível de zoom inicial do mapa.
        Return: None
        """
        self.center = center
        self.zoom = zoom
        self.layers = []

    def add_layer(self, layer):
        """
        Adiciona uma camada ao mapa.
        Parâmetros:
            layer: Camada a ser adicionada ao mapa.
        Return: None
        """
        self.layers.append( layer )

    def remove_layer(self, layer):
        """
        Remove uma camada do mapa.
        Parâmetros:
            layer: Camada a ser removida do mapa.
        Return: None
        """
        self.layers.remove( layer )

    def set_zoom(self, zoom):
        """
        Define o nível de zoom do mapa.
        :param zoom: int
            Nível de zoom a ser definido.
        :return: None
        """
        self.zoom = zoom

    def set_center(self, center):
        """
        Define o centro do mapa.
        Parâmetros:
            center (tuple): Tupla com as coordenadas de latitude e longitude do novo centro do mapa.
        Return: None
        """
        self.center = center

    def create_marcador(self, lat, lon, titulo):
        """
        Cria um marcador em uma posição específica do mapa.
        Parâmetros:
            lat (float): Latitude da posição do marcador.
            lon (float): Longitude da posição do marcador.
            titulo (str): Título do marcador.
        Return: Um objeto Marker da biblioteca Folium.
        """
        marker = folium.Marker( location=[lat, lon], popup=titulo )
        return marker

    def show(self):
        """
        Exibe o mapa.
        Parâmetros: None
        Return: Um objeto Map da biblioteca Folium.
        """
        m = folium.Map( location=[self.center[0], self.center[1]], zoom_start=self.zoom )
        for layer in self.layers:
            m.add_child( layer )
        return m
    
    def create_map(self):
        """
        Cria um mapa em formato HTML.
        Parâmetros: None.
        Return: Uma string contendo o código HTML do mapa.
        """
        m = folium.Map(location=self.center, zoom_start=self.zoom)
        for layer in self.layers:
            m.add_child(layer)
        html = m.get_root().render()
        return html
    
import math

class Coordinate:
    """ 
    Essa classe representa uma coordenada geográfica.
    """
    def __init__(self, lat, lon, alt=None):
        """
        Construtor que cria uma instância de Coordinate, especificando a latitude, longitude e altitude (opcional) da coordenada.
        Parâmetros:
            lat (float): Latitude da coordenada.
            lon (float): Longitude da coordenada.
            alt (float, opcional): Altitude da coordenada. Valor padrão é None.
        Return: None
        """
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
        
    def distance(self, other):
        """
        Calcula a distância entre duas coordenadas.
        Parâmetros:
            other (Coordinate): Outra coordenada para a qual a distância será calculada.
        Return: A distância em quilômetros entre as duas coordenadas.
        """
        # calcula a distância entre esta coordenada e outra, usando o algoritmo especificado
        # fórmula de Haversine para distância entre dois pontos em uma esfera (como a Terra)
        R = 6371  # raio médio da Terra em quilômetros
        d_lat = math.radians(other.latitude - self.latitude)
        d_lon = math.radians(other.longitude - self.longitude)
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(other.latitude)
        a = math.sin(d_lat/2)**2 + math.sin(d_lon/2)**2 * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
import requests

class Location:
    """
    Essa classe representa uma localização geográfica, incluindo informações sobre o clima.
    """
    def __init__(self, name, address, latitude, longitude):
        """
        Construtor que cria uma instância de Location, especificando o nome, endereço, latitude e longitude da localização.
        Parâmetros:
            name (str): Nome da localização.
            address (str): Endereço da localização.
            latitude (float): Latitude da localização.
            longitude (float): Longitude da localização.
        Return: None
        """
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = None
        self.humidity = None
        self.pressure = None

    def set_weather(self, api_key,lat,lon):
        """
        O método obtém informações sobre o clima na localização usando uma API do OpenWeatherMap
        Parâmetros:
            api_key (str): a chave de API para acessar o OpenWeatherMap.
            lat (float): a latitude da localização.
            lon (float): a longitude da localização.
        Return: None
        """
        #url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if 'main' in data:
            self.temperature = data["main"]["temp"]
            self.humidity = data["main"]["humidity"]
            self.pressure = data["main"]["pressure"]
        else:
            self.temperature = None
            self.humidity = None
            self.pressure = None

    def get_coordinates(self):
        """
        O método retorna as coordenadas de latitude e longitude
        Parâmetros: None
        Return: uma tupla com a latitude e longitude da localização.
        """
        return self.latitude, self.longitude
import requests
import json

class OSMGeocoder:
    """
    Realizar a codificação e decodificação de endereços usando o serviço OpenStreetMap Nominatim
    """
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"

    def geocode(self, address):
        """
        Faz uma requisição GET para a API de geocodificação do OSM
        Parametros:
            address (str): endereço de entrada
        Return: as coordenadas latitude e longitude do endereço, caso encontrado 
        Caso contrário 
        Return: None
        """
        params = {
            "q": address,
            "format": "json",
            "addressdetails": 1
        }
        response = requests.get(self.base_url, params=params)
        data = json.loads(response.text)
        if data:
            location = data[0]
            return location["lat"], location["lon"]
        else:
            return None
     
    def reverse_geocode(self, latitude, longitude):
        """
        Faz uma requisição GET para a API de reverso-geocodificação do OSM
        Parâmetros:
            latitude (float): a latitude da localização.
            longitude (float): a longitude da localização.
        Return: o nome do estado e da rua correspondentes às coordenadas, caso encontrado. 
        Caso contrário, 
        Return: (None, None)
        """
        self.url = "https://nominatim.openstreetmap.org/reverse"
        try:
            response = requests.get(
                self.url,
                params={"format": "json", "lat": latitude, "lon": longitude}
            )
            if response.ok:
                data = response.json()
                address = data.get("address")
                if address:
                    state = address.get("state")
                    if not state:
                        state = address.get("state_district")
                    if not state:
                        state = address.get("region")
                    if not state:
                        state = address.get("county")
                    if not state:
                        state = address.get("city")
                    if not state:
                        state = address.get("town")
                    if not state:
                        state = address.get("village")
                    if not state:
                        state = address.get("hamlet")
                    if not state:
                        state = address.get("island")
                    
                    road = address.get("road")
                    if road:
                        return state, road
                    else:
                        return None, None
                else:
                    return None, None
            else:
                response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"HTTP error: {error}")
        except requests.exceptions.RequestException as error:
            print(f"Request error: {error}")