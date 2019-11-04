# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 23:43:12 2019

@author: luisf
"""

from reading_and_cleaning import *

def exe(link):
	
    df=read(link)
    df=clean_casenumber_date(df)
    df=clean_year_type(df)
    df=clean_country(df)
    df=clean_area_location(df)
    df=clean_activity(df)
    df=clean_names(df)
    df=clean_sex_age(df)
    df=clean_injury(df)
    df=clean_fatal_time(df)
    df=clean_species(df)
    df=fill_na(df)
    df=drop_columns(df)
    	
    return df

dff= exe("./Documents/Python Projects/datamex1019/module-1/pandas-project/global-shark-attacks/attacks.csv")
dff.to_csv('sharks_clean.csv')

print (exe("./Documents/Python Projects/datamex1019/module-1/pandas-project/global-shark-attacks/attacks.csv"))
