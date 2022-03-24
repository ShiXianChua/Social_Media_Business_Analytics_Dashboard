import base64
import datetime
import io
import pdfkit

import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

pd.options.mode.chained_assignment = None  # default='warn'


def init_dashboard(server):
    # DASH FRAMEWORK STARTS HERE
    external_stylesheets = [dbc.themes.COSMO]
    app = dash.Dash(server=server, routes_pathname_prefix='/psmaa/', external_stylesheets=external_stylesheets)

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
            df = pd.read_excel(io.BytesIO(decoded))
            # # READ EXCEL DATA IN
            # df = pd.read_excel('MindSight-Campaigns-Lifetime.xlsx')
            # print('hello')

            # Data Cleaning
            df.sort_values(['Campaign name'], ascending=[True], inplace=True, ignore_index=True)
            # Fill in missing values (just in case)
            df['Campaign name'] = df['Campaign name'].fillna('Unknown Campaign Name')
            df.rename(columns={'Cost per results': 'Cost per result (MYR)'}, inplace=True)
            df['Cost per result (MYR)'] = df['Cost per result (MYR)'].apply(lambda x: round(x, 2))
            df['Frequency'] = df['Frequency'].apply(lambda x: round(x, 2))
            df['Unique CTR (Link Click-Through Rate, %)'] = (df['Unique link clicks'] / df['Reach']) * 100
            df['Unique CTR (Link Click-Through Rate, %)'] = df['Unique CTR (Link Click-Through Rate, %)'].apply(
                lambda x: round(x, 2))

            startDate = str(df.iloc[0]['Reporting starts'].date())
            endDate = str(df.iloc[0]['Reporting ends'].date())

            # Reach and Impressions (Barchart)
            RIfig = px.bar(df, x="Campaign name", y=["Reach", "Impressions"], title='<b>Reach & Impressions</b>',
                           barmode='group',
                           template='plotly_white')
            texts = [df['Reach'], df['Impressions']]
            for i, t in enumerate(texts):
                RIfig.data[i].text = t
                RIfig.data[i].textposition = 'outside'
            RIfig.update_layout(
                width=900,
                height=700,
                xaxis_title="Campaign Name",
                yaxis_title="Number",
                title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
            )

            # CTR (Barchart)
            CTRfig = px.bar(df, x="Campaign name", y="Unique CTR (Link Click-Through Rate, %)",
                            title='<b>Unique CTR (Link Click-Through Rate, %)</b>', template='plotly_white',
                            text="Unique CTR (Link Click-Through Rate, %)", color='Result indicator')
            CTRfig.update_layout(
                height=600,
                xaxis_title="Campaign Name",
                yaxis_title="Unique CTR (%)",
                title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                xaxis={'categoryorder': 'total descending'}
            )

            # Cost per result (Barchart)
            CPAfig = px.bar(df, x="Campaign name", y="Cost per result (MYR)", title='<b>Cost per result (MYR)</b>',
                            template='plotly_white', text="Cost per result (MYR)", color='Result indicator')
            CPAfig.update_layout(
                height=600,
                xaxis_title="Campaign Name",
                yaxis_title="MYR",
                title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                xaxis={'categoryorder': 'total descending'}
            )

            # Amount Spent (Barchart)
            ASfig = px.bar(df, x="Campaign name", y="Amount spent (MYR)", title='<b>Amount spent (MYR)</b>',
                           template='plotly_white',
                           text="Amount spent (MYR)", color='Result indicator')
            ASfig.update_layout(
                height=600,
                xaxis_title="Campaign Name",
                yaxis_title="MYR",
                title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                xaxis={'categoryorder': 'total descending'}
            )

            # Frequency (Barchart)
            Ffig = px.bar(df, x="Campaign name", y="Frequency", title='<b>Frequency</b>', template='plotly_white',
                          text="Frequency")
            Ffig.update_layout(
                height=600,
                xaxis_title="Campaign Name",
                yaxis_title="Frequency",
                title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                xaxis={'categoryorder': 'total descending'}
            )

        except Exception as e:
            print('ada error')
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H2("Paid Social Media Ads Analytics"),
                            style={'text-align': 'center', 'margin': 30, 'margin-bottom': 50})
                ]),
                dbc.Row([
                    dbc.Col(html.H5("Ads Campaigns (" + startDate + "  -  " + endDate + ")"),
                            width={"size": 8, "offset": 2}, )
                ]),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='graph1',
                            figure=RIfig
                        ),
                        width={"size": 8, "offset": 2},
                    )
                ]),
                dbc.Row(
                    [
                        dbc.Col([
                            dcc.Graph(
                                id='graph2',
                                figure=CTRfig
                            ),
                        ]),
                        dbc.Col([
                            dcc.Graph(
                                id='graph3',
                                figure=CPAfig
                            ),
                        ]),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([
                            dcc.Graph(
                                id='graph4',
                                figure=ASfig
                            ),
                        ]),
                        dbc.Col([
                            dcc.Graph(
                                id='graph5',
                                figure=Ffig
                            ),
                        ]),
                    ]
                ),
            ])])

    @app.callback(Output('output-data-upload', 'children'),
                  Input('upload-data', 'contents'))
    def update_output(contents):
        if contents is not None:
            children = parse_contents(contents)
            return children

    return app.server
