data <- c(20.0, 20.1, 19.9, 20.0, 20.5, 20.25, 20.9, 20.9, 20.9,  20.75, 20.75, 21.0, 21.1, 20.9, 20.9, 21.25, 21.4, 21.4, 21.25, 21.75, 22.0)

data2 <- c() 
for (i in 2:length(data)){
  data2 <- append(data2, (log(data[i] / data[i-1])))
}

promedio = mean(data2)
desviacion = sd(data2)

tau <- 252  #Volatilidad anual

Time_mature <- 2

t = 1

volatilidad <- desviacion * sqrt(tau)

epsilon = set.seed(112358)

s0 <- 22
r <- 0.002

lensimula <- 500

esp <- c()

for (i in 1:lensimula){
  st <- s0*exp((r- (1/2)*volatilidad^2)*(Time_mature-t) + volatilidad*epsilon*sqrt(Time_mature-t))
  esp <- append(esp, st)
  s0 <- st
}

promesp <- mean(esp)

Ftx <-exp(-1*r*(Time_mature -t))*promesp
