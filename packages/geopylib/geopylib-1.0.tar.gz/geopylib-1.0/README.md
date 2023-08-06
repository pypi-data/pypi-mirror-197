geopylib
==============

#### Esse é um pacote que permite realizar diversas funcionalidades relacionadas a mapas geográficos.

## Instalação:
    pip install geopylib

## Uso:

...
import geopylib as gl

## O programa permite ao usuário:

visualizar um mapa com uma latitude, longitude e nível de zoom específicos;
adicionar marcadores ao mapa;
calcular a distância entre dois pontos no mapa;
recuperar dados meteorológicos de um determinado local;
converter um endereço ou coordenadas para seu formato oposto.

## O programa usa as seguintes classes:

Mapa: da biblioteca Folium, representa um mapa;
Coordenada: representa um par de latitude e longitude;
Localização: representa uma localização com um endereço e coordenadas;
OSMGeocoder: da biblioteca geopy, é usado para recuperar um objeto Location de um endereço.