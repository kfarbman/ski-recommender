import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

pkl_file = open('df.pkl', 'rb')
df = pickle.load(pkl_file)
pkl_file.close() 

resort_urls = {'Loveland': 'colorado/loveland',
               'Arapahoe Basin': 'colorado/arapahoe-basin-ski-area',
               'Copper': 'colorado/copper-mountain-resort',
               'Eldora': 'colorado/eldora-mountain-resort',
               'Alpine Meadows': 'california/squaw-valley-usa',
               'Vail': 'colorado/vail',
               'Monarch': 'colorado/monarch-mountain',
               'Crested Butte': 'colorado/crested-butte-mountain-resort',
               'Taos': 'new-mexico/taos-ski-valley',
               'Diamond Peak': 'nevada/diamond-peak',
               'Winter Park': 'colorado/winter-park-resort',
               'Beaver Creek': 'colorado/beaver-creek'}
               
browser = webdriver.PhantomJS()

def get_elevs_colors_lifts_price(resort):
    URL = 'http://www.onthesnow.com/'+resort_urls[resort]+'/ski-resort.html'
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    stuff = soup.select('table.ovv_info tbody tr td')
    rows = [cell.text for cell in stuff]
    _, elevs, colors, lifts, price = rows
    bottom = int(''.join([x for x in elevs.split()[0] if x.isnumeric()]))
    top = int(''.join([x for x in elevs.split()[2] if x.isnumeric()]))
    greens = int(''.join([x for x in colors.split()[0] if x.isnumeric()]))
    blues = int(''.join([x for x in colors.split()[1] if x.isnumeric()]))
    blacks = int(''.join([x for x in colors.split()[2] if x.isnumeric()]))
    bbs = int(''.join([x for x in colors.split()[3] if x.isnumeric()]))
    lifts = int(lifts)
    price = int(''.join([x if x.isnumeric() else '0' for x in price.split()[0]]))
    return [bottom, top, greens, blues, blacks, bbs, lifts, price]
    
elevs_colors_lifts_price = {}
for resort in resort_urls:
    elevs_colors_lifts_price[resort] = get_elevs_colors_lifts_price(resort)
    
new_cols = ['resort_bottom','resort_top','greens','blues','blacks','bbs','lifts','price']
df = df.reindex(columns=[*df.columns.tolist(), *new_cols], fill_value=0)

for resort in elevs_colors_lifts_price:
    df['resort_bottom'][df['resort'] == resort] = elevs_colors_lifts_price[resort][0]
    df['resort_top'][df['resort'] == resort] = elevs_colors_lifts_price[resort][1]
    df['greens'][df['resort'] == resort] = elevs_colors_lifts_price[resort][2]
    df['blues'][df['resort'] == resort] = elevs_colors_lifts_price[resort][3]
    df['blacks'][df['resort'] == resort] = elevs_colors_lifts_price[resort][4]
    df['bbs'][df['resort'] == resort] = elevs_colors_lifts_price[resort][5]
    df['lifts'][df['resort'] == resort] = elevs_colors_lifts_price[resort][6]
    df['price'][df['resort'] == resort] = elevs_colors_lifts_price[resort][7]
    
output = open('mtn_df.pkl', 'wb')
pickle.dump(df, output)
output.close()

print(df.head())