import re
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from tela_mapa import Tela_mapa
from tela_main import Tela_main
from tela_marcador import Tela_marcador
from tela_calc_dist import Tela_calc_dist
from tela_dados_meteoro import Tela_dados_meteoro
from tela_conversor import Tela_conversor

from Classes import Map, Coordinate, Location, OSMGeocoder
import webbrowser

class UiMain( QtWidgets.QWidget ):
    def setupUi(self, Main):
        Main.setObjectName( 'Main' )
        Main.resize( 640, 480 )

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()

        self.tela_main = Tela_main()
        self.tela_main.setupUi( (self.stack0) )

        self.tela_mapa = Tela_mapa()
        self.tela_mapa.setupUi( (self.stack1) )

        self.tela_marcador = Tela_marcador()
        self.tela_marcador.setupUi((self.stack2))

        self.tela_calc_dist = Tela_calc_dist()
        self.tela_calc_dist.setupUi((self.stack3))

        self.tela_dados_meteoro = Tela_dados_meteoro()
        self.tela_dados_meteoro.setupUi((self.stack4))

        self.tela_conversor = Tela_conversor()
        self.tela_conversor.setupUi((self.stack5))

        self.QtStack.addWidget( self.stack0 )
        self.QtStack.addWidget( self.stack1 )
        self.QtStack.addWidget( self.stack2 )
        self.QtStack.addWidget( self.stack3 )
        self.QtStack.addWidget( self.stack4 )
        self.QtStack.addWidget( self.stack5 )

class Main( QMainWindow, UiMain ):
    
    def __init__(self, parent=None):
        super( Main, self ).__init__( parent )
        self.setupUi( self )
        self.cont = 0

        self.marc = [] # lista com os marcadores

        self.tela_main.pushButton_mapa.clicked.connect( self.voltar_mapa )
        self.tela_main.pushButton_calc_dist.clicked.connect(self.MostrarTela_calc_dist)
        self.tela_main.pushButton_dados_met.clicked.connect(self.MostraTela_dados_meteoro)
        self.tela_main.pushButton_conversor.clicked.connect(self.MostrarTela_conversor)

        self.tela_mapa.pushButton_ver_map.clicked.connect(self.visualizar_mapa)
        self.tela_mapa.pushButton_add_marc.clicked.connect(self.Tela_marcador)
        self.tela_mapa.pushButton_voltar.clicked.connect(self.TelaMain)
        
        self.tela_marcador.pushButton_addTitu.clicked.connect(self.adicionar_marcador)
        self.tela_marcador.pushButton_voltar.clicked.connect(self.voltar_mapa)
        
        self.tela_calc_dist.pushButton_calc.clicked.connect(self.calcular_distancia)
        self.tela_calc_dist.pushButton_voltar.clicked.connect(self.TelaMain)

        self.tela_dados_meteoro.pushButton_busc_dados.clicked.connect(self.buscar_dados_meteoro)
        self.tela_dados_meteoro.pushButton_voltar.clicked.connect(self.Voltar_dados_meteoro)

        self.tela_conversor.pushButton_conv_End.clicked.connect(self.converter_endereco)
        self.tela_conversor.pushButton_conv_Coord.clicked.connect(self.converter_coordenadas)
        self.tela_conversor.pushButton_voltar.clicked.connect(self.Voltar_converter)

    def salva_html(self,mapa):
        """
        Salva o mapa em um arquivo HTML
        :param mapa: 
            objeto da biblioteca folium
        :return: 
            None
        """
        with open('mapa.html', 'w') as f:
            f.write(mapa.show().get_root().render())
            f.write('''
                <script>
                setTimeout(function() {
                    window.close();
                }, 25000);
                </script>
                ''')
    def visualizar_mapa(self):
        """
        Abre automaticamente o arquivo HTML em uma janela do navegador mostrando o mapa
        :param: 
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex( 1 )
        lat = self.tela_mapa.lineEdit_lat.text()
        lon = self.tela_mapa.lineEdit_lon.text()
        zoo = self.tela_mapa.lineEdit_zoom.text()
        if lat!='' and lon!='' and zoo!='':
            mapa = Map(center=[lat, lon],zoom=zoo)
            global cont
            if self.cont==0:
                self.salva_html(mapa)
            else:
                cont=0
            
            webbrowser.open('mapa.html')
            self.tela_mapa.lineEdit_lat.setText( '' )
            self.tela_mapa.lineEdit_lon.setText( '' )
            self.tela_mapa.lineEdit_zoom.setText( '' )
        else:
            QMessageBox.information( None, 'Mensagem', 'Digite as informações!')
            self.tela_mapa.lineEdit_lat.setText( '' )
            self.tela_mapa.lineEdit_lon.setText( '' )
            self.tela_mapa.lineEdit_zoom.setText( '' )

    def adicionar_marcador(self):
        """
        Adiciona um marcador no mapa
        :param:
            None
        :return:
            None    
        """
        self.QtStack.setCurrentIndex( 2 )
        lat = self.tela_marcador.lineEdit_lat.text()
        lon = self.tela_marcador.lineEdit_lon.text()
        titulo = self.tela_marcador.lineEdit_titu.text()
        if lat!='' and lon!='' and titulo!='':
            mapa = Map(center=[lat, lon],zoom=15)
            marker = mapa.create_marcador(lat,lon,titulo)
            global marc
            self.marc.append(marker)

            for i in self.marc:
                mapa.add_layer(i)
            self.salva_html(mapa)
            global cont
            self.cont=1
            QMessageBox.information( None, 'Mensagem', 'Marcador Adicionado')
            self.tela_marcador.lineEdit_lat.setText( '' )
            self.tela_marcador.lineEdit_lon.setText( '' )
            self.tela_marcador.lineEdit_titu.setText( '' )
            
            self.tela_mapa.lineEdit_lat.setText(lat)
            self.tela_mapa.lineEdit_lon.setText(lon)
            self.tela_mapa.lineEdit_zoom.setText('15')
        else:
            QMessageBox.information( None, 'Mensagem', 'Digite as informações!')

    def retorFloat(self,valor1,valor2,valor3,valor4):
        """
        Modifica o type dos valores de str para float
        :param valor1:
            valor1 str
        :param valor2:
            valor2 str
        :param valor3:
            valor3 str
        :param valor4:
            valor4 str
        :return:
            Os valores em float(valor1,valor2,valor3,valor4)
        """
        valor1= float(valor1)
        valor2= float(valor2)
        valor3= float(valor3)
        valor4= float(valor4)
        return valor1,valor2,valor3,valor4

    def calcular_distancia(self):
        """
        Calcula a distancia de duas coordenadas
        :param:
            None
        :return:
            None
        """
        lat_A = self.tela_calc_dist.lineEdit_lat_A.text()
        lon_A = self.tela_calc_dist.lineEdit_lon_A.text()
        
        lat_B = self.tela_calc_dist.lineEdit_lat_B.text()
        lon_B = self.tela_calc_dist.lineEdit_lon_B.text()
        if lat_A!='' and lon_A!='' and lat_B!='' and lon_B!='':
            lat_A,lon_A,lat_B,lon_B = self.retorFloat(lat_A,lon_A,lat_B,lon_B)

            self.p1 = Coordinate(lat_A, lon_A)
            self.p2 = Coordinate(lat_B, lon_B)
            
            dist = self.p1.distance(self.p2)
            dist = int(dist)
            self.tela_calc_dist.lineEdit_result.setText(str(dist)+' km')
        else:
            QMessageBox.information( None, 'Mensagem', 'Preencha as informações!')            
            self.tela_calc_dist.lineEdit_lat_A.setText('')
            self.tela_calc_dist.lineEdit_lon_A.setText('')
            self.tela_calc_dist.lineEdit_lat_B.setText('')
            self.tela_calc_dist.lineEdit_lon_B.setText('')
    
    def buscar_dados_meteoro(self):
        """
        Busca dados meteorologicos como temperatura, umidade e pressão de uma api usando o serviço OpenStreetMap Nominatim
        :param:
            None
        :return:
            None
        """
        lat = self.tela_dados_meteoro.lineEdit_lat.text()
        lon = self.tela_dados_meteoro.lineEdit_lon.text()
        cidade = self.tela_dados_meteoro.lineEdit_cidade.text()
        endereco = self.tela_dados_meteoro.lineEdit_endere.text()
        if lat!='' and lon!='' or cidade!='' and endereco!='':
            if lat=='' and lon=='':
                geocoder = OSMGeocoder()
                coordinates = geocoder.geocode(cidade+','+endereco)
                lat = (str(coordinates[0]))
                lon=(str(coordinates[1]))
        
            self.busc = Location(cidade, endereco, float(lat),float(lon))
            # obtém as informações meteorológicas para a cidade de Nova York
            self.busc.set_weather('1fad30734db859e67fe4b73213276fbf',lat ,lon)
            self.tela_dados_meteoro.lineEdit_tempe.setText(str(self.busc.temperature)+' °C')
            self.tela_dados_meteoro.lineEdit_umidad.setText(str(self.busc.humidity)+'%')
            self.tela_dados_meteoro.lineEdit_pressao.setText(str(self.busc.pressure)+' hPa')
            self.tela_dados_meteoro.lineEdit_lat.setText('')
            self.tela_dados_meteoro.lineEdit_lon.setText('')
            self.tela_dados_meteoro.lineEdit_cidade.setText('')
            self.tela_dados_meteoro.lineEdit_endere.setText('')
        else:
            QMessageBox.information( None, 'Mensagem', 'Preencha as informações!')            
            

    def Voltar_dados_meteoro(self):
        """
        Sai da tela de buscar dados meteorologicos e retorna para tela principal 
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex( 0 )
        self.tela_dados_meteoro.lineEdit_lat.setText('')
        self.tela_dados_meteoro.lineEdit_lon.setText('')
        self.tela_dados_meteoro.lineEdit_cidade.setText('')
        self.tela_dados_meteoro.lineEdit_endere.setText('')
        self.tela_dados_meteoro.lineEdit_tempe.setText('')
        self.tela_dados_meteoro.lineEdit_umidad.setText('')
        self.tela_dados_meteoro.lineEdit_pressao.setText('')

    def Voltar_converter(self):
        """
        Sai da tela de converter coordenadas e retorna para tela principal 
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex( 0 )
        self.tela_conversor.lineEdit_enderc_Coord.setText('')
        self.tela_conversor.lineEdit_endere_E.setText('')
        self.tela_conversor.lineEdit_lat_C.setText('')
        self.tela_conversor.lineEdit_lat_E.setText('')
        self.tela_conversor.lineEdit_lon_C.setText('')
        self.tela_conversor.lineEdit_lon_E.setText('')
    
    def converter_endereco(self):
        """
        Converte um determinado endereço em coordenadas latitude e longitude usando uma api com serviços do OpenStreetMap Nominatim
        :param:
            None
        :return:
            None
        """
        geocoder = OSMGeocoder()
        endereco = self.tela_conversor.lineEdit_endere_E.text()
        if endereco!='':
            coordinates = geocoder.geocode(endereco)
            self.tela_conversor.lineEdit_lat_E.setText(str(coordinates[0]))
            self.tela_conversor.lineEdit_lon_E.setText(str(coordinates[1]))

            self.tela_conversor.lineEdit_endere_E.setText('')
        else:
            QMessageBox.information( None, 'Mensagem', 'Preencha o enderço!')            
            
    def converter_coordenadas(self):
        """
        Converte coordenadas latitude e longitude em um determinado endereço, com uma api que usa o serviço OpenStreetMap Nominatim
        :param:
            None
        :return:
            None
        """
        geocoder = OSMGeocoder()
        lat = self.tela_conversor.lineEdit_lat_C.text()
        lon = self.tela_conversor.lineEdit_lon_C.text()
        if lat!='' and lon!='':
            address = geocoder.reverse_geocode(lat, lon)
            
            address=str(address)
            address = address.replace('(','')
            address = address.replace(')','')
            address = address.replace( "'", '' )
            
            self.tela_conversor.lineEdit_enderc_Coord.setText(str(address))

            self.tela_conversor.lineEdit_lat_C.setText('')
            self.tela_conversor.lineEdit_lon_C.setText('')
        else:
            QMessageBox.information( None, 'Mensagem', 'Preencha as informações!')            
            
    def TelaMain(self):
        """
        Volta para tela principal do sistema
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex( 0 )

    def voltar_mapa(self):
        """
        Abre uma tela de visualizar o mapa
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex( 1 )

    def Tela_marcador(self):
        """
        Abre uma tela para adicionar marcadores
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex(2)

    def MostrarTela_calc_dist(self):
        """
        Abre uma tela para calcular a distancia entre coordenadas
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex(3)

    def MostraTela_dados_meteoro(self):
        """
        Abre uma tela para buscar dados meteorologicos
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex(4)

    def MostrarTela_conversor(self):
        """
        Abre uma tela para converter endereços em coordenadas e vice-versa
        :param:
            None
        :return:
            None
        """
        self.QtStack.setCurrentIndex(5)

if __name__ == '__main__':
    app = QApplication( sys.argv )
    show_main = Main()
    sys.exit( app.exec_() )
