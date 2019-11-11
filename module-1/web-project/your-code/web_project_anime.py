# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:28:37 2019

@author: luisf
"""

import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

class scrape_anime_bruh:

    def __init__(self, url_pattern, pages_to_scrape=1, sleep_interval=-1, content_parser=None):
        self.url_pattern = url_pattern
        self.pages_to_scrape = pages_to_scrape + 1600
        self.sleep_interval = sleep_interval
        self.content_parser = content_parser
    

    def scrape_url(self, url):
        
        response = requests.get(url)
        result = self.content_parser(response.content)
        print(result)
        return result


    def kickstart(self):
        scraped = []
        for i in range(1600, self.pages_to_scrape,50):
            try:
                scraped.append(self.scrape_url(self.url_pattern % i))
                time.sleep(self.sleep_interval)
            except:
                print('Something bad is happening')     
        return scraped

def html_links_parser(content):
    
    content = bs(content, 'html.parser')
    
    lst = []
    for e in content.find_all('a', {'class':'hoverinfo_trigger fl-l fs14 fw-b'}):
        e=str(e)
        e=e.split('"')
        lst.append(e[3])
    
    content=lst
    return content

def web_scrapping(lst):
    info_animes = []
    for e in lst:
        response = requests.get(e, verify=False)
        res_text = response.text
        soupa = bs(res_text, 'html.parser')
        
        #Title:
        title_string = soupa.select('h1 span')
        title_string=str(title_string)
        time.sleep(2) #Me has salvado la vida
        title_string=title_string.split(">")
        print(title_string)
        title_string=title_string[1].replace("</span", "")
        #Type
        typo = soupa.select('span + a')
        typo = typo[0]
        typo =str(typo)
        typo =typo.split(">")
        typo = typo[1].replace("</a", "")
        print(typo)
        
        #####################################################
        ###############   Varios   ##########################
        #####################################################
        soupa_varios=soupa.findAll('div', {'class' :'spaceit'})
        #Episodes
        ep=str(soupa_varios[0])
        ep=ep.split("\n ")
        ep=ep[1].replace(" ","")
        #Status
        status=soupa.find("span", text="Status:").nextSibling
        status=str(status).split("\n")[1].strip()
        #Airing
        aired=str(soupa_varios[1])
        aired=aired.split("\n ")
        
        if 'to' in aired[1] == True:
            aired=aired[1].split("to")
            start_airing=aired[0].strip()
            end_airing=aired[1].strip()
        else:
            start_airing= aired[1].strip()
            end_airing='-'
        #Starting season
        if typo == 'TV':
            sseason=soupa.find("span", text="Premiered:").nextSibling.nextSibling
            if '>' in sseason:
                sseason=str(sseason).split(">")[1].split(" ")[0]
        else:
            sseason = '-'
        #Broadcast
        if typo == 'TV':
            broad=str(soupa_varios[2])
            broad=broad.split("\n ")
            broad=broad[1].strip()
        else:
            broad = '-'
        #Licensors
        if typo == 'TV':
            licensor=str(soupa_varios[3])
            licensor=licensor.split(">")
            licensor=licensor[4].replace('</a','')
        else:
            licensor=str(soupa_varios[2])
            licensor=licensor.split(">")
            licensor=licensor[4].replace('</a','')
        #Sources
        if typo == 'TV':
            source=str(soupa_varios[4])
            source = source.split("\n ")
            source = source[1].strip()
        else:
            source=str(soupa_varios[3])
            source = source.split("\n ")
            source = source[1].strip()
        #Duration
        if typo == 'TV':
            duration=str(soupa_varios[5])
            duration=duration.split("\n ")
            duration=duration[1].strip()
        else:
            duration=str(soupa_varios[4])
            duration=duration.split("\n ")
            duration=duration[1].strip()
        #Members
        if typo == 'TV':
            members=str(soupa_varios[7])
            members=members.split("\n ")
            members=members[1].replace('\n</div>','').strip()
        else:
            members=str(soupa_varios[6])
            members=members.split("\n ")
            members=members[1].replace('\n</div>','').strip()
        #Producers and Studio
        temp_ps=soupa.find('td')
        temp_ps=temp_ps.find_all('a')
        
        lst_ps = []
        for e in temp_ps:
            e=str(e)
            if '/anime/producer' in e:
                lst_ps.append(e)
        
        lst_ps=[e.split('>')[1].replace('</a','') for e in lst_ps]
        
        if len(lst_ps) == 0:
            producers = '-'
            studio = '-'
        else:    
            producers = ','.join(lst_ps[:len(lst_ps)-1])
            studio = lst_ps[-1]
        #Genres
        temp_genres=soupa.find('td')
        temp_genres=temp_genres.find_all('a')
        
        lst_g=[]
        for e in temp_genres:
            e=str(e)
            if '/anime/genre' in e:
                lst_g.append(e)
        
        lst_g=[e.split('>')[1].replace('</a','') for e in lst_g]
        genres=','.join(lst_g)
        #Rating
        rating=soupa.find("span", text="Rating:").nextSibling
        rating=str(rating).split("\n")[1].strip()
        #Score
        score=soupa.find("span", text="Score:").nextSibling.nextSibling
        score=str(score).split(">")[1].replace("</span",'')
        #Scored by
        scored_by=soupa.find("span", text="Ranked:").nextSibling
        scored_by = scored_by.split("#")[1]
        #Favorites
        favorites=soupa.find("span", text="Favorites:").nextSibling
        favorites= str(favorites).split("\n")[1].strip()
        #Description
        description = soupa.find('span', {'itemprop':'description'})
        description=str(description).replace('<span itemprop="description">','').replace('<br/>\n<br/>\r\n','').replace('</span>','')

        ######  Creación del DIC  #########
        dic = {'Title':title_string,
               'Type': typo,
               'Episodes': ep,
               'Status':status,
               'Start_Airing': start_airing,
               'End_Airing': end_airing,
               'Starting season':sseason,
               'Broadcast time': broad,
               'Producers':producers,
               'Licensors': licensor,
               'Studios':studio,
               'Sources': source,
               'Genres':genres,
               'Duration': duration,
               'Rating':rating,
               'Score':score,
               'Scored by': scored_by,
               'Members': members,      
               'Favorites':favorites,
               'Description':description
               }
        
        info_animes.append(dic)
    return info_animes
    

def dic_to_df(dic):
    df=pd.DataFrame(dic)
    df = df[['Title', 'Type','Episodes','Status','Start_Airing','End_Airing','Starting season','Broadcast time',
'Producers','Licensors','Studios','Sources','Genres','Duration','Rating','Score','Scored by','Members','Favorites','Description']]
    return df