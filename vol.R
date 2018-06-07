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