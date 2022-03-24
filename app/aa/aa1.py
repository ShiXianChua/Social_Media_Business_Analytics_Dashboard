# CONVERT FROM XLS TO XLSX
import win32com.client as win32
import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import os

pd.options.mode.chained_assignment = None  # default='warn'


def init_dashboard(server):
    # DASH FRAMEWORK STARTS HERE
    external_stylesheets = [dbc.themes.COSMO]
    app = dash.Dash(server=server, routes_pathname_prefix='/aa1/', external_stylesheets=external_stylesheets)

    # fname = r"C:\Users\ChuaShiXian\Desktop\Bachelor of Computer Science (Information Systems)\2020-21\Semester 2 2020-21\Academic Project\Development\dash-flask\Audience (Celebliss).xls"
    # excel = win32.Dispatch('Excel.Application')
    # wb = excel.Workbooks.Open(fname)
    #
    # wb.SaveAs(fname + "x", FileFormat=51)  # FileFormat = 51 is for .xlsx extension
    # wb.Close()  # FileFormat = 56 is for .xls extension
    # excel.Application.Quit()

    # READ EXCEL DATA IN
    filepath = 'https://firebasestorage.googleapis.com/v0/b/fyprealtimedb.appspot.com/o/qV7CknzUmhP9Mb76rR9FU3EIPb83%2FAA%2FAudience_Celebliss.xlsx?alt=media'
    df = pd.read_excel(filepath, header=None)
    df.columns = ['Property', 'V1', 'V2']

    # FB Age & Gender
    FbAGi1 = df[df['Property'] == 'Age'].index[0] + 1
    FbAGi2 = df[df['Property'] == 'Instagram Followers by Gender and Age'].index.item() - 1
    FbAGdf = df[FbAGi1:FbAGi2]
    FbAGdf.reset_index(drop=True, inplace=True)
    FbAGdf.columns = ['Age', 'Women', 'Men']
    FbAGdf['Women'] = FbAGdf['Women'].astype(str).astype(float) * 100
    FbAGdf['Men'] = FbAGdf['Men'].astype(str).astype(float) * 100

    # Facebook Page Likes by Gender (Piechart)
    women = FbAGdf['Women'].sum()
    men = FbAGdf['Men'].sum()
    unknown = 100.0 - women - men
    labels = ['Women', 'Men', 'Unknown']
    values = [women, men, unknown]
    FbAGfig1 = px.pie(values=values, names=labels,
                      title='Facebook Page Likes by Gender')
    FbAGfig1.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    # Facebook Page Likes by Gender and Age (Barchart)
    FbAGfig2 = px.bar(FbAGdf, x="Age", y=["Women", "Men"], title='Facebook Page Likes by Gender and Age',
                      barmode='group')
    FbAGfig2.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Percentage (%)",
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    # Ig Age & Gender
    IgAGi1 = df[df['Property'] == 'Age'].index[1] + 1
    IgAGi2 = df[df['Property'] == 'Facebook Page Likes by Top Cities'].index.item() - 1
    IgAGdf = df[IgAGi1:IgAGi2]
    IgAGdf.reset_index(drop=True, inplace=True)
    IgAGdf.columns = ['Age', 'Women', 'Men']
    IgAGdf['Women'] = IgAGdf['Women'].astype(str).astype(float) * 100
    IgAGdf['Men'] = IgAGdf['Men'].astype(str).astype(float) * 100

    # Instagram Followers by Gender (Piechart)
    women = IgAGdf['Women'].sum()
    men = IgAGdf['Men'].sum()
    unknown = 100.0 - women - men
    labels = ['Women', 'Men', 'Unknown']
    values = [women, men, unknown]
    IgAGfig1 = px.pie(values=values, names=labels,
                      title='Instagram Followers by Gender')
    IgAGfig1.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    # Instagram Followers by Gender and Age (Barchart)
    IgAGfig2 = px.bar(IgAGdf, x="Age", y=["Women", "Men"], title='Instagram Followers by Gender and Age',
                      barmode='group')
    IgAGfig2.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Percentage (%)",
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    # Fb Top Cities
    FbCityi1 = df[df['Property'] == 'Top Cities'].index[0] + 1
    FbCityi2 = df[df['Property'] == 'Instagram Followers by Top Cities'].index.item() - 1
    FbCitydf = df[FbCityi1:FbCityi2]
    FbCitydf.reset_index(drop=True, inplace=True)
    FbCitydf.drop(columns=['V2'], inplace=True)
    FbCitydf.columns = ['Top Cities', 'Percentage']
    FbCitydf['Percentage'] = FbCitydf['Percentage'].astype(str).astype(float) * 100

    # Facebook Page Likes by Top Cities (Barchart)
    FbCityfig = px.bar(FbCitydf, x="Percentage", y='Top Cities', title='Facebook Page Likes by Top Cities')
    FbCityfig.update_layout(
        xaxis_title="Percentage (%)",
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    # Ig Top Cities
    IgCityi1 = df[df['Property'] == 'Top Cities'].index[1] + 1
    IgCityi2 = df[df['Property'] == 'Facebook Page Likes by Top Countries'].index.item() - 1
    IgCitydf = df[IgCityi1:IgCityi2]
    IgCitydf.reset_index(drop=True, inplace=True)
    IgCitydf.drop(columns=['V2'], inplace=True)
    IgCitydf.columns = ['Top Cities', 'Percentage']
    IgCitydf['Percentage'] = IgCitydf['Percentage'].astype(str).astype(float) * 100

    # Instagram Followers by Top Cities (Barchart)
    IgCityfig = px.bar(IgCitydf, x="Percentage", y='Top Cities', title='Instagram Followers by Top Cities')
    IgCityfig.update_layout(
        xaxis_title="Percentage (%)",
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    # Fb Top Countries
    FbCountryi1 = df[df['Property'] == 'Top Countries'].index[0] + 1
    FbCountryi2 = df[df['Property'] == 'Instagram Followers by Top Countries'].index.item() - 1
    FbCountrydf = df[FbCountryi1:FbCountryi2]
    FbCountrydf.reset_index(drop=True, inplace=True)
    FbCountrydf.drop(columns=['V2'], inplace=True)
    FbCountrydf.columns = ['Top Countries', 'Percentage']
    FbCountrydf['Percentage'] = FbCountrydf['Percentage'].astype(str).astype(float) * 100

    # Facebook Page Likes by Top Countries (Barchart)
    FbCountryfig = px.bar(FbCountrydf, x="Percentage", y='Top Countries', title='Facebook Page Likes by Top Countries')
    FbCountryfig.update_layout(
        xaxis_title="Percentage (%)",
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    # Ig Top Countries
    IgCountryi1 = df[df['Property'] == 'Top Countries'].index[1] + 1
    IgCountryi2 = df.tail(1).index.item()
    IgCountrydf = df[IgCountryi1:IgCountryi2 + 1]
    IgCountrydf.reset_index(drop=True, inplace=True)
    IgCountrydf.drop(columns=['V2'], inplace=True)
    IgCountrydf.columns = ['Top Countries', 'Percentage']
    IgCountrydf['Percentage'] = IgCountrydf['Percentage'].astype(str).astype(float) * 100

    # Instagram Followers by Top Countries (Barchart)
    IgCountryfig = px.bar(IgCountrydf, x="Percentage", y='Top Countries', title='Instagram Followers by Top Countries')
    IgCountryfig.update_layout(
        xaxis_title="Percentage (%)",
        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    # DATA PROCESSES
    # Fb Page Likes
    FbPL = df.loc[2]['Property']

    # Ig Followers
    IgFL = df.loc[6]['Property']

    def findFbDominantAG():
        if FbAGdf[FbAGdf['Women'] == FbAGdf['Women'].max()]['Age'].count() == 1:
            FbWAgeMax = FbAGdf[FbAGdf['Women'] == FbAGdf['Women'].max()]['Age'].iloc[0]
            FbWD = "Women: {}".format(FbWAgeMax)
        else:
            FbWCount = FbAGdf[FbAGdf['Women'] == FbAGdf['Women'].max()]['Age'].count()
            FbWD = "Women: "
            for x in range(FbWCount - 1):
                FbWD = FbWD + FbAGdf[FbAGdf['Women'] == FbAGdf['Women'].max()]['Age'].iloc[x] + ", "
            FbWD = FbWD + FbAGdf[FbAGdf['Women'] == FbAGdf['Women'].max()]['Age'].iloc[FbWCount - 1]

        if FbAGdf[FbAGdf['Men'] == FbAGdf['Men'].max()]['Age'].count() == 1:
            FbMAgeMax = FbAGdf[FbAGdf['Men'] == FbAGdf['Men'].max()]['Age'].iloc[0]
            FbMD = "Men: {}".format(FbMAgeMax)
        else:
            FbMCount = FbAGdf[FbAGdf['Men'] == FbAGdf['Men'].max()]['Age'].count()
            FbMD = "Men: "
            for x in range(FbMCount - 1):
                FbMD = FbMD + FbAGdf[FbAGdf['Men'] == FbAGdf['Men'].max()]['Age'].iloc[x] + ", "
            FbMD = FbMD + FbAGdf[FbAGdf['Men'] == FbAGdf['Men'].max()]['Age'].iloc[FbMCount - 1]
        return FbWD, FbMD

    if FbAGdf['Women'].sum() == FbAGdf['Men'].sum():
        FbGD = "Equally distributed among men and women"
        print(FbGD)
        FbWD, FbMD = findFbDominantAG()
        print(FbWD)
        print(FbMD)

    elif FbAGdf['Women'].sum() > FbAGdf['Men'].sum():
        FbGD = "Women > Men"
        print(FbGD)
        FbWD, FbMD = findFbDominantAG()
        print(FbWD)
        print(FbMD)

    else:
        FbGD = "Men > Women"
        print(FbGD)
        FbWD, FbMD = findFbDominantAG()
        print(FbWD)
        print(FbMD)

    def findIgDominantAG():
        if IgAGdf[IgAGdf['Women'] == IgAGdf['Women'].max()]['Age'].count() == 1:
            IgWAgeMax = IgAGdf[IgAGdf['Women'] == IgAGdf['Women'].max()]['Age'].iloc[0]
            IgWD = "Women: {}".format(IgWAgeMax)
        else:
            IgWCount = IgAGdf[IgAGdf['Women'] == IgAGdf['Women'].max()]['Age'].count()
            IgWD = "Women: "
            for x in range(IgWCount - 1):
                IgWD = IgWD + IgAGdf[IgAGdf['Women'] == IgAGdf['Women'].max()]['Age'].iloc[x] + ", "
            IgWD = IgWD + IgAGdf[IgAGdf['Women'] == IgAGdf['Women'].max()]['Age'].iloc[IgWCount - 1]

        if IgAGdf[IgAGdf['Men'] == IgAGdf['Men'].max()]['Age'].count() == 1:
            IgMAgeMax = IgAGdf[IgAGdf['Men'] == IgAGdf['Men'].max()]['Age'].iloc[0]
            IgMD = "Men: {}".format(IgMAgeMax)
        else:
            IgMCount = IgAGdf[IgAGdf['Men'] == IgAGdf['Men'].max()]['Age'].count()
            IgMD = "Men: "
            for x in range(IgMCount - 1):
                IgMD = IgMD + IgAGdf[IgAGdf['Men'] == IgAGdf['Men'].max()]['Age'].iloc[x] + ", "
            IgMD = IgMD + IgAGdf[IgAGdf['Men'] == IgAGdf['Men'].max()]['Age'].iloc[IgMCount - 1]
        return IgWD, IgMD

    if IgAGdf['Women'].sum() == IgAGdf['Men'].sum():
        IgGD = "Equally distributed among men and women"
        print(IgGD)
        IgWD, IgMD = findIgDominantAG()
        print(IgWD)
        print(IgMD)

    elif IgAGdf['Women'].sum() > IgAGdf['Men'].sum():
        IgGD = "Women > Men"
        print(IgGD)
        IgWD, IgMD = findIgDominantAG()
        print(IgWD)
        print(IgMD)

    else:
        IgGD = "Men > Women"
        print(IgGD)
        IgWD, IgMD = findIgDominantAG()
        print(IgWD)
        print(IgMD)

    app.layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("Audience Analytics"),
                        style={'text-align': 'center', 'margin': 30, 'margin-bottom': 0})
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src="https://1000logos.net/wp-content/uploads/2021/04/Facebook-logo.png", width="160px",
                             height="100px"),
                    style={'text-align': 'center', 'margin': '20px'}),
                dbc.Col(html.Img(src="https://workingwithdog.com/wp-content/uploads/2016/05/new_instagram_logo.jpg",
                                 width="90px", height="90px"),
                        style={'text-align': 'center', 'margin': '20px', 'margin-top': '25px',
                               'margin-bottom': '15px'}),
            ]),
            dbc.Row([
                dbc.Col(
                    [html.H4("Facebook Page Likes"), html.H1(FbPL), html.H5(html.I(FbGD)), html.H5(FbWD),
                     html.H5(FbMD)],
                    style={'text-align': 'center'}),
                dbc.Col(
                    [html.H4("Instagram Followers"), html.H1(IgFL), html.H5(html.I(IgGD)), html.H5(IgWD),
                     html.H5(IgMD)],
                    style={'text-align': 'center'}),
            ]),
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Graph(
                            id='graph1',
                            figure=FbAGfig1
                        ),
                    ]),
                    dbc.Col([
                        dcc.Graph(
                            id='graph2',
                            figure=IgAGfig1
                        ),
                    ]),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Graph(
                            id='graph3',
                            figure=FbAGfig2
                        ),
                    ]),
                    dbc.Col([
                        dcc.Graph(
                            id='graph4',
                            figure=IgAGfig2
                        ),
                    ]),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Graph(
                            id='graph5',
                            figure=FbCityfig
                        ),
                    ]),
                    dbc.Col([
                        dcc.Graph(
                            id='graph6',
                            figure=IgCityfig
                        ),
                    ]),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Graph(
                            id='graph7',
                            figure=FbCountryfig
                        ),
                    ]),
                    dbc.Col([
                        dcc.Graph(
                            id='graph8',
                            figure=IgCountryfig
                        ),
                    ]),
                ]
            ),

        ])

    ])
    return app.server
