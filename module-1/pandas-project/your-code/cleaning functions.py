# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:00:36 2019

@author: luisf
Pandas Project
"""

import pandas as pd
import numpy as np
import re
import unicodedata

df = pd.read_csv("./Documents/Python Projects/datamex1019/module-1/pandas-project/global-shark-attacks/attacks.csv", engine='python')
df.info(memory_usage=True)

"""
RangeIndex: 25723 entries, 0 to 25722
Data columns (total 24 columns):
Case Number               8702 non-null object
Date                      6302 non-null object
Year                      6300 non-null float64
Type                      6298 non-null object
Country                   6252 non-null object
Area                      5847 non-null object
Location                  5762 non-null object
Activity                  5758 non-null object
Name                      6092 non-null object
Sex                       5737 non-null object
Age                       3471 non-null object
Injury                    6274 non-null object
Fatal (Y/N)               5763 non-null object
Time                      2948 non-null object
Species                   3464 non-null object
Investigator or Source    6285 non-null object
pdf                       6302 non-null object
href formula              6301 non-null object
href                      6302 non-null object
Case Number.1             6302 non-null object
Case Number.2             6302 non-null object
original order            6309 non-null float64
Unnamed: 22               1 non-null object
Unnamed: 23               2 non-null object
"""

########  Drop 'pdf', 'Case Number.1', 'Case Number.2', 'Unnamed: 22', 'Unnamed: 23', 'href formula'
#df_1 = df.drop(columns=['pdf', 'Case Number.1', 'Case Number.2', 'Unnamed: 22', 'Unnamed: 23', 'href formula'])
#df_1
#
#def drop_columns(data_set):
#    data_out = data_set.drop(columns=['pdf', 'Case Number.1', 'Case Number.2', 'Unnamed: 22', 'Unnamed: 23', 'href formula'])
#    return data_out

#################################################################################
##################### Columna Case Number and Date  #####################
#################################################################################
df_1 = df.copy()

### Strings
df_1['Case Number'].value_counts()

df_1['Case Number'] = df_1['Case Number'].str.replace('.b','').str.replace('.a','').str.replace('.R','').str.replace('.k','')
df_1['Case Number'] = df_1['Case Number'].str.replace('.a.R','').str.replace('R2','').str.replace('R1','').str.replace('R3','').str.replace('R4','')
df_1['Case Number'].value_counts()
df_1['Case Number'] = df_1['Case Number'].str.replace('.c','').str.replace('.j','').str.replace('.i','').str.replace('.R.a','')
#df_1['Case Number']
df_1['Case Number'] = df_1['Case Number'].str.replace('.d','').str.replace('.a & b','').str.replace('.m','')
#set(df_1['Case Number'])
df_1['Case Number'] = df_1['Case Number'].str.replace('.e','').str.replace('.f','').str.replace('.l','')
#set(df_1['Case Number'])
df_1['Case Number'] = df_1['Case Number'].str.replace('.g','').str.replace('.d.R','').str.replace('.c.R','')
#set(df_1['Case Number'])
df_1['Case Number'] = df_1['Case Number'].str.replace('. ','').str.replace('.b.R','').str.replace('.R.b','')
#set(df_1['Case Number'])
df_1['Case Number'] = df_1['Case Number'].str.replace('.h','').str.replace('.R.a & b','').str.replace('.x','')
#set(df_1['Case Number'])

#Discriminar registros que estan en blanco:
df_1 = df_1[0:6302]

#df_1.to_csv('jojoa.csv')
### Asignar NaN a los valores como ND (No date) y demás que no son útiles:
#df_1['Case Number'].isnull().sum()
#df_1['Case Number'][df_1["Case Number"] == '0'] = 'Unknown'
#df_1['Case Number'][df_1["Case Number"] == 'xx'] = 'Unknown'

#Hay un valor con NaN, le asignare un valor temporal para asignar NaN a los valores que empiezan con 'ND'
#ya que es un valor inútil.
df_1['Case Number'].isnull().sum()
df_1['Case Number'] = df_1['Case Number'].fillna('Unknown')
df_1['Case Number'][df_1['Case Number'].str.startswith('ND')]=np.NaN


#df_1['Case Number'].dropna(inplace=True)
#String faltante
#df_1['Case Number'][df_1['Case Number'].str.endswith('.')] = ''
#
#set(df_1['Case Number'])
#
#
#df_1['Case Number'].isnull() #Ahora solo hay 6301 registros con datos
#df_1['Case Number'].shape
#df_1.shape



#Después de que tenemos limpia la columna Case Number, le cambiamos el formato a esta columna como fecha y
#asignamos estos valores a la columna Date. Ya que, Case Number es el registro de las fechas pero en formato string.
#A los valores que sean ND (No Date) o esten vaciós, que les ponga NaT

df_1.Date = df_1['Case Number'].apply(lambda x: pd.to_datetime(x,format='%Y.%m.%d',errors='coerce'))

#df_1.Date.loc[847] Punto al final, lo pone como NaT
#df_1.Date
#df_1.Date > '2000-06-10'

df_1.info(memory_usage=True)
#Ahora Date ya esta en formato datetime64

#################################################################################
##################### Columna Year y Type #####################
#################################################################################
df_2 = df_1.copy()
df_2.Type.value_counts()

#YEAR
df_2.Year[df_2.Year == 0] = np.NaN

#a) Creo que Boat y Boating es lo mismo: Homologar nombres
#b) Creo que Boatomg se refiere a Boating: Homologar nombres 
df_2.Type.isnull().sum()
list(df_2.Type[df_2.Type.isnull()].index) #[85, 382, 4867, 5705] Obtuve los índices de los NA's
#Los cambio momentaneamente para poder correr el str.startswith
df_2.Type.iloc[85] = ''
df_2.Type.iloc[382] = ''
df_2.Type.iloc[4867] = ''
df_2.Type.iloc[5705] = ''

df_2.Type[df_2.Type.str.startswith('Boat')]='Boating' #No pude hacerlo en un principio debido a unos NA's
df_2.Type[df_2.Type.str.startswith('Questiona')]='Invalid' 

#Ahora si puedo hacer el startswith, sin embago, quedan 4 valores sin nada como título. Los pongo como NaN's
df_2.Type.value_counts()

df_2.Type.iloc[85] = np.NAN
df_2.Type.iloc[382] = np.NAN
df_2.Type.iloc[4867] = np.NAN
df_2.Type.iloc[5705] = np.NAN
#################################################################################
################################ Columna Country #################################
#################################################################################
df_3 = df_2.copy()
df_3.isnull().sum()
df_3.Country.isnull().sum()
df_3.Country.value_counts()

#Poner en mayúsculas a todos los valores:
df_3.Country = df_3.Country.apply(lambda x: str.upper(str(x)))
df_3.Country.iloc[299]

set(df_3.Country)

#Si hay dos lugares en un solo string, dejare al primero como el válido.
#Si hay dos registros como Andama y Andaman Islands, los unire como Andaman Islands.

df_3.Country[df_3.Country.str.startswith(' ')] = ''
df_3.Country[df_3.Country.str.startswith('ANDAMA')]='ANDAMAN ISLANDS'
df_3.Country = df_3.Country.str.replace('?','')
df_3.Country[df_3.Country.str.startswith('BETWEEN POR')]='PORTUGAL'
df_3.Country[df_3.Country.str.endswith('SRI LANKA)')]='CEYLON'
df_3.Country[df_3.Country.str.endswith(' ')]=''
df_3.Country[df_3.Country.str.endswith('/ ISRAEL')]='EGYPT'
df_3.Country[df_3.Country.str.endswith('/ CAMEROON')]='EQUATORIAL GUINEA'
df_3.Country[df_3.Country.str.endswith('/ IRAQ')]='IRAN'
df_3.Country[df_3.Country.str.endswith('/ CROATIA')]='ITALY'
df_3.Country = df_3.Country.str.replace('MALDIVES','MALDIVE ISLANDS')
df_3.Country = df_3.Country.str.replace('-',' ')
df_3.Country = df_3.Country.str.replace('BRITISH NEW GUINEA','NEW GUINEA')
df_3.loc[df_3.Country == 'OCEAN'] #Index 5748
df_3.Country[5748] = 'UNKOWN' #OCEAN es demasiado ambiguo
df_3.Country[df_3.Country.str.startswith('PAPUA')]='NEW GUINEA'
df_3.Country[df_3.Country.str.endswith('/ INDIAN OCEAN')]='RED SEA'
df_3.Country[df_3.Country.str.endswith('REUNION')]='REUNION ISLAND'
df_3.Country[df_3.Country.str.endswith('/ VANUATU')]='SOLOMON ISLANDS'
df_3.Country[df_3.Country.str.endswith('MAARTIN')]='ST. MARTIN'
df_3.Country[df_3.Country.str.endswith('(UAE)')]='UNITED ARAB EMIRATES'
df_3.Country = df_3.Country.apply(lambda x: str.title(x)) #Capitalizar
df_3.Country[df_3.Country == 'Usa'] = 'USA'
df_3.Country[df_3.Country == 'Nan'] = np.NaN

#df_5.Country.value_counts()

#################################################################################
##################################  Area  #######################################
#################################################################################
df_4 = df_3.copy()
df_4.Area.value_counts()
df_4.Area.isnull().sum()

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

area_string = df_4.Area.to_string() #Convertir la columna en string
area_string = strip_accents(area_string) #Quitar los acentos y poner 'Nan' en valores vacios
area_string = re.sub('\d', '', area_string) #Quitar el número del principio
area_string = [x.split(';') for x in area_string.split('\n')] #Convertir el string a lista
df_4.Area = pd.DataFrame(area_string) #Almacenar la lista en el DataFrame
df_4.Area = df_4.Area.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
df_4.Area = df_4.Area.apply(lambda x: str.title(x)) #Capitalizar

#Valores con acentos, comillas, paréntesis, diagonales, coordenadas geográficas, valores desconocidos...
df_4.Area.iloc[[310,447,607,860,913,1167,1634,1687,2126,2160,2356,2362,2396,2515,2530,2545,2546,2591,
                3489,3850,3918,3930,3984,4085,4187,4312,4541,4614,4702,4727,5045,5386,5403,5462,5736,5907,
                5912,5915,5916,5947,6083]]

df_4.Area = df_4.Area.str.replace('"','')
df_4.Area = df_4.Area.str.replace('(','').str.replace(')','')
df_4.Area = df_4.Area.str.replace('?','')
df_4.Area = df_4.Area.str.replace(' /',',')
df_4.Area = df_4.Area.str.replace('.N .W','N, W')
df_4.Area = df_4.Area.str.replace('.N-.W','N, W')
#df_4.Area[df_4.Area.str.endswith(' ')]=''
#df_4.Area.iloc[5386] = 'Unknown'
df_4.Area[df_4.Area == 'Nan'] = np.NaN
df_4.Area[df_4.Area == ''] = np.NaN
df_4.Area.iloc[4187] = np.NaN
df_4.Area.iloc[6083] = np.NaN
df_4.Area.iloc[3984] = np.NaN

#################################################################################
############################  Location    #######################################
#################################################################################
df_5 = df_4.copy()
df_5.Location.value_counts()
set(df_5.Location)
df_5.Location.isnull().sum()

location_string = df_5.Location.to_string() #Convertir la columna en string
location_string = strip_accents(location_string) #Quitar los acentos y poner 'Nan' en valores vacios
location_string = re.sub('\d', '', location_string) #Quitar el número del principio
location_string = [x.split(';') for x in location_string.split('\n')] #Convertir el string a lista
df_5.Location = pd.DataFrame(location_string) #Almacenar la lista en el DataFrame
df_5.Location = df_5.Location.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
df_5.Location = df_5.Location.apply(lambda x: str.title(x)) #Capitalizar
df_5.Location[df_5.Location == 'Nan'] = np.NaN

#Encontrar matches dentro de la columna, con base al primer string de cada registro
#location_string_2 = list(df_5.Location)
#location_string_3 = [e.split() for e in location_string_2]
#
#list_dup_locations1 = []
#for e in location_string_3:
#    list_dup_locations1.append(e[0])
#    
##list_dup_locations2 = []
##for e in location_string_3:
##    list_dup_locations2.append(e[:2])
#
#sorted(set(list_dup_locations1))
##sorted(set(list_dup_locations2))
#
#[s for s in location_string_3 if any(xs in s for xs in list_dup_locations1)]

#################################################################################
############################  Activity    #######################################
#################################################################################
df_6 = df_5.copy()
df_6.Activity.value_counts()
"""
Surfing                                                                                                   971
Swimming                                                                                                  869
Fishing                                                                                                   431
Spearfishing                                                                                              333
Bathing                                                                                                   162
Wading                                                                                                    149
Diving                                                                                                    127
Standing                                                                                                   99
Snorkeling                                                                                                 89
Scuba diving                                                                                               76
Body boarding                                                                                              61
Body surfing                                                                                               49
Swimming                                                                                                   47
Kayaking                                                                                                   33
Fell overboard                                                                                             32
Treading water                                                                                             32
Pearl diving                                                                                               32
Boogie boarding                                                                                            29
Free diving                                                                                                29
Windsurfing                                                                                                19
Walking                                                                                                    17
Boogie Boarding                                                                                            16
Shark fishing                                                                                              15
Floating                                                                                                   14
Canoeing                                                                                                   13
Fishing                                                                                                    13
Surf-skiing                                                                                                12
Surf fishing                                                                                               12
Surf skiing                                                                                                12
Rowing                                                                                                    
"""

activity_string = df_6.Activity.to_string() #Convertir la columna en string
activity_string = strip_accents(activity_string)
activity_string = re.sub('\d', '', activity_string) #Quitar el número del principio
activity_string = [x.split(';') for x in activity_string.split('\n')] #Convertir el string a lista
df_6.Activity = pd.DataFrame(activity_string) #Almacenar la lista en el DataFrame
df_6.Activity = df_6.Activity.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio

#### Clasificación:
df_6.Activity = df_6.Activity.apply(lambda x: x.lower()) #Lower
activity_string = list(df_6.Activity)
#activity_string = [e.split() for e in activity_string] #Hacer lista de listas

#'ee' in activity_string[4]
#'surf' in activity_string[210]

for e in activity_string:
    if 'surf' in e:
        activity_string[activity_string.index(e)] = 'Surfing'
    elif 'swim' in e:
        activity_string[activity_string.index(e)]= 'Swimming'
    elif 'fishing' in e:
        activity_string[activity_string.index(e)]= 'Fishing'
    elif 'crabbing' in e:
        activity_string[activity_string.index(e)]= 'Fishing'
    elif 'spear' in e:
        activity_string[activity_string.index(e)]= 'Fishing' 
    elif 'bat' in e:
        activity_string[activity_string.index(e)]= 'Bathing'
    elif 'wading' in e:
        activity_string[activity_string.index(e)]= 'Wading'
    elif 'dive' in e:
        activity_string[activity_string.index(e)]= 'Diving'
    elif 'stand' in e:
        activity_string[activity_string.index(e)]= 'Standing'
    elif 'snork' in e:
        activity_string[activity_string.index(e)]= 'Snorkeling'
    elif 'board' in e:
        activity_string[activity_string.index(e)]= 'Boarding'
    elif 'kayak' in e:
        activity_string[activity_string.index(e)]= 'Kayaking'
    elif 'Fell overboard' in e:
        activity_string[activity_string.index(e)]= 'Boarding'
    elif 'walk' in e:
        activity_string[activity_string.index(e)]= 'Walking'
    elif 'float' in e:
        activity_string[activity_string.index(e)]= 'Floating'
    elif 'canoe' in e:
        activity_string[activity_string.index(e)]= 'Canoeing'
    elif 'sail' in e:
        activity_string[activity_string.index(e)]= 'Sailing'
    elif 'boat' in e:
        activity_string[activity_string.index(e)]= 'Boating'
    elif 'skiing' in e:
        activity_string[activity_string.index(e)]= 'Skiing'
    elif 'playing' in e:
        activity_string[activity_string.index(e)]= 'Playing'
    elif 'feed' in e:
        activity_string[activity_string.index(e)]= 'Feeding shark'
    elif 'tagg' in e:
        activity_string[activity_string.index(e)]= 'Tagging sharks'
    elif 'splash' in e:
        activity_string[activity_string.index(e)]= 'Splashing'
    elif 'fell' in e:
        activity_string[activity_string.index(e)]= 'Fell into water'
    elif 'bend' in e:
        activity_string[activity_string.index(e)]= 'Fell into water'
    elif 'sunk' in e:
        activity_string[activity_string.index(e)]= 'Fell into water'
    elif 'sink' in e:
        activity_string[activity_string.index(e)]= 'Sunk'
    elif 'photo' in e:
        activity_string[activity_string.index(e)]= 'Photographing'
    elif 'adrift' in e:
        activity_string[activity_string.index(e)]= 'Adrift'
    elif 'air' in e:
        activity_string[activity_string.index(e)]= 'Aircraft accident'    
    elif 'collecting' in e:
        activity_string[activity_string.index(e)]= 'Collecting fish'
    elif 'gather' in e:
        activity_string[activity_string.index(e)]= 'Collecting fish'
    elif 'dived' in e:
        activity_string[activity_string.index(e)]= 'Diving'
    elif 'film' in e:
        activity_string[activity_string.index(e)]= 'Filming'
    elif 'net' in e:
        activity_string[activity_string.index(e)]= 'Netting'
    elif 'hunt' in e:
        activity_string[activity_string.index(e)]= 'Hunting'
    elif 'jump' in e:
        activity_string[activity_string.index(e)]= 'Fell into water'
    elif 'row' in e:
        activity_string[activity_string.index(e)]= 'Rowing'
    elif 'wash' in e:
        activity_string[activity_string.index(e)]= 'Washing'
    elif 'wreck' in e:
        activity_string[activity_string.index(e)]= 'Wrecking'
    elif 'watch' in e:
        activity_string[activity_string.index(e)]= 'Watching'
    elif 'catch' in e:
        activity_string[activity_string.index(e)]= 'Fishing'
    elif 'unkown' in e:
        activity_string[activity_string.index(e)]= 'Unknown'
    elif 'sea disaster' in e:
        activity_string[activity_string.index(e)]= 'Sea disaster'
    else:
        activity_string[activity_string.index(e)]= 'Unknown'
        
df_6.Activity = pd.DataFrame(activity_string)

df_6.Activity = df_6.Activity.str.replace('"','')
df_6.Activity = df_6.Activity.str.replace("' ",'')
df_6.Activity = df_6.Activity.str.replace(',-','')

df_6.Activity = df_6.Activity.apply(lambda x: str.title(x)) #Capitalizar
#
#df_6.Activity.iloc[5437] = 'Unkown'
#df_6.Activity.iloc[5454] = 'Unkown'
#df_6.Activity.iloc[5481] = 'Unkown'
#df_6.Activity.iloc[5803] = 'Unkown'
#df_6.Activity.iloc[5481] = 'Unkown'
#df_6.Activity.iloc[1678] = 'Unkown'
#df_6.Activity.iloc[4701] = 'Unkown'
#df_6.Activity.iloc[5666] = 'Unkown'
#df_6.Activity.iloc[2543] = 'Unkown'
#df_6.Activity.iloc[3823] = 'Unkown'
#df_6.Activity.iloc[5393] = 'Unkown'
#df_6.Activity.iloc[5420] = 'Unkown'
#df_6.Activity.iloc[5985] = 'Unkown'
#df_6.Activity[df_6.Activity == 'NaN'] = 'Unkown'
df_6.Activity.value_counts()

#################################################################################
############################  Names    #######################################
#################################################################################
df_7 = df_6.copy()

df_7.Name.value_counts()

names_string = df_7.Name.to_string() #Convertir la columna en string
names_string = strip_accents(names_string)
names_string = re.sub('\d', '', names_string) #Quitar el número del principio
names_string = [x.split(';') for x in names_string.split('\n')] #Convertir el string a lista
df_7.Name = pd.DataFrame(names_string) #Almacenar la lista en el DataFrame
df_7.Name = df_7.Name.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio

df_7.Name = df_7.Name.apply(lambda x: x.lower()) #Lower
names_string = list(df_7.Name)

###############################################################
for e in names_string:
    if 'male' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'female' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'woman' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'teacher' in e:
        names_string[names_string.index(e)] = 'Unknown'    
    elif 'people' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'dive' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'soldier' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'girl' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'boy' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'sailor' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'dinghy' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'men' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'crew' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'pilot' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'guard' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'boat' in e:
        names_string[names_string.index(e)] = 'Unknown'
    elif 'child' in e:
        names_string[names_string.index(e)] = 'Unknown' 
    elif 'native' in e:
        names_string[names_string.index(e)] = 'Unknown' 
    elif 'fisherm' in e:
        names_string[names_string.index(e)] = 'Unknown' 

df_7.Name = pd.DataFrame(names_string)


df_7.Name = df_7.Name.apply(lambda x: re.sub(r"^(.*?(\boccupant\b))", '', x))
df_7.Name = df_7.Name.apply(lambda x: re.sub(r"^(.*?(\boccupants\b))", '', x))


df_7.Name = df_7.Name.str.replace(' :','')
df_7.Name = df_7.Name.str.replace("' ",'')
df_7.Name = df_7.Name.str.replace('"','')
df_7.Name = df_7.Name.str.replace('" ','')
df_7.Name = df_7.Name.str.replace(',','')
df_7.Name = df_7.Name.str.replace(', ','')
df_7.Name = df_7.Name.str.replace(':     ','')
df_7.Name = df_7.Name.str.replace(':','')
df_7.Name = df_7.Name.str.replace(': ','')
df_7.Name = df_7.Name.str.replace('occupant: ','')
df_7.Name = df_7.Name.str.replace('occupants: ','')
df_7.Name = df_7.Name.str.replace('occupant:     ','')

df_7.Name[df_7.Name.str.startswith('a ')]=''

df_7.Name[df_7.Name == 'anonymous'] = 'Unknown'
df_7.Name[df_7.Name == 'unidentified'] = 'Unknown'
df_7.Name[df_7.Name == 'unkown'] = 'Unknown'
df_7.Name[df_7.Name == 'nan'] = 'Unknown'
df_7.Name[df_7.Name == ''] = 'Unknown'

df_7.Name = df_7.Name.apply(lambda x: str.title(x)) #Capitalizar

df_7.Name.value_counts()


#################################################################################
############################  Sex    #######################################
#################################################################################

df_8 = df_7.copy()

df_8.rename(columns={'Sex ':'Sex'}, inplace=True)
df_8.Sex.value_counts()
df_8.Sex.isnull().sum()
#
#df_8.Sex[df_8.Sex == 'lli'] #1624
#df_8.Sex[df_8.Sex == 'M '] #563, 1587
#df_8.Sex[df_8.Sex == '.']#5437
#df_8.Sex[df_8.Sex == 'N']#4938, 6131

df_8.Sex[df_8.Sex == 'lli'] = np.NaN
df_8.Sex[df_8.Sex == '.'] = np.NaN
df_8.Sex[df_8.Sex == 'N'] = np.NaN
df_8.Sex[df_8.Sex == 'M '] = 'M'

df_8.Sex = df_8.Sex.fillna(method = 'backfill')

#################################################################################
############################  Age    #######################################
#################################################################################
df_9 = df_8.copy()

df_9.Age.value_counts()
df_9.Age.isnull().sum()

(df_9.Age.apply(lambda x: re.findall(r"^.\d+", str(x)))).value_counts()

df_9.Age = df_9.Age.apply(lambda x: re.findall(r"^.\d+", str(x)))
df_9.Age = df_9.Age.apply(lambda x: str(x))

df_9.Age = df_9.Age.str.replace("[",'')
df_9.Age = df_9.Age.str.replace("]",'')
df_9.Age = df_9.Age.str.replace("'",'')
df_9.Age = df_9.Age.str.replace(" ",'')
df_9.Age[df_9.Age == ''] = np.NaN
df_9.Age.loc[3364] = 50
#df_9.Age[df_9.Age == 'Unknown'] = np.NaN


df_9.Age = df_9.Age.apply(lambda x: float(x))
df_9.Age = df_9.Age.fillna(df_9.Age.mean())
df_9.Age = df_9.Age.apply(lambda x: int(x))
df_9.Age = df_9.Age.fillna(df_9.Age.mean())

df_9.to_csv('jojoa.csv')

#################################################################################
############################  Injury   #######################################
#################################################################################
df_10 = df_9.copy()

df_10.Injury.value_counts()
df_10.Injury.isnull().sum()

injury_string = df_10.Injury.to_string() #Convertir la columna en string
injury_string = strip_accents(injury_string)
injury_string = re.sub('\d', '', injury_string) #Quitar el número del principio
injury_string = [x.split(';') for x in injury_string.split('\n')] #Convertir el string a lista
df_10.Injury = pd.DataFrame(injury_string) #Almacenar la lista en el DataFrame
df_10.Injury = df_10.Injury.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
df_10.Injury[df_10.Injury == 'NaN'] = 'Unknown'

df_10.Injury = df_10.Injury.apply(lambda x: x.lower()) #Lower
injury_string = list(df_10.Injury)

for e in injury_string:
    if 'no injury' in e:
        injury_string[injury_string.index(e)] = 'no injury'
    elif 'minor' in e:
        injury_string[injury_string.index(e)] = 'minor injury'
#    elif 'details' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'probable' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'possibly' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'possible' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'unkown' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'survived' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'people' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'shark' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'fatal' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'remains' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'hooked' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'disappeared' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'bitten' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'boat' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
#    elif 'body' in e:
#        injury_string[injury_string.index(e)] = 'unknown'
    elif 'wrist' in e:
        injury_string[injury_string.index(e)] = 'hand injury'
    elif 'thump' in e:
        injury_string[injury_string.index(e)] = 'hand injury'
    elif 'hand' in e:
        injury_string[injury_string.index(e)] = 'hand injury'
    elif 'palm' in e:
        injury_string[injury_string.index(e)] = 'hand injury'
    elif 'finger' in e:
        injury_string[injury_string.index(e)] = 'hand injury'
    elif 'arm' in e:
        injury_string[injury_string.index(e)] = 'arm injury'
    elif 'shoulder' in e:
        injury_string[injury_string.index(e)] = 'arm injury'
    elif 'elbow' in e:
        injury_string[injury_string.index(e)] = 'arm injury'
    elif 'fore' in e:
        injury_string[injury_string.index(e)] = 'arm injury'
    elif 'torso' in e:
        injury_string[injury_string.index(e)] = 'torso injury'
    elif 'abdomen' in e:
        injury_string[injury_string.index(e)] = 'abdomen injury'
    elif 'foot' in e:
        injury_string[injury_string.index(e)] = 'foot injury'
    elif 'feet' in e:
        injury_string[injury_string.index(e)] = 'foot injury'
    elif 'toe' in e:
        injury_string[injury_string.index(e)] = 'foot injury'
    elif 'ankle' in e:
        injury_string[injury_string.index(e)] = 'foot injury'
    elif 'foot' in e:
        injury_string[injury_string.index(e)] = 'foot injury'
    elif 'leg' in e:
        injury_string[injury_string.index(e)] = 'leg injury'
    elif 'knee' in e:
        injury_string[injury_string.index(e)] = 'leg injury'
    elif 'heel' in e:
        injury_string[injury_string.index(e)] = 'leg injury'
    elif 'calf' in e:
        injury_string[injury_string.index(e)] = 'leg injury'
    elif 'thigh' in e:
        injury_string[injury_string.index(e)] = 'leg injury'
    elif 'hip' in e:
        injury_string[injury_string.index(e)] = 'hip injury'
    elif 'waist' in e:
        injury_string[injury_string.index(e)] = 'hip injury'
    elif 'head' in e:
        injury_string[injury_string.index(e)] = 'head injury'
    elif 'shin' in e:
        injury_string[injury_string.index(e)] = 'face injury'
    elif 'face' in e:
        injury_string[injury_string.index(e)] = 'face injury'
    elif 'facial' in e:
        injury_string[injury_string.index(e)] = 'face injury'
    elif 'jaw' in e:
        injury_string[injury_string.index(e)] = 'face injury'
    elif 'cheek' in e:
        injury_string[injury_string.index(e)] = 'face injury'
    elif 'chest' in e:
        injury_string[injury_string.index(e)] = 'chest injury'
    elif 'buttock' in e:
        injury_string[injury_string.index(e)] = 'buttocks injury'
    else:
        injury_string[injury_string.index(e)] = 'unknown'

df_10.Injury = pd.DataFrame(injury_string)

df_10.Injury = df_10.Injury.apply(lambda x: str.title(x)) #Capitalizar

df_10.to_csv('jojoa.csv')
#################################################################################
############################  Fatal   #######################################
#################################################################################
df_11 = df_10.copy()

df_11['Fatal (Y/N)'].value_counts()

df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == ' N'] = 'N'
df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == 'M'] = 'Unknown'
df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == '2017'] = 'Unknown'
df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == 'N '] = 'N'
df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == 'y'] = 'Y'
df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == '2017'] = 'Unknown'
df_11['Fatal (Y/N)'][df_11['Fatal (Y/N)'] == 'UNKNOWN'] = 'Unknown'



#################################################################################
############################  Time   #######################################
#################################################################################
df_12 = df_11.copy()

df_12.Time.value_counts()

(df_12.Time.apply(lambda x: re.findall(r"^.\d+.\d+", str(x)))).value_counts()

df_12.Time = df_12.Time.apply(lambda x: re.findall(r"^.\d+.\d+", str(x)))
df_12.Time = df_12.Time.apply(lambda x: str(x))

df_12.Time = df_12.Time.str.replace("[",'')
df_12.Time = df_12.Time.str.replace("]",'')
df_12.Time = df_12.Time.str.replace(">",'')
df_12.Time = df_12.Time.str.replace("<",'')
df_12.Time = df_12.Time.str.replace("j",'h')

df_12.Time[df_12.Time == ''] = 'Unknown'

#df_12.Time = df_12.Time.str.replace("h",':')

#df_12.Time.apply(lambda x: pd.to_datetime(x,format='%H:%M',errors='coerce'))

#################################################################################
############################  species   #######################################
#################################################################################
df_13 = df_12.copy()

df_13.rename(columns={'Species ':'Species'},inplace=True)
df_13.Species.value_counts()

species_string = df_13.Species.to_string() #Convertir la columna en string
species_string = strip_accents(species_string)
species_string = re.sub('\d', '', species_string) #Quitar el número del principio
species_string = [x.split(';') for x in species_string.split('\n')] #Convertir el string a lista
df_13.Species = pd.DataFrame(species_string) #Almacenar la lista en el DataFrame
df_13.Species = df_13.Species.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
df_13.Species[df_13.Species == 'NaN'] = 'Unknown'

df_13.Species = df_13.Species.apply(lambda x: x.lower()) #Lower
species_string = list(df_13.Species)

for e in species_string:
    if 'black' in e:
        species_string[species_string.index(e)] = 'black tip shark'
    elif 'limbatus' in e:
        species_string[species_string.index(e)] = 'black tip shark'
    elif 'blue' in e:
        species_string[species_string.index(e)] = 'blue shark'
    elif 'dog' in e:
        species_string[species_string.index(e)] = 'dog shark'
    elif 'tiger' in e:
        species_string[species_string.index(e)] = 'tiger shark'
    elif 'limbatus' in e:
        species_string[species_string.index(e)] = 'black tip shark'
    elif 'whale' in e:
        species_string[species_string.index(e)] = 'blue whale shark'
    elif 'gumm' in e:
        species_string[species_string.index(e)] = 'gummy shark'
    elif 'gray' in e:
        species_string[species_string.index(e)] = 'grey shark'
    elif 'grey' in e:
        species_string[species_string.index(e)] = 'grey shark'
    elif 'sand' in e:
        species_string[species_string.index(e)] = 'sand shark'
    elif 'white sh' in e:
        species_string[species_string.index(e)] = 'white shark'
    elif 'hammer' in e:
        species_string[species_string.index(e)] = 'hammerhead shark'
    elif 'dusk' in e:
        species_string[species_string.index(e)] = 'dusky shark'
    elif 'macruru' in e:
        species_string[species_string.index(e)] = 'dusky shark'
    elif 'gray' in e:
        species_string[species_string.index(e)] = 'grey shark'
    elif 'bull' in e:
        species_string[species_string.index(e)] = 'bull shark'
    elif 'leucas' in e:
        species_string[species_string.index(e)] = 'bull shark'
    elif 'whitet' in e:
        species_string[species_string.index(e)] = 'whitetip shark'
    elif 'silver' in e:
        species_string[species_string.index(e)] = 'silvertip shark'        
    elif 'albimarginatus' in e:
        species_string[species_string.index(e)] = 'silvertip shark'
    elif 'spinn' in e:
        species_string[species_string.index(e)] = 'spinner shark'
    elif 'zambe' in e:
        species_string[species_string.index(e)] = 'zambesi shark'
    elif 'wobb' in e:
        species_string[species_string.index(e)] = 'wobbewong shark'
    elif 'thresh' in e:
        species_string[species_string.index(e)] = 'thresher shark'
    elif 'copp' in e:
        species_string[species_string.index(e)] = 'copper shark'
    elif 'carpet' in e:
        species_string[species_string.index(e)] = 'carpet shark'
    elif 'angel' in e:
        species_string[species_string.index(e)] = 'angel shark'
    elif 'bronze' in e:
        species_string[species_string.index(e)] = 'bronze whaler shark'
    elif 'galapa' in e:
        species_string[species_string.index(e)] = 'galapagos shark'
    elif 'nurse' in e:
        species_string[species_string.index(e)] = 'nurse shark'
    elif 'gobli' in e:
        species_string[species_string.index(e)] = 'goblin shark'
    elif 'lemon' in e:
        species_string[species_string.index(e)] = 'lemon shark'
    elif 'mako' in e:
        species_string[species_string.index(e)] = 'mako shark'
    elif 'porbeagle' in e:
        species_string[species_string.index(e)] = 'porbeagle shark'
    elif 'raggedtooth' in e:
        species_string[species_string.index(e)] = 'raggedtooth shark'
    elif 'seven' in e:
        species_string[species_string.index(e)] = 'sevengill shark'
    elif 'banj' in e:
        species_string[species_string.index(e)] = 'banjo shark'
    elif 'reef' in e:
        species_string[species_string.index(e)] = 'caribbean reef shark'
    elif 'shovel' in e:
        species_string[species_string.index(e)] = 'shovelnose shark'
    elif 'silk' in e:
        species_string[species_string.index(e)] = 'silky shark'
    else:
        species_string[species_string.index(e)] = 'unknown'

df_13.Species = pd.DataFrame(species_string)

df_13.Species = df_13.Species.apply(lambda x: str.title(x)) #Capitalizar
#################################################################################
#################################################################################
##########################  NA's #############################
#################################################################################
#################################################################################

df_14 = df_13.copy()

df_14.isnull().sum()
"""
Case Number                  1 drop
Date                       906
Year                         2 drop
Type                         4 drop
Country                      0
Area                         0
Location                     0
Activity                     0
Name                         0
Sex                        569
Age                          0
Injury                       0
Fatal (Y/N)                539
Time                         0
Species                      0
Investigator or Source      17
pdf                          0
href formula                 1
href                         0
Case Number.1                0
Case Number.2                0
original order               0
Unnamed: 22               6301
Unnamed: 23               6300
"""

df_14.Date = df_14.Date.fillna('Unknown')
#df_14.Area = df_14.Area.fillna('Unknown')
df_14.Sex = df_14.Sex.fillna(method = 'backfill')
df_14.Age = df_14.Age.fillna(df_14.Sex.mean())
#df_14.Activity = df_14.Activity.fillna('Unknown')
df_14['Fatal (Y/N)'] = df_14['Fatal (Y/N)'].fillna(method = 'backfill')
#df_14.Time = df_14.Time.fillna('Unknown')
#df_14.Species = df_14.Species.fillna('Unknown')




df_13.to_csv('jojoa.csv')
