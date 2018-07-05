from matplotlib import pyplot as plt, figure
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
class Grafico():
	def __init__(self, parent=None):
		self.figure = plt.figure()
		FigureCanvas.__init__(self, self.figure)
		self.setParent(parent)


