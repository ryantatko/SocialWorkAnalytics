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
        
provider_tbl = html.Div([dash_table.DataTable(
        id='datatable-interactivity',
      columns=[
            {"name" : 'Agency', "id": 'Agency', "deletable": False},
            {"name" : 'Division', "id": 'Division', "deletable": False},
            {"name" : 'Age Served', "id": 'Age Served', "deletable": False},
            {"name" : 'Point of Contact', "id": 'Provider', "deletable": False},
            {"name" : 'Gender', "id": 'Gender', "deletable": False},
            {"name" : 'Primary Language', "id": 'Language', "deletable": False},
            {"name" : 'Phone Number', "id": 'Phone Number', "deletable": False}
        ],
        data=df_main.to_dict('records'),
        editable=True,
        filtering=True,
        sorting=False,
        row_selectable="multi",
        row_deletable=False,
        selected_rows=[],
        style_table={'overflowX': 'scroll', 'max-width': '650px'},
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
                },
        pagination_mode="fe",
        pagination_settings={
            "current_page": 0,
            "page_size": 5,
        },
        css=[
        { 'selector': '.previous-page, .next-page', 'rule': 'background-color: white;' }
        ],
    ),
    html.Div(id='datatable-interactivity-container')
    ])

#~~~~~~~~~~~~~~~~~~~~~~~~~CREATE APP LAYOUT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        

app = dash.Dash(__name__, external_style_sheets=style_sheet)

app.layout = html.Div([

    html.Div([navbar]),
        
    html.Div(
    [dbc.Button("Case Worker Dashboard", color="secondary", className="mr-1")]
    ),
      
    html.Div([provider_tbl], style={'width': '50%','display': 'inline-block', 
             'padding':'5px', 'vertical-align': 'middle'}),

    html.Div([
    html.Iframe(id='map', srcDoc= open('prototype.html', 'r').read(), width=700, height=600)
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle', 
            'border':'4px #384654 solid'})
      
])
    

#~~~~~~~~~~~~~DEFINE APPLICATION CALLBACK FOR TABLES~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
"""

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")]
    )
    
def update_graphs(rows, derived_virtual_selected_rows):
    
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df_main if rows is None else pd.DataFrame(rows)

    colors = ['#D9AE00' if i in derived_virtual_selected_rows else '#005fb2'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            style={'font_family': 'verdana'},
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["Initials"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 190,
                    "width": 650,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ["Yrs in Practice", "Match Score"] if column in dff
    ]
if __name__ == '__main__':
    app.run_server(debug=True)
