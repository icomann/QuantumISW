from matplotlib import pyplot as plt, figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
class Grafico():
	def __init__(self,grid):
		self.grid = grid
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		grid.addWidget(self.canvas, 10,10)#No funcionan los tamaños



	def show(self):
		print("(zaz)")
		#self.x = close(?)
		#self.y = fechas(?)
		graf = plt.subplot(111)
		graf.plot([1,2],[1,3])
		graf.set_title('Plotcito')
		plt.xlabel("tiempo [t(?)]")
		plt.ylabel("ganancia[$(?)]")
		plt.tight_layout()
		self.canvas.draw()

