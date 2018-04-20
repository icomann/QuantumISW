# -*- coding: utf-8 -*-
import sys
import os
import shutil

from PyQt4 import QtGui, QtCore, uic
import rpy2.robjects as robjects
import numpy
import pandas
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from math import *
import rpy2.robjects.numpy2ri

rpy2.robjects.numpy2ri.activate() #Convierte objetos numpy en objetos R

qtCreatorFile = "SIMPLE_GUI.ui" # Enter file here. #Interfaz hecha con QTDesigner

r = robjects.r # Con r llamamos a una funcion de R, por ejemplo: r.mean()



# jugar para obtener valores aleatorios
#robjects.r('set.seed(42)')
# r = robjects.r
# z = r.rnorm(10)
# print (z)
# zz = numpy.array(z)
# print (zz.mean())



# Hay una funcion aqui interesante para la carga de archivos
# class QDataViewer(QtGui.QWidget):
#     def __init__(self):
#         QtGui.QWidget.__init__(self)
#         # Layout Init.
#         self.setGeometry(650, 300, 600, 600)
#         self.setWindowTitle('Data Viewer')
#         self.quitButton = QtGui.QPushButton('QUIT', self)
#         self.uploadButton = QtGui.QPushButton('UPLOAD', self)
#         hBoxLayout = QtGui.QHBoxLayout()
#         hBoxLayout.addWidget(self.quitButton)
#         hBoxLayout.addWidget(self.uploadButton)
#         self.setLayout(hBoxLayout)
#         # Signal Init.
#         self.connect(self.quitButton,   QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
#         self.connect(self.uploadButton, QtCore.SIGNAL('clicked()'), self.open)

#     def open (self):
#         filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
#         #filename = os.path.basename(filepath)
#         #print (filename)
#         print(read_csv(filepath))


# def window():
# 	app = QtGui.QApplication(sys.argv)
# 	mw = QDataViewer()
# 	mw.show()
# 	sys.exit(app.exec_())

# if __name__ == '__main__':
# 	window()



Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        #Todo lo necesario para la inicializacion
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #Lanzador para el boton Calcular, llama a result_function
        self.calculate_option.clicked.connect(self.result_function)

    def result_function(self):
        stock_symbol = self.stock_name.toPlainText() #get symbol

        temp_var = self.start_date.date() #get start date
        start_date = (temp_var.toPyDate()).strftime("%Y-%m-%d") #formato start date
        temp_var2 = self.finish_date.date() #get finish date
        finish_date = (temp_var2.toPyDate()).strftime("%Y-%m-%d") #formato finish date

        Time_mature = float(self.Time_mature_name.toPlainText()) #tiempo de madurez

        k = float(self.k_value.toPlainText()) #get k

        r = float(self.r_value.toPlainText()) #get r

        #combo = self.business_type_combo.QComboBox() #Compra/Venta
        #combo.addItem("Compra")
        #combo.addItem("Venta")

        filename = self.import_data_from_server(stock_symbol,start_date,finish_date) #llama a la importacion desde el servidor

        close_values = self.read_csv(filename) #leo el csv y guardo los datos Close en una lista
        #close_values =[20.0, 20.1, 19.9, 20.0, 20.5, 20.25, 20.9, 20.9, 20.9,  20.75, 20.75, 21.0, 21.1, 20.9, 20.9, 21.25, 21.4, 21.4, 21.25, 21.75, 22.0]

        volatilidad = self.fvolatilidad(close_values) #calculo volatilidad
        #volatilidad = 0.2

        call = self.Call(volatilidad, r, k, Time_mature, close_values) #Llamada a compra
        #put = self.Put(volatilidad, r, k, Time_mature)   #Llamada a venta
        ans_string = '{0:0.6f}'.format(call)
        self.result.setText(ans_string) #muestra resultado

    def import_data_from_server(self,stock_symbol,start_date,finish_date):
        #Inicializa llamada al servidor
        yf.pdr_override()
        data = pdr.get_data_yahoo(stock_symbol, start=start_date, end=finish_date,as_panel = False) #guarda data en dataframe
        #Guardo los datos en un csv
        filename = 'historical_data/' +stock_symbol+'_'+start_date+'_'+finish_date+'.txt'
        archivo = open(filename, 'w')
        archivo.write(data.to_csv())
        archivo.close()
        return filename #retorno el path del archivo

    def read_csv(self,file): #funcion que retorna una lista con los datos Close del CSV
        colnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        data = pandas.read_csv(file, names=colnames)
        close = data.Close.tolist()
        close = close[1:]
        return close


    def Call(self, volatilidad, r, k, Time_mature, close_values):
        robjects.r("""
            f <- function(volatilidad, r, k, Time_mature, close_values, verbose=FALSE){
                if(verbose) {
                    cat("I am calling Call().\n")
                }
                s0 <- close_values[-1] #precio de la acción hoy

                lensimula <- 1000 #numero simulaciones

                generator <- rnorm(lensimula, mean = 0, sd = 1) #Genera lista con numeros aleatorios usando distribucion normal

                esp <- c()
                

                #Generación de curvas S_t
                for (i in 1:lensimula){
                  st <- s0*exp((r - (1/2)*volatilidad^2)*(Time_mature) + volatilidad*generator[i]*sqrt(Time_mature))
                  esp <- append(esp,max(0.0,st-k))
                }

                promesp <- mean(esp)
                Ftx <- exp(-1*r*(Time_mature))*promesp #resultado final
                return(Ftx)
            }
        """)

        r_f = robjects.r['f']

        r_close_values = robjects.FloatVector(close_values)
        put_call = r_f(volatilidad, r, k, Time_mature, r_close_values)

        return float(put_call[0])


    def Put(self, volatilidad, r, k, Time_mature, close_values):
        robjects.r("""
            f <- function(volatilidad, r, k, Time_mature, close_values, verbose=FALSE){
                if(verbose) {
                    cat("I am calling Put().\n")
                }
                s0 <- close_values[-1] #precio de la acción hoy

                lensimula <- 1000 #numero simulaciones

                generator <- rnorm(lensimula, mean = 0, sd = 1) #Genera lista con numeros aleatorios usando distribucion normal

                esp <- c()

                #Generación de curvas S_t
                for (i in 1:lensimula){
                  st <- s0*exp((r - (1/2)*volatilidad^2)*(Time_mature) + volatilidad*generator[i]*sqrt(Time_mature))
                  esp <- append(esp,max(0.0,k-st))
                }

                promesp <- mean(esp)
                Ftx <- exp(-1*r*(Time_mature))*promesp #resultado final
                return(Ftx)
            }
        """)

        r_f = robjects.r['f']

        r_close_values = robjects.FloatVector(close_values)
        put_sim = r_f(volatilidad, r, k, Time_mature, r_close_values)

        return float(put_sim[0])


    def fvolatilidad(self, close_values):
        robjects.r("""
            f <- function(close_values, verbose=FALSE){
                if(verbose) {
                    cat("I am calling simulation().\n")
                }
                mu_values <- c()
                for (i in 2:length(close_values)){
                  mu_values <- append(mu_values, (log(close_values[i] / close_values[i-1])))
                }

                desviacion <- sd(mu_values)
                tau <- 252  #Factor para Volatilidad anual
                volatilidad <- desviacion * sqrt(tau)

                return(volatilidad)
            }
        """)

        r_f = robjects.r['f']

        r_close_values = robjects.FloatVector(close_values)
        ret = r_f(r_close_values)

        return float(ret[0])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
