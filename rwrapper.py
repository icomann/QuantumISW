import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri

class RWrapper():
	def __init__(self, *args):
		self.r = robjects.r # Con r llamamos a una funcion de R, por ejemplo: r.mean()
		rpy2.robjects.numpy2ri.activate() #Convierte objetos numpy en objetos R
		for file in args:
			self.load_source(file)# for file in args

	#Carga funciones de archivo R
	def load_source(self, filename):
		file = open(filename)
		source = ""
		for line in file:
			source += line
		robjects.r(source)
		file.close()

	def call(self, function_name):
		return self.r[function_name]
		
	def vectorize(self, data):
		return robjects.FloatVector(data)