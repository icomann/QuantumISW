# -*- coding: utf-8 -*-
import sys
import os
import shutil

from PyQt4 import QtGui, QtCore, uic
import numpy
import pandas
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from math import *
import rwrapper
import rpy2.robjects as robjects

qtCreatorFile = "SIMPLE_GUI.ui" # Enter file here. #Interfaz hecha con QTDesigner
R = rwrapper.RWrapper("europe.R", "vol.R", "murica.R")

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

        comboBox = self.business_type_combo
        comboBox.addItem(QtGui.QIcon("rsc/call.png"),"Compra")
        comboBox.addItem(QtGui.QIcon("rsc/put.png"),"Venta")

        comboBoxType = self.Option_type
        comboBoxType.addItem(QtGui.QIcon("rsc/american_option.png"),"Americana")
        comboBoxType.addItem(QtGui.QIcon("rsc/european_option.png"),"Europea")
        
        #Lanzador para el boton Calcular, llama a result_function
        self.calculate_option.clicked.connect(self.result_function)

    def reload_sources(self):

    def result_function(self):
        option = self.business_type_combo.currentText()
        zone = self.Option_type.currentText()

        stock_symbol = self.stock_name.toPlainText() #get symbol

        temp_var = self.start_date.date() #get start date
        start_date = (temp_var.toPyDate()).strftime("%Y-%m-%d") #formato start date
        temp_var2 = self.finish_date.date() #get finish date
        finish_date = (temp_var2.toPyDate()).strftime("%Y-%m-%d") #formato finish date

        Time_mature = float(self.Time_mature_name.toPlainText()) #tiempo de madurez

        k = float(self.k_value.toPlainText()) #get k

        r = float(self.r_value.toPlainText()) #get r

        try:
            filename = self.import_data_from_server(stock_symbol,start_date,finish_date) #llama a la importacion desde el servidor
        except:
            self.result.setText("ERROR CARGA DATOS")
            return

        close_values = self.read_csv(filename) #leo el csv y guardo los datos Close en una lista
        #close_values =[20.0, 20.1, 19.9, 20.0, 20.5, 20.25, 20.9, 20.9, 20.9,  20.75, 20.75, 21.0, 21.1, 20.9, 20.9, 21.25, 21.4, 21.4, 21.25, 21.75, 22.0]

        volatilidad = self.fvolatilidad(close_values) #calculo volatilidad
        #volatilidad = 0.2
        
        if zone=="Europea":
            if option=="Compra":
                option_func = "europeanCall"
            elif option=="Venta":
                option_func = "europeanPut"
        elif zone=="Americana":
            if option=="Compra":
                option_func = "americanCall"
            elif option=="Venta":
                option_func = "americanPut"

        #Linea bestia que llama la funcion y la chanta en result
        self.result.setText('{0:0.6f}'.format(R.call(option_func)(volatilidad, r, k, Time_mature, R.vectorize(close_values))[0]))


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

    def fvolatilidad(self, close_values):
        ret = R.call("volatilidad")(R.vectorize(close_values))

        return float(ret[0])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
