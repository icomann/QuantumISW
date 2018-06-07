import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri

class RWrapper():
	def __init__():
		self.r = robjects.r # Con r llamamos a una funcion de R, por ejemplo: r.mean()
		rpy2.robjects.numpy2ri.activate() #Convierte objetos numpy en objetos R

	#Carga funciones de archivo R
	def load_source(filename):
		robjects.r(filename)

	def call(function_name):
		if function_name in self.r:
			return self.r.[function_name]
		print "ANSDLAKSND"