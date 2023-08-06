import requests
import folium
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):

    lista = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(562, 463)
        MainWindow.setStyleSheet("background-color: rgb(67, 149, 255) ")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 120, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 150, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 180, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(40, 210, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 240, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(40, 270, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(40, 300, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(40, 330, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(40, 360, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(40, 390, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(100, 120, 391, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(120, 150, 391, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(210, 180, 261, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(170, 210, 261, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(190, 240, 261, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(110, 270, 261, 16))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(130, 300, 261, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(190, 330, 261, 16))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(170, 360, 261, 16))
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(140, 390, 261, 16))
        self.label_22.setObjectName("label_22")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 80, 571, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 0, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 40, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 562, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Laitude:"))
        self.label_4.setText(_translate("MainWindow", "Longitude:"))
        self.label_5.setText(_translate("MainWindow", "Condição meteorológica:"))
        self.label_6.setText(_translate("MainWindow", "Temperatura(ºC):"))
        self.label_7.setText(_translate("MainWindow", "Pressão atmosférica:"))
        self.label_8.setText(_translate("MainWindow", "Umidade:"))
        self.label_9.setText(_translate("MainWindow", "Visibilidade:"))
        self.label_10.setText(_translate("MainWindow", "Velocidade do vento:"))
        self.label_11.setText(_translate("MainWindow", "Direção do vento:"))
        self.label_12.setText(_translate("MainWindow", "Nebulosidade:"))
        self.label_13.setText(_translate("MainWindow", str(self.lista[1])))
        self.label_14.setText(_translate("MainWindow", str(self.lista[2])))
        self.label_15.setText(_translate("MainWindow", str(self.lista[3])))
        self.label_16.setText(_translate("MainWindow", str(self.lista[4])))
        self.label_17.setText(_translate("MainWindow", "{} Pa".format(str(self.lista[5]))))
        self.label_18.setText(_translate("MainWindow", "{} %".format(str(self.lista[6]))))
        self.label_19.setText(_translate("MainWindow", "{} metros".format(str(self.lista[7]))))
        self.label_20.setText(_translate("MainWindow", "{} m/s".format(str(self.lista[8]))))
        self.label_21.setText(_translate("MainWindow", "{} graus".format(str(self.lista[9]))))
        self.label_22.setText(_translate("MainWindow", "{} %".format(str(self.lista[10]))))
        self.label.setText(_translate("MainWindow", "Dados meteorológicos"))
        self.label_2.setText(_translate("MainWindow", self.lista[0]))

    def main():
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

class MD():

    def __init__(self, cidade, tipo):
        self._cidade = cidade
        self._tipo = tipo

    def retorna_dados(self):
        API_KEY = "aed9ff8e44c7dd4601968e82a30b1aec"
        link = f"https://api.openweathermap.org/data/2.5/weather?q={self._cidade}&appid={API_KEY}&lang=pt_br&units=metric"
        requisicao = requests.get(link)

        if(requisicao.status_code == 200):
            dados_requisicao = requisicao.json()
            latitude = dados_requisicao['coord']['lat']
            longitude = dados_requisicao['coord']['lon']
            condicao = dados_requisicao['weather'][0]['description']
            temperatura = dados_requisicao['main']['temp']
            pressao_atm = dados_requisicao['main']['pressure']
            umidade = dados_requisicao['main']['humidity']
            visibilidade = dados_requisicao['visibility']
            vel_vento = dados_requisicao['wind']['speed']
            direcao_vento = dados_requisicao['wind']['deg']
            nebulosidade = dados_requisicao['clouds']['all']

            Ui_MainWindow.lista = [self._cidade, latitude, longitude, condicao, temperatura, pressao_atm, umidade, visibilidade, vel_vento, direcao_vento, nebulosidade]

            if(self._tipo == 'visualizar'):

                mapa = folium.Map(
                width=1350, height=615,
                location=[latitude, longitude],
                zoom_start=12
                )
                folium.Marker(
                    [latitude, longitude]
                ).add_to(mapa)

                mapa.save("mapa.html")
                webbrowser.open('mapa.html')

                Ui_MainWindow.main()
                
            elif(self._tipo == "retornar"):
                lista_dados = [latitude, longitude, condicao, temperatura, pressao_atm, umidade, visibilidade, vel_vento, direcao_vento, nebulosidade]
                return lista_dados
            
            else:
                print("Tipo de retorno inválido!")
                return None

        elif(requisicao.status_code == 404):
            print("Cidade informada não possui registros meteorológicos!")

        else:
            print("Servidor não encontrado!")