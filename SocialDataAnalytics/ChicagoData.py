#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:00:53 2019

@author: rwtatko@us.ibm.com
"""
# Import Dash Visualization Libraries
import pandas as pd
import numpy as np

# Load Primary Dataframe

path = '/Users/rwtatko@us.ibm.com/SocialDataAnalytics/WelfareData/Service_Providers.csv'

df_main = pd.read_csv(filepath_or_buffer=path, error_bad_lines=False)

#Clean Dataframe & Impute Missing Values

df_main = df_main[df_main.Latitude.notnull()]
 
df_main = df_main[['Agency','Site Name','Division', 'Provider', 'Age Served', 'Gender', 'Yrs in Practice', 
                   'Expertise 1', 'Transportation Assistance', 'Address', 'Phone Number','Latitude','Longitude']]

age_list = ['10 and Under', '11 to 15 Years', '16 and Over']
df_main['Age Served'] = df_main['Age Served'].fillna(pd.Series(np.random.choice(age_list, size=len(df_main.index))))

df_main['Transportation Assistance'] = df_main['Transportation Assistance'].fillna('Yes')

yrs_prac_list = [3, 2, 4, 5, 6, 7, 10, 12, 11, 15, 17, 19, 20, 22, 25, 28, 34]
df_main['Yrs in Practice'] = df_main['Yrs in Practice'].fillna(pd.Series(np.random.choice(yrs_prac_list, size=len(df_main.index)+1)))

gender_list = ['Male', 'Female']
df_main['Gender'] = df_main['Gender'].fillna(pd.Series(np.random.choice(gender_list, size=len(df_main.index)+1)))

df_main.drop(columns=['Provider'])
name_list = [ 
'Dan Merkle',
'Katelynn Hunt',
'Grant Peterson',
'Sarah Cook',
'Michael Turnbull',
'Marianne Scott',
'Henry Booth',
'Edward Hart',
'Letty Mark',
'Lorraine Kingsley',
'Abilene Witherspoon',
'Tory Blakesley',
'Christen Sampson',
'Clifton Farmer',
'Sherman Brooks',
'Chantal Day',
'Cindy Danell',
'Elton Stanton',
'Brannon Thomas',
'Karl Sutton',
'Kerry Anderson',
'Phyliss Kirk',
'Beverly Elwes',
'Virgee Hatheway',
'Leigh Paternoster',
'Anastacia Bullard',
'Justina Haden',
'Carmina Dittrich',
'Terry Ates',
'Jeanie Marmolejo',
'Azalee Pharris',
'Darcy Stuart',
'Bret Hibbert',
'Joellen Bach',
'Steffanie Schlager',
'Hwa Gutierrez',
'Alesia Deckman',
'Lawanna Peavler',
'Lavina Lape',
'Cornelia Bedoya',
'Junita Penix',
'Toshia Helzer',
'Joe Capshaw',
'Malka Steed',
'Cherri Kreider',
'Minna Canizales',
'Rolando Mckea',
'Oliver Rey',
'Macy Farrelly',
'Tess Demarco',
'Terra Delawder',
'Elmira Austin',
'Janell Nunemaker',
'Donnette Harbuck',
'Rosamaria Lenhart',
'Phung Wayland',
'Lilly Noonkester',
'Marni Donlan',
'Barbra Gold',
'Numbers Yamauchi',
'Becki Rahim',
'Vernetta Christina',
'Georgianna Renf',
'Mary Terlizzi',
'Emil Patrick',
'Jake Vandeusen',
'Obdulia Hermansen',
'Darryl Blough',
'Haley Holley',
'Doyle Swayne',
'Coralee Arthurs',
'Rosa Ensminge',
'Misha Nader',
'Lissette Pryor'
]
df_main['Provider'] = name_list

#Create Match Score Variable for Providers

score_list = [0,0,0,0,0,0,0,0,5,5,5,10,10,10,10,10,15,15,15,15,15,15,45,45,65,65,95]
df_main['Match Score'] = pd.Series(np.random.choice(score_list, size=len(df_main.index)+1))

#Create Language list for Providers
lang_list = ['English','English','English','English','English','Spanish','Spanish','Spanish','Spanish','Mandarin','Polish']
df_main['Language'] = pd.Series(np.random.choice(lang_list, size=len(df_main.index)+1))


df_main['Popout'] = df_main['Provider'] + str(' : ') + df_main['Agency']

#Create Function that Returns Provider Initial + Last Name 
#***NOT NEEDED FOR MAP***

def name(s): 
    l = s.split() 
    new = "" 
    for i in range(len(l)-1): 
        s = l[i] 
        new += (s[0].upper()+'.') 
    new += l[-1].title() 
    return new  

init = []
for i in name_list:
    init.append(name(i))
    
df_main['Initials'] = init

#Load Bus Data
bus_path = '/Users/rwtatko@us.ibm.com/SocialDataAnalytics/WelfareData/Bus_Stations.csv'
df_bus = pd.read_csv(filepath_or_buffer=bus_path, error_bad_lines=False)

#Clean Bus Data
df_bus = df_bus[df_bus.Latitude.notnull()]
df_bus = df_bus[df_bus.Longitude.notnull()]
df_bus = df_bus[:500] #Only sample of 500 needed for map

#Load Railway Data
rail_path = '/Users/rwtatko@us.ibm.com/SocialDataAnalytics/WelfareData/CTA_RailStations.csv' 
df_rail = pd.read_csv(filepath_or_buffer=rail_path, error_bad_lines=False)

#Clean Railway Data
df_rail = df_rail[df_rail.X.notnull()]
df_rail = df_rail[df_rail.Y.notnull()]
