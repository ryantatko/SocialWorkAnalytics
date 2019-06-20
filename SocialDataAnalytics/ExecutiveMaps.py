#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 09:23:08 2019

@author: rwtatko@us.ibm.com
"""

import ChicagoData as cd
import pandas as pd
import geopandas as gpd
import json 

import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

zip_shp_path = '/Users/rwtatko@us.ibm.com/SocialDataAnalytics/WelfareData/Chicago_ZIP_Boundaries/Chi_Zip.shp'

zip_shapefile = gpd.read_file(zip_shp_path)

zip_shapefile.to_file('ChicagoZIP.geojson', driver='GeoJSON')
    
chi_coordinates = (41.88, -87.63)
max_coordinates = [[41.3228, -88.4271],[42.2783,-87.2727]]


#~~~~~~~~~~FOOD DESERT MAP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

fd_dsrt_map = folium.Map()
fd_dsrt_map = folium.Map(location=chi_coordinates,tiles='cartodbpositron',maxBounds=max_coordinates,zoom_start=11,min_zoom=10) 

#Add Markers for Food Pantry Centers
"""
for i in range(0,len(cd.df_pantry)):
    folium.Marker(
            location=[cd.df_pantry.iloc[i][23], cd.df_pantry.iloc[i][24]],
            popup=cd.df_pantry.iloc[i][4],
            icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
            ).add_to(fd_dsrt_map)
"""

# List comprehension to make out list of lists
fd_heat_data = [[row['Latitude'],row['Longitude']] for index, row in df_pantry.iterrows()]

# Plot it on the map
HeatMap(fd_heat_data, name='Food Pantries').add_to(fd_dsrt_map)

zip_shapefile.zip = pd.to_numeric(zip_shapefile.zip, errors='coerce')

bins = list(df_lunch['Enrollment'].quantile([0,0.15,0.25,0.5,0.75,0.85,1]))

fd_dsrt_map.choropleth(
 geo_data=zip_shapefile,
 name='Subsidized Lunch Locations',
 data=cd.df_lunch,
 columns=['Zip 5','Enrollment'],
 key_on='feature.properties.zip',
 fill_color='OrRd',
 fill_opacity=0.35,
 line_opacity=0.75,
 bins=bins,
 legend_name='Subsidized Lunch Enrollment'
)
folium.LayerControl().add_to(fd_dsrt_map)


fd_dsrt_map.save(outfile='fd_dsrt_prototype.html')


#~~~~~~~EARLY LEARNING CENTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

chld_cr_map = folium.Map()
chld_cr_map = folium.Map(location=chi_coordinates,tiles='cartodbpositron',maxBounds=max_coordinates,zoom_start=11,min_zoom=10) 

"""
#Add Markers for Early Learning Centers
for i in range(0,len(cd.df_el)):
    folium.Marker(
            location=[cd.df_el.iloc[i][20], cd.df_el.iloc[i][21]],
            popup=cd.df_el.iloc[i][1],
            icon=folium.Icon(color='blue', icon='child', prefix='fa')
            ).add_to(chld_cr_map)
"""

# List comprehension to make out list of lists
chld_heat_data = [[row['Latitude'],row['Longitude']] for index, row in df_el.iterrows()]

# Plot it on the map
HeatMap(chld_heat_data, name='Early Learning Centers').add_to(chld_cr_map)

bins_2 = list(df_ymbirth['Teen Births 2009'].quantile([0,0.15,0.25,0.5,0.75,0.85,1]))


chld_cr_map.choropleth(
 geo_data=zip_shapefile,
 name='Young Mother Locations',
 data=cd.df_ymbirth,
 columns=['ZIP','Teen Births 2009'],
 key_on='feature.properties.zip',
 fill_color='YlGnBu',
 fill_opacity=0.35,
 line_opacity=0.75,
 bins=bins_2,
 legend_name='Concentration of Young Mothers'
)
folium.LayerControl().add_to(chld_cr_map)


chld_cr_map.save(outfile='chld_cr_prototype.html')
