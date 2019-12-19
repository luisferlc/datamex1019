# Predicción de IMECA para PM10 y PM2.5

## Resúmen
Crear un modelo de predicción para las mediciones de PM10 y PM2.5 máximas diarias. Este modelo de predicción se va comparar con los valores máximos diarios de cada partícula.
## Alcance del análisis

### Alcaldía: Cuahtemoc
Esto se traduce a las estaciones de medicion:
- Cuahtémoc: HGM (Hospital General de México). Zona Centro de CDMX.
#### Contaminantes
* PM10
* PM2.5

## Modo de cálculo
1. Las mediciones de PM10 y PM2.5 derivan de las concentraciones obtenidas como promedio móvil de 24 horas (NOM-025-SSA1-2014).
2. Con base a las mediciones por hora, se obtendra el valor máximo de cada día y se hará la predicción bajo estos valores.
3. Se comparará con el IMECA máximo de cada día.
