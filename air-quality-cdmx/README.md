![ironhacklogo](https://github.com/luisferlc/datamex1019/edit/final-project/air-quality-cdmx/ironhack.png)

# Predicción de IMECA para PM10 y PM2.5

**Luis Fernando López Corrales**

## Alcance del análisis
Crear un modelo de predicción para las mediciones de PM10 y PM2.5 máximas diarias, en la zona centro de la Ciudad de México. Posteriormente, se calculará el IMECA máximo diario.
### Alcaldía: Cuahtemoc
Esto se traduce a las estaciones de medicion:
- Cuahtémoc: HGM (Hospital General de México). Zona Centro de CDMX.
#### Contaminantes
* PM10
* PM2.5

## Resúmen
El análisis se puede dividir en dos etapas:

1. Predicción de partículas por cada hora del día (análisis hecho solo para PM10):
    - Rellenando NaN's con el promedio de cada año
    - Eliminando los NaN's.
Estos dos enfoques daban practicamente los mismos resultados. Después pase a la segunda etapa, donde me di cuenta que tenía mejores resultados. Es aquí donde analize también a PM2.5

2. Predicción de partículas por día individual (PM10 y PM2.5):
    - Eliminando NaN's y outliers.
 
## Modo de cálculo
1. Las mediciones de PM10 y PM2.5 derivan de las concentraciones obtenidas como promedio móvil de 24 horas (NOM-025-SSA1-2014).
2. Con base a las mediciones por hora, se obtendra el valor máximo de cada día y se hará la predicción bajo estos valores.
3. Se comparará con el IMECA máximo de cada día.

## Resultados

1. Predicción de partículas por cada hora del día:
- MAPE alrededor de 40%
- 60-80% de similitud con IMECA real.
