import base64
import datetime
import io
import pdfkit
import math
import urllib.request
import os.path as path
import json

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px


def init_dashboard(server):
    external_stylesheets = [dbc.themes.COSMO]

    app = dash.Dash(server=server, routes_pathname_prefix='/ia/', external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            # multiple=True
        ),
        html.Div(id='output-data-upload'),
    ])

    def parse_contents(contents):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            print(df)
            print(df.shape[0])
            numOfRows = df.shape[0]
            # saving pp image first
            two_up_dir = path.abspath(path.join(__file__, "../.."))
            print(two_up_dir)
            for z in range(numOfRows):
                img_filename = two_up_dir + r'\assets' + "\\" + df['name'].iloc[z] + ".png"
                urllib.request.urlretrieve(df['img'].iloc[z], img_filename)
            # layout variable
            tobeReturned = [dbc.Row([
                dbc.Col(html.H2("Influencer Analytics"),
                        style={'text-align': 'center', 'margin': 30})
            ])]
            numOfDbcRows = math.ceil(numOfRows / 3)
            print(numOfDbcRows)
            try:
                for x in range(numOfDbcRows):
                    print('check num of rows left')
                    print(df.shape)
                    if df.shape[0] >= 3:
                        print('still got 3 or more than 3')
                        counter = 0
                        listInDbcRow = []
                        while counter < 3:
                            imgName = df['name'].iloc[0] + '.png'
                            print(imgName)
                            dbcCol = dbc.Col(
                                [dbc.Row(
                                    html.H5(df['name'].iloc[0], style={'font-weight': 'bold', 'padding-top': '10px'}),
                                    style={'textAlign': 'center', }),
                                 dbc.Row(html.Img(
                                     src=app.get_asset_url(imgName), width="300px", height="350px",
                                     style={"border-radius": "50%", 'padding': '35px', 'padding-top': '20px'})),
                                 dbc.Row(
                                     [dbc.Col(html.H5("Posts")), dbc.Col(html.H5("Followers")),
                                      dbc.Col(html.H5('Following'))], style={'textAlign': 'center', }),
                                 dbc.Row(
                                     [dbc.Col(html.H5(df['posts'].iloc[0])), dbc.Col(html.H5(df['followers'].iloc[0])),
                                      dbc.Col(html.H5(df['following'].iloc[0]))], style={'textAlign': 'center', })],
                                style={'padding': '5px', 'background-color': '#daebf7',
                                       'background-clip': 'content-box'})
                            df.drop(df.index[:1], inplace=True)
                            listInDbcRow.append(dbcCol)
                            counter += 1
                        dbcRow = dbc.Row(listInDbcRow, style={'margin-top': '10px', 'margin-bottom': '10px'})
                        tobeReturned.append(dbcRow)
                    else:
                        print('less than 3')
                        counter = 0
                        listInDbcRow = []
                        while counter <= df.shape[0]:
                            imgName = df['name'].iloc[0] + '.png'
                            print(imgName)
                            dbcCol = dbc.Col(
                                [dbc.Row(
                                    html.H5(df['name'].iloc[0], style={'font-weight': 'bold', 'padding-top': '10px'}),
                                    style={'textAlign': 'center', }),
                                    dbc.Row(html.Img(
                                        src=app.get_asset_url(imgName), width="300px", height="350px",
                                        style={"border-radius": "50%", 'padding': '35px', 'padding-top': '20px'})),
                                    dbc.Row(
                                        [dbc.Col(html.H5("Posts")), dbc.Col(html.H5("Followers")),
                                         dbc.Col(html.H5('Following'))], style={'textAlign': 'center', }),
                                    dbc.Row(
                                        [dbc.Col(html.H5(df['posts'].iloc[0])),
                                         dbc.Col(html.H5(df['followers'].iloc[0])),
                                         dbc.Col(html.H5(df['following'].iloc[0]))], style={'textAlign': 'center', })],
                                style={'padding': '5px', 'background-color': '#daebf7',
                                       'background-clip': 'content-box'})
                            df.drop(df.index[:1], inplace=True)
                            listInDbcRow.append(dbcCol)
                            counter += 1
                        diff = 3 - len(listInDbcRow)
                        for y in range(diff):
                            listInDbcRow.append(dbc.Col())
                        dbcRow = dbc.Row(listInDbcRow, style={'margin-top': '10px', 'margin-bottom': '10px'})
                        tobeReturned.append(dbcRow)
            except BaseException as e:
                print('layout error')
                print(e)
                return html.Div([
                    dbc.Container(tobeReturned)])
        except Exception as e:
            print('ia prob')
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        return html.Div([
            dbc.Container(tobeReturned)])

    @app.callback(Output('output-data-upload', 'children'),
                  Input('upload-data', 'contents'))
    def update_output(contents):
        if contents is not None:
            children = parse_contents(contents)
            return children

    return app.server
