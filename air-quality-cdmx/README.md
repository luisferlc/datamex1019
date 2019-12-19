![ironhacklogo](https://github.com/luisferlc/datamex1019/final-project/air-quality-cdmx/imágenes/ironhack.png)

<img src="https://github.com/luisferlc/datamex1019/final-project/air-quality-cdmx/imágenes/ironhack.png">

# Predicción de IMECA para PM10 y PM2.5

**Luis Fernando López Corrales**

**Facebook Prophet**

## Alcance del análisis
Crear un modelo de predicción para las mediciones de PM10 y PM2.5 máximas diarias, en la zona centro de la Ciudad de México. Posteriormente, se calculará el IMECA máximo diario y se hará la comparación de los resultados con los IMECA's del 2019.
### Alcaldía: Cuahtemoc
Esto se traduce a las estaciones de medicion:
- Cuahtémoc: HGM (Hospital General de México). Zona Centro de CDMX.
#### Contaminantes
* PM10
* PM2.5

## Resúmen
El análisis se puede dividir en dos etapas:

1. Predicción de partículas por cada hora del día (análisis hecho solo para PM10):

Dos tipos de limpieza:
- Rellenando NaN's con el promedio de cada año
- Eliminando los NaN's.

Estos dos enfoques daban practicamente los mismos resultados. Después pase a la segunda etapa, donde me di cuenta que tenía mejores resultados. Es aquí donde analize también a PM2.5

2. Predicción de partículas por máxima concentración del día individual (PM10 y PM2.5):
- Eliminando NaN's y outliers.
 
 
## Modo de cálculo
1. Las mediciones de PM10 y PM2.5 derivan de las concentraciones obtenidas como promedio móvil de 24 horas (NOM-025-SSA1-2014).
2. Con base a las mediciones por hora, se obtendra el valor máximo de cada día y se hará la predicción bajo estos valores.
3. Se comparará con el IMECA máximo de cada día del 2019.

## Resultados

1. Predicción de partículas por cada hora del día:

Los dos tipos de limpieza de datos o enfoques tuvieron los mismos resultados:
- MAPE alrededor de 40%
- 60-80% de similitud con IMECA real.


