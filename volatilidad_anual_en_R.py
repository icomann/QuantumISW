import rpy2.robjects as robjects

robjects.r("""
        f <- function(close_values, verbose=FALSE){
            if(verbose) {
                cat("I am calling f().\n")
            }
            mu_values <- c()
            for (i in 2:length(close_values)){
              mu_values <- append(mu_values, (log(close_values[i] / close_values[i-1])))
            }

            promedio <- mean(mu_values)
            desviacion <- sd(mu_values)

            tau <- 252  #Factor para Volatilidad anual

            volatilidad <- desviacion * sqrt(tau)

            Time_mature <- 0.5

            #set.seed(112358)

            s0 <- 42 #precio de la acción hoy
            r <- 0.1 #tasa interés libre de riesgo

            lensimula <- 1000 #numero simulaciones

            generator <- rnorm(lensimula, mean = 0, sd= 1) #Genera lista con numeros aleatorios usando distribucion normal

            esp <- c()

            #Generación de curvas S_t
            for (i in 1:lensimula){
              st <- s0*exp((r- (1/2)*volatilidad^2)*(Time_mature) + volatilidad*generator[i]*sqrt(Time_mature))
              esp <- append(esp,st)
            }


            promesp <- mean(esp)
            Ftx <- exp(-1*r*(Time_mature))*promesp #resultado final
            return(Ftx)
        }

""")

r_f = robjects.r['f']

#r_f = robjects.r['f']

close_values = [20.0, 20.1, 19.9, 20.0, 20.5, 20.25, 20.9, 20.9, 20.9,  20.75, 20.75, 21.0, 21.1, 20.9, 20.9, 21.25, 21.4, 21.4, 21.25, 21.75, 22.0]

r_close_values = robjects.FloatVector(close_values)
res = r_f(r_close_values)

print(res)








"""
def volatilidad_anual(self, close_values):
    mu_values = robjects.FloatVector([])
    for i in range(1,len(close_values)):
        mu = log(float(close_values[i]) / float(close_values[i-1]))
        mu_values.append(mu)
    desviacion = r.sd(numpy.array(mu_values)) #guarda un vector con el valor
    tau = 252  #Factor para Volatilidad anual
    volatilidad = desviacion[0]* sqrt(tau)
    return volatilidad
"""
