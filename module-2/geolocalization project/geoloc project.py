# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 09:45:30 2019

@author: luisf
Geolocalization project
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
##Al menos una oficina
at_least_1_office = db.companies.find({'offices':{'$not':{'$size':0}}})
                                    #,{'name':1, 'offices':1, '_id':0})

df = pd.DataFrame(at_least_1_office)
df.head()
df.columns
df.competitions
df.investments[4]
##########    Los tipos de empresa:
df.category_code.unique()
types_count = df.groupby('category_code').agg({'category_code':'count'}).rename(columns={'category_code':'count'})
types_count.sort_values(by='count', ascending=False) #Los giros de empresas más presentes son web, software, games_video, mobile,advertising,ecommerce,consulting,network_hosting
##Mi cliente va ser alguien que este en algunos de esos giros.
##Reducir mi df con solo esos tipos:
df_1 = df.query('category_code in ["web","software","ecommerce","consulting"]')
##Los índices cambiaron, asi que tengo que reindexar:
df_1.head()
df_1 = df_1.reset_index()
#df_1.isnull().sum()
## Reduciendo por número de empleados
df_1.describe()
small_companies = df_1.query('number_of_employees < 250')
micro_companies = df_1.query('number_of_employees < 10')
## Empresas no mayor a 3 años de iniciadas
#pd.set_option('display.max_columns', 4)
#pd.reset_option('all')
small_companies.columns
small_companies.founded_year.max() # 2013
small_companies[(2013 - small_companies.founded_year) <= 4] #199 row, poco...
micro_companies[(2013 - micro_companies.founded_year) <= 4] #141 rows, poco...

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

geo_companies = json_normalize(get_first(small_companies)[0])
geo_companies.oficina_principal = get_first(small_companies)[1]
geo_companies.head()
geo_companies.columns


#df_clean_small=pd.concat([small_companies, geo_companies], axis=1)[['name', 'number_of_employees', 'competitions','lat', 'lng', 'oficina_principal', 'total_offices']]
df_clean_micro=pd.concat([micro_companies, geo_companies], axis=1)[['name', 'category_code','number_of_employees', 'competitions','lat', 'lng', 'oficina_principal', 'total_offices']]
#df_clean_small=df_clean_small.dropna()
df_clean_micro=df_clean_micro.dropna()
df_clean_micro = df_clean_micro.reset_index()
df_clean_micro.columns
df_clean_micro.head()

## Convertir este dataframe a una colección:
db.companies_filtered.insert_many(df_clean_micro.to_dict('records'))
list(db.companies_filtered.find().limit(2))
## Crear indice 2d
db.companies_filtered.create_index([('oficina_principal', '2dsphere')])

## Encontrar los puntos cercanos:
def find_near(geopoint, radio=1000):
    return db.companies_filtered.find({'oficina_principal':{'$near':{'$geometry':geopoint,
                                                                     '$maxDistance':radio}}})

#wetpaint={'type':'Point', 'coordinates':[-122.333253, 47.603122]} #Recuerda que es Longitud, latitud
#radio=5000
#
#n_ofi=find_near(wetpaint, radio).count()
#
#print ('Hay {} oficinas a {} metros'.format(n_ofi, radio))
#print ('La mas cercana es {}'.format(list(find_near(wetpaint, radio).limit(1))[0]['name']))

#Imprimir el nombre de todas las empresas dentro del radio:
#for e in range(find_near(wetpaint, radio).count()):
#    print(find_near(wetpaint, radio)[e]['name'])
#
#type(find_near(wetpaint, radio))
#find_near(wetpaint, radio)[0]['lng']
#find_near(wetpaint, radio)[0]['name']

## Iterar find_near para encontrar los puntos donde hay más empresas cerca:
companies_coordinates=df_clean_micro[['lng','lat']].values.tolist()
#lst = [find_near({'type':'Point','coordinates': e}, radio) for e in companies_coordinates]
#len(lst)
#lst[0].count()
#lst[1].count()    

position_competitors=[]
for e in companies_coordinates:
    dic = {'origin_point':find_near({'type':'Point','coordinates': e}, radio)[0]['name'],
           'n_ofi_close': find_near({'type':'Point','coordinates': e}, radio).count(),
           'lat':find_near({'type':'Point','coordinates': e}, radio)[0]['lat'],
           'lon':find_near({'type':'Point','coordinates': e}, radio)[0]['lng']
            }
    position_competitors.append(dic)
len(position_competitors)

## El punto donde hay más empresas cerca:
max(position_competitors, key=lambda x: x['n_ofi_close'])

############## Mapeo  ##################
#Mi origen sera la empresa AllofMe, que obtuve anteriormente:
origin = {'type':'Point', 'coordinates':[-73.983626, 40.743808]}
#Traer todos los puntos cerca de AllofMe y ponerlos en un DF:
origin_lst = []
for e in range(find_near(origin, radio).count()):
    dic = {'name':find_near(origin, radio)[e]['name'],
           'lat':find_near(origin, radio)[e]['lat'],
           'lng':find_near(origin, radio)[e]['lng']
           }
    origin_lst.append(dic)
    
df_nearest_origin = pd.DataFrame(origin_lst) 
df_nearest_origin.head()

#Crear una lista con las puras coordenadas en orden lat-long para luego mapear:
locations = df_nearest_origin[['lat', 'lng']]
locationlist = locations.values.tolist()

mapa = folium.Map(location=[40.743808, -73.983626], zoom_start=15)
for point in range(0, len(locationlist)):
    folium.Marker(locationlist[point], popup=df_nearest_origin['name'][point]).add_to(mapa)

mapa.save("mymap.html")



