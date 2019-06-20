#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 19:08:36 2019

@author: rwtatko@us.ibm.com
"""

import ChicagoData
import dash
from ChicagoData import *
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

#~~~~~~~~~~~~~~~~~~~~~~~~~CREATE DASHBOARD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

IBM_LOGO = "http://www.freelogovectors.net/wp-content/uploads/2018/12/ibm-watson-logo.png"

style_sheet = '/Users/rwtatko@us.ibm.com/SocialDataAnalytics/assets/bootstrap.css'

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Enter Address")),
        dbc.Col(
            dbc.Button("Search", color="secondary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.Col(html.Img(src=IBM_LOGO, height="50px")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Case Worker Dashboard"),
                dbc.DropdownMenuItem("Executive Dashboard"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Data Sources")],
        ), 
    dbc.NavItem(dbc.NavLink("Logout", href="#")),
    dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    brand="CHILD WELFARE ANALYTICS PLATFORM",
    className='navbar navbar-expand-lg navbar-dark bg-dark',
    brand_href="#",
    sticky="top",
) 
        
exec_tbl = html.Div([dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in df_exec_smmry.columns],
        data=df_exec_smmry.to_dict('records'),
        editable=False,
        filtering=False,
        sorting=False,
        row_selectable="multi",
        row_deletable=False,
        #n_fixed_rows=1,
        #style_table={'overflowX': 'scroll','overflowY': 'scroll'},
        style_table={'height': 500, 'overflowY': 'scroll'},
        style_cell={'textAlign': 'left'},
        style_cell_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ] + [
            {
                'textAlign': 'left',
                'font_family': 'verdana',
                'size':'10px'
            }
            ],
        style_header={
                'backgroundColor': 'rgb(56,70,84)',
                'color': 'white',
                #'fontWeight': 'bold',
                'textAlign': 'center'
                }
        )
    ])
        

#~~~~~~~~~~~~~~~~~~~~~~~~~CREATE APP LAYOUT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

app = dash.Dash(__name__, external_style_sheets=style_sheet)

app.layout = html.Div([

    html.Div([navbar]),
        
    html.Div([
            dbc.Button("Executive Dashboard", color="secondary", className="mr-1")
            ]),
    
    html.Div([
            html.Iframe(id='fd_map', srcDoc= open('fd_dsrt_prototype.html', 'r').read(), width=675, height=350)
            ], 
                style={'width': '650', 'display': 'inline-block', 'vertical-align': 'middle',
                       'border':'4px #384654 solid'}
            ),
            
    html.Div([
            html.Iframe(id='chld_map', srcDoc= open('chld_cr_prototype.html', 'r').read(), width=675, height=350)
            ], 
                style={'width': '650', 'display': 'inline-block', 'vertical-align': 'middle',
                       'border':'4px #384654 solid'}
            ),
    
    html.Br(),
    
    html.Div([
            dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Food Deserts"), dbc.DropdownMenuItem("Early Learning Areas"),
             dbc.DropdownMenuItem("Job Program Growth"),dbc.DropdownMenuItem("Mental Health Needs")],
            label="View Analyses")
            ]),
    
    html.Div([exec_tbl], style={'display': 'inline-block', 
             'padding':'15px'}),
            ])
    

#~~~~~~~~~~~~~DEFINE APPLICATION CALLBACK FOR TABLES~~~~~~~~~~~~~~~~~~~~~~~~~~#


if __name__ == '__main__':
    app.run_server(debug=True)
