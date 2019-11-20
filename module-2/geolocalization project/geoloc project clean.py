# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:30:50 2019

@author: luisf
"""

from pymongo import MongoClient
import pandas as pd
import folium
from pandas.io.json import json_normalize

#mongoimport db_companies companies companies.json
#mongoimport --db db_companies --collection companies --file companies.json
#mongoimport --db db_companies --collection companies companies.json

client = MongoClient("mongodb://localhost:27017/")

db = client.db_companies #llamas a la BD

companies = db.companies #Llamas a la colección

#query = companies.find() #haces un query de TODO
#df = pd.DataFrame(query) #Lo metes a un df

###################################################################################
#########################  Análisis exploratorio  #################################
###################################################################################

##Filtrar registros por al menos una oficina
at_least_1_office = db.companies.find({'offices':{'$not':{'$size':0}}})

df = pd.DataFrame(at_least_1_office)

##########    Los tipos de empresa: solo para saber qué tipos de empresa son las más presentes en los datos:
#df.category_code.unique()
#types_count = df.groupby('category_code').agg({'category_code':'count'}).rename(columns={'category_code':'count'})
#types_count.sort_values(by='count', ascending=False) #Los giros de empresas más presentes son web, software, games_video, mobile,advertising,ecommerce,consulting,network_hosting
##Mi cliente va ser alguien que este en algunos de esos giros.

##Reducir mi df con solo esos tipos:
df_1 = df.query('category_code in ["web","software","ecommerce","consulting"]')

##Los índices cambiaron, asi que tengo que reindexar:
df_1.index=range(len(df_1))

## Seccionando por número de empleados
micro_companies = df_1.query('number_of_employees < 10')

## Empresas no mayor a 4 años de iniciadas
micro_companies.founded_year.max() # Obtengo el año máximo que me sirve de referencia para sacar la vida de las compañias
micro_companies=micro_companies[(2013 - micro_companies.founded_year) <= 4] #141 rows
micro_companies.index=range(len(micro_companies))
######### Definición de mi cliente:
# Startup
# Giro: una empresa de consultoría de software y e-commerce
# Que no este al lado de empresas con más de 4 años?


###################################################################################
#########################  GeoQuerie  #################################
###################################################################################
def get_first(data):
    res=[]
    ofi=[]
    
    data=data['offices']
    
    for e in data:
        principal=None   # solo las tienen geodata
        if e[0]['latitude'] and e[0]['longitude']:
            principal={'type':'Point',
                       'coordinates':[
                           e[0]['longitude'],
                           e[0]['latitude']
                       ]}
            
        ofi.append(principal)
        
        res.append({
            'total_offices':len(e),
            'lat':e[0]['latitude'],
            'lng':e[0]['longitude'],
            'oficina_principal':principal
        })
    
    return res, ofi

#Armando el DF que servira de parámetro para encontrar los puntos más cercanos
geo_companies = json_normalize(get_first(micro_companies)[0])
geo_companies.oficina_principal = get_first(micro_companies)[1]
df_clean_micro=pd.concat([micro_companies, geo_companies], axis=1)[['name', 'category_code','number_of_employees', 'competitions','lat', 'lng', 'oficina_principal', 'total_offices']]
df_clean_micro=df_clean_micro.dropna()
df_clean_micro.index=range(len(df_clean_micro))

## Convertir este dataframe a una colección:
db.companies_filtered.insert_many(df_clean_micro.to_dict('records'))
list(db.companies_filtered.find().limit(2))
## Crear indice 2d
db.companies_filtered.create_index([('oficina_principal', '2dsphere')])

## Función para encontrar la informacíon de los puntos cercanos:
def find_near(geopoint, radio=5000):
    return db.companies_filtered.find({'oficina_principal':{'$near':{'$geometry':geopoint,
                                                                     '$maxDistance':radio}}})

## Iterar find_near para encontrar los puntos donde hay más empresas cerca:
radio=5000
#Paso los valores de lng y lat a una lista para poder usarlos en la iteración:
companies_coordinates=df_clean_micro[['lng','lat']].values.tolist()

position_competitors=[]
for e in companies_coordinates:
    dic = {'origin_point':find_near({'type':'Point','coordinates': e}, radio)[0]['name'],
           'n_ofi_close': find_near({'type':'Point','coordinates': e}, radio).count(),
           'lat':find_near({'type':'Point','coordinates': e}, radio)[0]['lat'],
           'lon':find_near({'type':'Point','coordinates': e}, radio)[0]['lng']
            }
    position_competitors.append(dic)

## El punto donde hay más empresas cerca:
max(position_competitors, key=lambda x: x['n_ofi_close'])

#########################################################################
########################### Mapeo  ######################################
#########################################################################

#Mi origen sera la empresa Spotlex, que obtuve anteriormente:
origin = {'type':'Point', 'coordinates':[-122.419204, 37.775196]}
#Traer todos los puntos cerca de Spotlex y ponerlos en un DF:
origin_lst = []
for e in range(find_near(origin, radio).count()):
    dic = {'name':find_near(origin, radio)[e]['name'],
           'lat':find_near(origin, radio)[e]['lat'],
           'lng':find_near(origin, radio)[e]['lng']
           }
    origin_lst.append(dic)
    
df_nearest_origin = pd.DataFrame(origin_lst) 

#Crear una lista con las puras coordenadas en orden lat-long para luego mapear:
locations = df_nearest_origin[['lat', 'lng']]
locationlist = locations.values.tolist()

#En el mapeo ya se ponen las coordenadas en orden normal(lat,lng), de tu origen
mapa = folium.Map(location=[37.775196, -122.419204], zoom_start=15)
for point in range(0, len(locationlist)):
    folium.Marker(locationlist[point], popup=df_nearest_origin['name'][point]).add_to(mapa)

mapa.save("sanfranciscomap.html")

### Conclusión:

#Mi recomendación sería localizarse en el área de Brannan y 2dn Street, ya que ahí no hay tantas empresas
#como en la parte de arriba, pero tampoco no hay ninguna otra empresa con la que pueda localizarse su negocio.



