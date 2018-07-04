from matplotlib import pyplot as plt, figure
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
class Grafico():
	def __init__(self,grid):
		self.grid = grid
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		grid.addWidget(self.canvas, 10,10)



	def show(self,time,close):
		print("(zaz)")
		self.x = np.linspace(0, time, num=len(close))
		self.y = close

		data = np.cumprod([x,y],1)
		graf = plt.subplot(111)
		graf.plot(data)
		graf.set_title('Plotcito')
		plt.xlabel("tiempo [t(?)]")
		plt.ylabel("ganancia[$(?)]")
		plt.tight_layout()
self.canvas.draw()
