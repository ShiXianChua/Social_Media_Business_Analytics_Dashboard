import base64
import datetime
import io
import pdfkit
from app.sa.commentProcessing import CommentProcessing
from app.sa.sentimentAnalysisP1 import SentimentAnalysisP1
from app.sa.sentimentAnalysisP2 import SentimentAnalysisP2

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

    app = dash.Dash(server=server, routes_pathname_prefix='/sa_fb/', external_stylesheets=external_stylesheets)

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
            df = pd.read_csv(io.BytesIO(decoded), header=None)
            commentList = df[0].tolist()
            fbName = commentList[0]
            commentList.pop(0)
            numOfPosts = commentList[0]
            commentList.pop(0)
            numOfComments = len(commentList)
            commentProcessing = CommentProcessing()
            positiveWords, negativeWords, positiveEmojis, negativeEmojis = commentProcessing.process_comment(
                commentList)
            sentimentAnalysisP1 = SentimentAnalysisP1()
            ss, ssc, ssd, commentFig, positive, neutral, negative = sentimentAnalysisP1.conduct_saP1(commentList)
            sentimentAnalysisP2 = SentimentAnalysisP2()
            wordsFig, emojisFig, WordFig, EmojiFig = sentimentAnalysisP2.conduct_saP2(positiveWords, negativeWords,
                                                                                      positiveEmojis, negativeEmojis)
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H2("Sentiment Analysis"),
                            style={'text-align': 'center', 'margin': 30})
                ]),
                dbc.Row([
                    dbc.Col(
                        [html.Img(src="https://1000logos.net/wp-content/uploads/2021/04/Facebook-logo.png",
                                  width="50px", height="30px", style={"float": "left", "margin-right": 2}),
                         html.H5("Facebook Page: " + fbName, style={'font-style': 'italic'})]),
                ]),
                dbc.Row([
                    dbc.Col(html.H1(ss, style={"font-weight": "bold", 'font-size': '50px'}),
                            style={'text-align': 'center', 'color': ssc}),
                ]),
                dbc.Row([
                    dbc.Col(html.H4('Sentiment Score', style={'font-weight': 'bold'}), style={'text-align': 'center'}, )
                ]),
                dbc.Row([
                    dbc.Col(html.H5(ssd, style={'font-style': 'italic'}), style={'text-align': 'center'}, ),
                ]),
                # dbc.Row([
                #     dbc.Col(html.H5("Total Number of Posts: " + numOfPosts), style={'text-align': 'left'}, )
                # ]),
                # dbc.Row([
                #     dbc.Col(html.H5("Total Number of Comments: " + numOfComments), style={'text-align': 'left'}, )
                # ]),
                dbc.Row([
                    dbc.Col([html.H5("All Posts", style={'font-weight': 'bold'}),
                             html.H5(numOfPosts)],
                            style={'text-align': 'center'}, ),
                    dbc.Col([html.H5("All Comments", style={'font-weight': 'bold'}),
                             html.H5(numOfComments)],
                            style={'text-align': 'center'}, ),
                    dbc.Col([html.H5("Positive Comments", style={'font-weight': 'bold'}),
                             html.H5(positive)],
                            style={'text-align': 'center'}, ),
                    dbc.Col([html.H5("Neutral Comments", style={'font-weight': 'bold'}),
                             html.H5(neutral)],
                            style={'text-align': 'center'}, ),
                    dbc.Col([html.H5("Negative Comments", style={'font-weight': 'bold'}),
                             html.H5(negative)],
                            style={'text-align': 'center'}, ),
                ], style={'margin-top': '25px'}),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='graph1',
                            figure=commentFig
                        ),
                        width={"size": 8, "offset": 2},
                    )
                ]),
                dbc.Row(
                    [
                        dbc.Col([
                            dcc.Graph(
                                id='graph2',
                                figure=wordsFig
                            ),
                        ]),
                        dbc.Col([
                            dcc.Graph(
                                id='graph3',
                                figure=emojisFig
                            ),
                        ]),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([
                            dcc.Graph(
                                id='graph4',
                                figure=WordFig
                            ),
                        ]),
                        dbc.Col([
                            dcc.Graph(
                                id='graph5',
                                figure=EmojiFig
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
