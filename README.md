# Proyecto Valoración de Opciones sobre Acciones (03-07-18)

## Equipo: QuantumWare

1. Calculadora de opciones: 
[Click me!](http://www.cboe.com/framed/IVolframed.aspx?content=https%3a%2f%2fcboe.ivolatility.com%2fcalc%2findex.j%3fcontract%3d95CB7CDF-A27A-4867-8894-ED1E2D1E0B90&sectionName=SEC_TRADING_TOOLS&title=CBOE%20-%20IVolatility%20Services)

2. Gráfico de simulaciones está impreciso (Puede que no temga nada que ver con la valorización pero se ve bonito :D)

3. El sistema logra descargar datos usando fix-yahoo-finance, pero suele caerse, se hace necesaria la importación de archivos.
4. El consultor ingresa T(tiempo de madurez), los datos históricos son de acuerdo a ese T. Por ejemplo, el consultor coloca T= 6 meses, habra que descargar 6 meses de datos históricos para calcular volatilidad.
5. Ejecución, por mientras:

```
python3 main.py
```
