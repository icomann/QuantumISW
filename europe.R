europeanCall <- function(volatilidad, r, k, Time_mature, close_values, verbose=FALSE){
    if(verbose) {
        cat("I am calling Call().\n")
    }
    s0 <- tail(close_values, n=1) #precio de la acción hoy


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
    s0 <- tail(close_values, n=1) #precio de la acción hoy

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