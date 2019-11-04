# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:02:49 2019

@author: luisf
"""

import pandas as pd
import numpy as np
import re
import unicodedata


def read(link):
    df = pd.read_csv(link, engine='python')
    return df

#df_0_function = leer()
    
def strip_accents(text):
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError): # unicode is a default on python 3 
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

def clean_casenumber_date(df):
    
                    #################################################################################
                    ##################### Columna Case Number and Date  #####################
                    #################################################################################
    
    ### Limpiar Strings
    df['Case Number'] = df['Case Number'].str.replace('.b','').str.replace('.a','').str.replace('.R','').str.replace('.k','')
    df['Case Number'] = df['Case Number'].str.replace('.a.R','').str.replace('R2','').str.replace('R1','').str.replace('R3','').str.replace('R4','')
    df['Case Number'] = df['Case Number'].str.replace('.c','').str.replace('.j','').str.replace('.i','').str.replace('.R.a','')
    df['Case Number'] = df['Case Number'].str.replace('.d','').str.replace('.a & b','').str.replace('.m','')
    df['Case Number'] = df['Case Number'].str.replace('.e','').str.replace('.f','').str.replace('.l','')
    df['Case Number'] = df['Case Number'].str.replace('.g','').str.replace('.d.R','').str.replace('.c.R','')
    df['Case Number'] = df['Case Number'].str.replace('. ','').str.replace('.b.R','').str.replace('.R.b','')
    df['Case Number'] = df['Case Number'].str.replace('.h','').str.replace('.R.a & b','').str.replace('.x','')
    
    #Discriminar registros que estan en blanco:
    df = df[0:6302]
    
    #Hay un valor con NaN, le asignare un valor temporal para asignar NaN a los valores que empiezan con 'ND'
    #ya que es un valor inútil.
    df['Case Number'] = df['Case Number'].fillna('Unknown')
    df['Case Number'][df['Case Number'].str.startswith('ND')]=np.NaN
    
    #Después de que tenemos limpia la columna Case Number, le cambiamos el formato a esta columna como fecha y
    #asignamos estos valores a la columna Date. Ya que, Case Number es el registro de las fechas pero en formato string.
    #A los valores que sean ND (No Date) o esten vaciós, que les ponga NaT
    
    df.Date = df['Case Number'].apply(lambda x: pd.to_datetime(x,format='%Y.%m.%d',errors='coerce'))
    return df
    
#df_1_function = clean_casenumber_date(df_0_function)


def clean_year_type(df):
    
                #################################################################################
                ##################### Columna Year y Type #####################
                #################################################################################
    
    df.Year[df.Year == 0] = np.NaN
    
    #Los cambio momentaneamente para poder correr el str.startswith
    df.Type.iloc[85] = ''
    df.Type.iloc[382] = ''
    df.Type.iloc[4867] = ''
    df.Type.iloc[5705] = ''
    
    df.Type[df.Type.str.startswith('Boat')]='Boating' #No pude hacerlo en un principio debido a unos NA's
    df.Type[df.Type.str.startswith('Questiona')]='Invalid' 
    
    #Ahora si puedo hacer el startswith, sin embago, quedan 4 valores sin nada como título. Los pongo como NaN's
    df.Type.iloc[85] = np.NAN
    df.Type.iloc[382] = np.NAN
    df.Type.iloc[4867] = np.NAN
    df.Type.iloc[5705] = np.NAN
    
    return df

#df_2_function = clean_year_type(df_1_function)

def clean_country(df):
                
                #################################################################################
                ################################ Columna Country #################################
                #################################################################################

    df.Country = df.Country.apply(lambda x: str.upper(str(x)))
    df.Country[df.Country.str.startswith(' ')] = ''
    df.Country[df.Country.str.startswith('ANDAMA')]='ANDAMAN ISLANDS'
    df.Country = df.Country.str.replace('?','')
    df.Country[df.Country.str.startswith('BETWEEN POR')]='PORTUGAL'
    df.Country[df.Country.str.endswith('SRI LANKA)')]='CEYLON'
    df.Country[df.Country.str.endswith(' ')]=''
    df.Country[df.Country.str.endswith('/ ISRAEL')]='EGYPT'
    df.Country[df.Country.str.endswith('/ CAMEROON')]='EQUATORIAL GUINEA'
    df.Country[df.Country.str.endswith('/ IRAQ')]='IRAN'
    df.Country[df.Country.str.endswith('/ CROATIA')]='ITALY'
    df.Country = df.Country.str.replace('MALDIVES','MALDIVE ISLANDS')
    df.Country = df.Country.str.replace('-',' ')
    df.Country = df.Country.str.replace('BRITISH NEW GUINEA','NEW GUINEA')
    df.loc[df.Country == 'OCEAN'] #Index 5748
    df.Country[5748] = 'UNKOWN' #OCEAN es demasiado ambiguo
    df.Country[df.Country.str.startswith('PAPUA')]='NEW GUINEA'
    df.Country[df.Country.str.endswith('/ INDIAN OCEAN')]='RED SEA'
    df.Country[df.Country.str.endswith('REUNION')]='REUNION ISLAND'
    df.Country[df.Country.str.endswith('/ VANUATU')]='SOLOMON ISLANDS'
    df.Country[df.Country.str.endswith('MAARTIN')]='ST. MARTIN'
    df.Country[df.Country.str.endswith('(UAE)')]='UNITED ARAB EMIRATES'
    df.Country = df.Country.apply(lambda x: str.title(x)) #Capitalizar
    df.Country[df.Country == 'Usa'] = 'USA'
    df.Country[df.Country == 'Nan'] = np.NaN
    
    return df

#df_3_function = clean_country(df_2_function)


def clean_area_location(df):
    
            #################################################################################
            ##################################  Area  #######################################
            #################################################################################

    area_string = df.Area.to_string() #Convertir la columna en string
    area_string = strip_accents(area_string) #Quitar los acentos y poner 'Nan' en valores vacios
    area_string = re.sub('\d', '', area_string) #Quitar el número del principio
    area_string = [x.split(';') for x in area_string.split('\n')] #Convertir el string a lista
    df.Area = pd.DataFrame(area_string) #Almacenar la lista en el DataFrame
    df.Area = df.Area.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
    df.Area = df.Area.apply(lambda x: str.title(x)) #Capitalizar
    
    df.Area = df.Area.str.replace('"','')
    df.Area = df.Area.str.replace('(','').str.replace(')','')
    df.Area = df.Area.str.replace('?','')
    df.Area = df.Area.str.replace(' /',',')
    df.Area = df.Area.str.replace('.N .W','N, W')
    df.Area = df.Area.str.replace('.N-.W','N, W')
    
    df.Area[df.Area == 'Nan'] = np.NaN
    df.Area[df.Area == ''] = np.NaN
    df.Area.iloc[4187] = np.NaN
    df.Area.iloc[6083] = np.NaN
    df.Area.iloc[3984] = np.NaN
    
    location_string = df.Location.to_string() #Convertir la columna en string
    location_string = strip_accents(location_string) #Quitar los acentos y poner 'Nan' en valores vacios
    location_string = re.sub('\d', '', location_string) #Quitar el número del principio
    location_string = [x.split(';') for x in location_string.split('\n')] #Convertir el string a lista
    df.Location = pd.DataFrame(location_string) #Almacenar la lista en el DataFrame
    df.Location = df.Location.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
    df.Location = df.Location.apply(lambda x: str.title(x)) #Capitalizar
    df.Location[df.Location == 'Nan'] = np.NaN
    
    return df


#df_4_function = clean_area_location(df_3_function)


def clean_activity(df):

            #################################################################################
            ############################  Activity    #######################################
            #################################################################################
    activity_string = df.Activity.to_string() #Convertir la columna en string
    activity_string = strip_accents(activity_string)
    activity_string = re.sub('\d', '', activity_string) #Quitar el número del principio
    activity_string = [x.split(';') for x in activity_string.split('\n')] #Convertir el string a lista
    df.Activity = pd.DataFrame(activity_string) #Almacenar la lista en el DataFrame
    df.Activity = df.Activity.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
    
    #### Clasificación:
    df.Activity = df.Activity.apply(lambda x: x.lower()) #Lower
    activity_string = list(df.Activity)
    
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
            
    df.Activity = pd.DataFrame(activity_string)
    
    df.Activity = df.Activity.str.replace('"','')
    df.Activity = df.Activity.str.replace("' ",'')
    df.Activity = df.Activity.str.replace(',-','')
    
    df.Activity = df.Activity.apply(lambda x: str.title(x)) #Capitalizar
    
    return df

#df_5_function = clean_activity(df_4_function)

def clean_names(df):

            #################################################################################
            ############################  Names    #######################################
            #################################################################################
    names_string = df.Name.to_string() #Convertir la columna en string
    names_string = strip_accents(names_string)
    names_string = re.sub('\d', '', names_string) #Quitar el número del principio
    names_string = [x.split(';') for x in names_string.split('\n')] #Convertir el string a lista
    df.Name = pd.DataFrame(names_string) #Almacenar la lista en el DataFrame
    df.Name = df.Name.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
    
    df.Name = df.Name.apply(lambda x: x.lower()) #Lower
    names_string = list(df.Name)
    
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
    
    df.Name = pd.DataFrame(names_string)
        
    df.Name = df.Name.apply(lambda x: re.sub(r"^(.*?(\boccupant\b))", '', x))
    df.Name = df.Name.apply(lambda x: re.sub(r"^(.*?(\boccupants\b))", '', x))
    
    df.Name = df.Name.str.replace(' :','')
    df.Name = df.Name.str.replace("' ",'')
    df.Name = df.Name.str.replace('"','')
    df.Name = df.Name.str.replace('" ','')
    df.Name = df.Name.str.replace(',','')
    df.Name = df.Name.str.replace(', ','')
    df.Name = df.Name.str.replace(':     ','')
    df.Name = df.Name.str.replace(':','')
    df.Name = df.Name.str.replace(': ','')
    df.Name = df.Name.str.replace('occupant: ','')
    df.Name = df.Name.str.replace('occupants: ','')
    df.Name = df.Name.str.replace('occupant:     ','')
    
    df.Name[df.Name.str.startswith('a ')]=''
    
    df.Name[df.Name == 'anonymous'] = 'Unknown'
    df.Name[df.Name == 'unidentified'] = 'Unknown'
    df.Name[df.Name.str.startswith('unknown')]='Unknown'
    df.Name[df.Name == 'nan'] = 'Unknown'
    df.Name[df.Name == ''] = 'Unknown'
    
    df.Name = df.Name.apply(lambda x: str.title(x)) #Capitalizar
    
    return df

#df_6_function = clean_names(df_5_function)

def clean_sex_age(df):
            #################################################################################
            ############################  Sex    #######################################
            #################################################################################
    
    df.rename(columns={'Sex ':'Sex'}, inplace=True)

    df.Sex[df.Sex == 'lli'] = np.NaN
    df.Sex[df.Sex == '.'] = np.NaN
    df.Sex[df.Sex == 'N'] = np.NaN
    df.Sex[df.Sex == 'M '] = 'M'

    df.Sex = df.Sex.fillna(method = 'backfill')
    
    
                #################################################################################
                ############################  Age    #######################################
                #################################################################################
    
    df.Age = df.Age.apply(lambda x: re.findall(r"^.\d+", str(x)))
    df.Age = df.Age.apply(lambda x: str(x))
    
    df.Age = df.Age.str.replace("[",'')
    df.Age = df.Age.str.replace("]",'')
    df.Age = df.Age.str.replace("'",'')
    df.Age = df.Age.str.replace(" ",'')
    df.Age[df.Age == ''] = np.NaN
    df.Age.loc[3364] = 50
    
    df.Age = df.Age.apply(lambda x: float(x))
    df.Age = df.Age.fillna(df.Age.mean())
    df.Age = df.Age.apply(lambda x: int(x))
    df.Age = df.Age.fillna(df.Age.mean())
    
    return df

#df_7_function = clean_sex_age(df_6_function)
    

def clean_injury(df):
    
            #################################################################################
            ############################  Injury   #######################################
            #################################################################################


    injury_string = df.Injury.to_string() #Convertir la columna en string
    injury_string = strip_accents(injury_string)
    injury_string = re.sub('\d', '', injury_string) #Quitar el número del principio
    injury_string = [x.split(';') for x in injury_string.split('\n')] #Convertir el string a lista
    df.Injury = pd.DataFrame(injury_string) #Almacenar la lista en el DataFrame
    df.Injury = df.Injury.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
    df.Injury[df.Injury == 'NaN'] = 'Unknown'
    
    df.Injury = df.Injury.apply(lambda x: x.lower()) #Lower
    injury_string = list(df.Injury)
    
    for e in injury_string:
        if 'no injury' in e:
            injury_string[injury_string.index(e)] = 'no injury'
        elif 'minor' in e:
            injury_string[injury_string.index(e)] = 'minor injury'
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
    
    df.Injury = pd.DataFrame(injury_string)
    
    df.Injury = df.Injury.apply(lambda x: str.title(x)) #Capitalizar
    
    return df

#df_8_function = clean_injury(df_7_function)

def clean_fatal_time(df):
    
            #################################################################################
            ############################  Fatal   #######################################
            #################################################################################
    
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == ' N'] = 'N'
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == 'M'] = 'Unknown'
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == '2017'] = 'Unknown'
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == 'N '] = 'N'
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == 'y'] = 'Y'
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == '2017'] = 'Unknown'
    df['Fatal (Y/N)'][df['Fatal (Y/N)'] == 'UNKNOWN'] = 'Unknown'
    
    
            
            #################################################################################
            ############################  Time   #######################################
            #################################################################################
    
    df.Time = df.Time.apply(lambda x: re.findall(r"^.\d+.\d+", str(x)))
    df.Time = df.Time.apply(lambda x: str(x))
    
    df.Time = df.Time.str.replace("[",'')
    df.Time = df.Time.str.replace("]",'')
    df.Time = df.Time.str.replace(">",'')
    df.Time = df.Time.str.replace("<",'')
    df.Time = df.Time.str.replace("j",'h')

    df.Time[df.Time == ''] = 'Unknown'
    
    return df

#df_9_function = clean_fatal_time(df_8_function)

def clean_species(df):
    
            #################################################################################
            ############################  species   #######################################
            #################################################################################

    df.rename(columns={'Species ':'Species'},inplace=True)
    species_string = df.Species.to_string() #Convertir la columna en string
    species_string = strip_accents(species_string)
    species_string = re.sub('\d', '', species_string) #Quitar el número del principio
    species_string = [x.split(';') for x in species_string.split('\n')] #Convertir el string a lista
    df.Species = pd.DataFrame(species_string) #Almacenar la lista en el DataFrame
    df.Species = df.Species.apply(lambda x: re.sub(r"^\s+", "", x)) #Quitar espacios del principio
    df.Species[df.Species == 'NaN'] = 'Unknown'
    
    df.Species = df.Species.apply(lambda x: x.lower()) #Lower
    species_string = list(df.Species)
    
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
    
    df.Species = pd.DataFrame(species_string)
    
    df.Species = df.Species.apply(lambda x: str.title(x)) #Capitalizar
    
    return df

def fill_na(df):
    
    df['Fatal (Y/N)'] = df['Fatal (Y/N)'].fillna(method = 'backfill')
    df.Type = df.Type.fillna(method = 'backfill')
    df.Date = df.Date.fillna('Unknown')
    df['Case Number'] = df['Case Number'].fillna('Unknown')
    df.Year = df.Year.fillna('Unknown')
    df.Country = df.Country.fillna('Unknown')
    df.Area = df.Area.fillna('Unknown')
    df.Location = df.Location.fillna('Unknown')
    df['Investigator or Source'] = df['Investigator or Source'].fillna('Unknown')
    
    return df

def drop_columns(df):
    df = df.drop(columns=['Case Number.1', 'Case Number.2', 'Unnamed: 22', 'Unnamed: 23'])
    
    return df

