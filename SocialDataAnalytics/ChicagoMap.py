#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 19:11:28 2019

@author: rwtatko@us.ibm.com
"""

import ChicagoData
import pandas as pd
import geopandas as gpd
import seaborn
import pip
import subprocess
import sys
import matplotlib as plt

import folium
import leaflet
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from folium.plugins import Search
import geopandas as gpd

shp_path = '/Users/rwtatko@us.ibm.com/SocialDataAnalytics/WelfareData/CTA_RailLines/CTA_RailLines.shp'

rail_shapefile = gpd.read_file(shp_path)

rail_shapefile.to_file('ChicagoRail.geojson', driver='GeoJSON')

chi_coordinates = (41.88, -87.63)
max_coordinates = [[41.3228, -88.4271],[42.2783,-87.2727]]

map_chi = folium.Map()
map_chi = folium.Map(location=chi_coordinates,tiles='cartodbpositron',maxBounds=max_coordinates,zoom_start=12,min_zoom=10) 

# Add Markers for Service Centers
for i in range(0,len(df_main)):
    if (df_main.iloc[i][2]=="Children Services" or df_main.iloc[i][2]=="Youth Services"):
        folium.Marker(
            location=[df_main.iloc[i][11], df_main.iloc[i][12]],
            #popup=str(df_main.iloc[i][1])+' : '+str(df_main.iloc[i][3]),
            popup= folium.Popup('<a href="' + 'https://www.metrofamily.org/programs-and-services/education/early-learning-head-start/' 
                            + '"target="_blank">' 
                            + str(df_main.iloc[i][1]) +' : '+str(df_main.iloc[i][3]) +'</a>'),
            icon=folium.Icon(color='blue', icon='child', prefix='fa')
            ).add_to(map_chi)
    elif df_main.iloc[i][2]=="Human Services Delivery":
        folium.Marker(
            location=[df_main.iloc[i][11], df_main.iloc[i][12]],
            popup=str(df_main.iloc[i][1])+' : '+str(df_main.iloc[i][3]),
            icon=folium.Icon(color='orange', icon='cutlery', prefix='fa')
            ).add_to(map_chi)
    elif df_main.iloc[i][2]=="Homeless Services":
        folium.Marker(
            location=[df_main.iloc[i][11], df_main.iloc[i][12]],
            popup=str(df_main.iloc[i][1])+' : '+str(df_main.iloc[i][3]),
            icon=folium.Icon(color='beige', icon='home', prefix='fa')
            ).add_to(map_chi)
    elif df_main.iloc[i][2]=="Domestic Violence":
        folium.Marker(
            location=[df_main.iloc[i][11], df_main.iloc[i][12]],
            popup=str(df_main.iloc[i][1])+' : '+str(df_main.iloc[i][3]),
            icon=folium.Icon(color='purple', icon='heart', prefix='fa')
            ).add_to(map_chi)
    elif df_main.iloc[i][2]=="Healthcare":
        folium.Marker(
            location=[df_main.iloc[i][11], df_main.iloc[i][12]],
            #popup=str(df_main.iloc[i][1])+' : '+str(df_main.iloc[i][3]),
            popup= folium.Popup('<a href="' + 'https://hh.emrconnect.org/portal/default.aspx'
                            + '"target="_blank">' 
                            + str(df_main.iloc[i][1]) +' : '+str(df_main.iloc[i][3]) +'</a>'),
            icon=folium.Icon(color='red', icon='h-square', prefix='fa')
            ).add_to(map_chi)
    else:
        folium.Marker(
            location=[df_main.iloc[i][12], df_main.iloc[i][13]],
            popup=str(df_main.iloc[i][1])+' : '+str(df_main.iloc[i][3]),
            icon=folium.Icon(color='gray', icon='info', prefix='fa')
            ).add_to(map_chi)

# Add Markers for Bus Stops
mc = MarkerCluster()

for i in range(0,len(df_bus)):
    mc.add_child(
            folium.Marker(
            location=[df_bus.iloc[i][12], df_bus.iloc[i][11]],
            icon=folium.Icon(color='gray', icon='bus', prefix='fa'),
            #radius= 3,
            #color='gray',
            popup=str(df_bus.iloc[i][0])+' : '+str(df_bus.iloc[i][10]),
            Fill=True)
    )

map_chi.add_child(mc)

#Add Markers for Rail Stations

mc = MarkerCluster()

for i in range(0,len(df_rail)):
    mc.add_child(
            folium.Marker(
            location=[df_rail.iloc[i][1], df_rail.iloc[i][0]],
            icon=folium.Icon(color='gray', icon='subway', prefix='fa'),
            popup=str(df_rail.iloc[i][2])+' : '+str(df_rail.iloc[i][7]),
            Fill=True)
    )
    
map_chi.add_child(mc)

#Add Railway Line GeoJSON Mapping 

rail_dict = rail_shapefile.set_index('ASSET_ID')['LEGEND'].to_dict()

def style(feature):
    values = rail_dict.get(feature['properties']['ASSET_ID'])
    if values=='BL':
        return '#3d4dff'
    elif values=='RD':
        return '#ff3d3d'
    elif values=='PR':
        return '#a73dff'
    elif values=='ML':
        return '#ffffff'
    elif values=='BR':
        return '#897867'
    elif values=='YL':
        return '#ffe74c'
    elif values=='GR':
        return '#44ff6a'
    elif values=='OR':
        return '#ff8544'
    elif values=='PK':
        return '#ff96eb'
        
        #Railyway Colors Include:
        #BL = Blue, RD= Red, PR = Purple, ML = White, BR = Brown YL = Yellow, GR = Green, 
        #OR = Orange, PK = Pink

folium.GeoJson(rail_shapefile, name='geojson',
               style_function = lambda feature: {
               'color': style(feature),
               'opacity': 0.75,
               'weight': 6
               }).add_to(map_chi)
    
#Add Client to Map
    
folium.Marker(
            location=[41.774, -87.6482],
            icon=folium.Icon(color='darkblue', icon='user', prefix='fa'),
            popup='Thomas Household',
            draggable=False).add_to(map_chi)

#Add Work Center to Map
    
folium.Marker(
            location=[41.788477, -87.599622],
            icon=folium.Icon(color='darkpurple', icon='briefcase', prefix='fa'),
            popup='University of Chicago Workforce Placement Center',
            draggable=False).add_to(map_chi)

#Draw Lines to Nearest Public Transport

trans_pts = [[41.774, -87.6482],[41.772436,-87.654398], #tobus
             [41.774, -87.6482],[41.779027, -87.6440],   #torail
             #[41.772436,-87.654398],[41.779027, -87.6440], #frombustorail
             ]

folium.PolyLine(trans_pts,weight=5,opacity=0.65,fill_color='lightblue',
                popup='Nearest Public Transport').add_to(map_chi)
                             
#Draw Lines to Destinations Based on Matching

dest_pts = [
             #[41.774, -87.6482],[41.7754406,-87.6093209], #toChildCenter
             [41.774, -87.6482],[41.75045, -87.6632],   #toFoodPantry
             #[41.774, -87.6482],[41.788477, -87.599622], #toUChicagoWorkCenter
             [41.75045, -87.6632],[41.7754406,-87.6093209],   #fromFoodPantrytoChildCenter
             [41.7754406,-87.6093209],[41.788477, -87.599622],   #fromChildCentertoUChicagoWorkCenter
             ]

folium.PolyLine(dest_pts,weight=5,opacity=0.65,color='darkred',fill_color='darkred', 
                popup='Matched Client Services Area').add_to(map_chi)

map_chi.save(outfile='prototype.html')


