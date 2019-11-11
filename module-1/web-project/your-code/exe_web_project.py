# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 08:38:55 2019

@author: luisf
"""

from web_project_anime import  *

url_pattern = 'https://myanimelist.net/topanime.php?limit=%s.html'
anime_to_scrape = 500

def exe():
    my_scrapping = scrape_anime_bruh(url_pattern, anime_to_scrape, sleep_interval=3, content_parser=html_links_parser)
    scraping_content = my_scrapping.kickstart()
    link_list = [j for e in scraping_content for j in e]
    dic_anime = web_scrapping(link_list)
    df =dic_to_df(dic_anime)
    return df.to_csv('Anime.csv')

exe()
