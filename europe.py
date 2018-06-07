europeanCall <- function(volatilidad, r, k, Time_mature, close_values, verbose=FALSE){
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

europeanPut <- function(volatilidad, r, k, Time_mature, close_values, verbose=FALSE){
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

volatilidad <- function(close_values, verbose=FALSE){
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