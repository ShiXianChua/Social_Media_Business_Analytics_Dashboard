from dash import html
import dash_bootstrap_components as dbc
import dash
from .layout import html_layout


def init_dashboard(server):
    external_stylesheets = [dbc.themes.COSMO]

    app = dash.Dash(server=server, routes_pathname_prefix='/intro/', external_stylesheets=external_stylesheets)

    # app.index_string = html_layout

    app.layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Welcome to Social Media Business Analytics Dashboard!", style={'font-weight': 'bold'}
                                ), style={'text-align': 'center', 'margin': '30px'})
            ]),
            dbc.Row([
                dbc.Col(html.H2("Our Key Analytics Programmes")
                        , style={'text-align': 'left', }),
            ]),
            dbc.Row([
                dbc.Col([html.H2("Audience Analytics"), html.H5(
                    "Designed to help your business identify its target audience. It is important because it helps the business build an effective and audience-first social media marketing strategy.")]
                        , style={'text-align': 'right', 'margin': 'auto'}),
                dbc.Col(html.Img(
                    src="https://digitalromans.com/wp-content/uploads/2020/09/target-audience-concept-vector-illustration_107173-16701.jpg",
                    width="570px", height="350px"),
                    style={'text-align': 'center'}),
            ], style={'margin': '5px'}),
            dbc.Row([
                dbc.Col(
                    html.Img(src="https://firespring.com/wp-content/uploads/2021/03/understanding-target-audience.png",
                             width="570px", height="350px"),
                    style={'text-align': 'center'}),
                dbc.Col([html.H2("Paid Social Media Ads Analytics"), html.H5(
                    "Designed to help marketers evaluate the effectiveness of social media ads campaigns via consistent tracking of important KPIs such as clicks, click-through rate (CTR), cost per action (CPA), etc.")]
                        , style={'text-align': 'left', 'margin': 'auto'}),
            ], style={'margin': '5px'}),
            dbc.Row([
                dbc.Col([html.H2("Performance Analytics"), html.H5(
                    "Designed to give marketers an overview of interactions across platforms and over time in order to understand if the content you’re publishing is effectively engaging your audience and to understand the results of your organization’s social media strategy, and see what return you’re getting from your investment.")]
                        , style={'text-align': 'right', 'margin': 'auto'}),
                dbc.Col(html.Img(
                    src="https://talkinginfluence.com/wp-content/uploads/2019/12/Six-Ways-to-Improve-Your-Influencer-Marketing-Analytics-2000x1200.jpg",
                    width="570px", height="350px"),
                    style={'text-align': 'center'}),
            ], style={'margin': '5px'}),
            dbc.Row([
                dbc.Col(html.Img(
                    src="https://www.marketingguru.io/blog/wp-content/uploads/elementor/thumbs/image-4-oo5e3zi4re4yuxy0p36stidooczefnrhbotullvol2.png",
                    width="570px", height="350px"),
                    style={'text-align': 'center'}),
                dbc.Col([html.H2("Influencer Analytics"), html.H5(
                    "Measure, analyze and evaluate an influencer’s reach and performance.")]
                        , style={'text-align': 'left', 'margin': 'auto'}),
            ], style={'margin': '5px'}),
            dbc.Row([
                dbc.Col([html.H2("Sentiment Analysis"), html.H5(
                    "A process of retrieving information about a consumer’s perception of a product, service or brand. It is important as it enables the business to learn more about what its audience really wants, and make changes to its brand messaging and product development accordingly.")]
                        , style={'text-align': 'right', 'margin': 'auto'}),
                dbc.Col(html.Img(
                    src="https://d1sjtleuqoc1be.cloudfront.net/wp-content/uploads/2019/04/25112909/shutterstock_1073953772.jpg",
                    width="570px", height="350px"),
                    style={'text-align': 'center'}),
            ], style={'margin': '5px'}),
        ])
    ])

    return app.server

