import os, types
import pandas as pd
from botocore.client import Config
import ibm_boto3

from jupyter_dash import JupyterDash               
from dash import html, dcc
from dash.dependencies import Output, Input, State      
import dash_bootstrap_components as dbc  
import plotly.express as px

def __iter__(self): return 0
endpoint_access = 'https://s3.eu.cloud-object-storage.appdomain.cloud'

client_access = ibm_boto3.client(
    service_name='s3',
    ibm_api_key_id='Ok05yixj-YW-zXdte-irTwTCu6UGQhpROV8kPd6SYaIH',
    ibm_auth_endpoint="https://iam.cloud.ibm.com/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url=endpoint_access)
key = 'London_processed_data_for_Dashboard.csv'
body = client_access.get_object(Bucket='digitalinsightspublictransport-donotdelete-pr-zraerohsdy8fer',Key=key)['Body']

if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )

df_data_1 = pd.read_csv(body)

## Test function
def plot1(df):
    fig = px.line(df, x='date', y='average transit stations(5d)', title = 'Mobility Changes')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Covid Case')
    fig.update_layout(margin=dict(l=5, r=5, b=90))
    return fig

## Dash python
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], title='Digital Insights WSP') 
server = app.server
app.layout = dbc.Container([
    dbc.Card(html.H1("COVID-19 vs Mobility Change in Greater London"), 
             body=True, color="light", outline = False, className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1("70%", className="card-title text-md-center"),
                    html.P("Population Vaccinated (1st)", className="text-md-center")],
                    className='border-0 bg-danger text-white')
            ])
        ],width=2),
        dbc.Col([
            dbc.Card([
                
                    html.H1("65%", className="card-title text-md-center"),
                    html.P("Population Vaccinated (2nd)", className="text-md-center")],
                    className='mb-3 mt-3 ml-3 mr-3 bg-secondary text-white rounded-lg')
            
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1("62%", className="card-title text-md-center"),
                    html.P("Population Vaccinated (3rd)", className="text-md-center")],
                    className='mb-3 mt-3 ml-3 border-0 bg-info text-white')
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1("-53%", className="card-title text-md-center"),
                    html.P("Average mobility change on workplaces", className="text-md-center"),
                    html.P("(last 2 weeks)", className="text-md-center")],
                    className='mb-3 mt-3 ml-3 bg-warning text-white rounded-pill')
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1("-52%", className="card-title text-md-center"),
                    html.P("Average mobility change on transit station (last 2 weeks)", className="text-md-center")],
                    className='mb-3 mt-3 ml-3 border-0 bg-dark text-white rounded-pill')
            ])
        ], width=3),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='covid_per_10k',figure={},config={'displayModeBar':False}),
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='weather',figure={},config={'displayModeBar':False}),
                ])
            ])
        ]),
    ],className='mb-3 mt-3 ml-3'),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='vacc_rate',figure={},config={'displayModeBar':False}),
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='mob_change',figure={},config={'displayModeBar':False}),
                ])
            ])
        ]),
    ],className='mb-3 mt-3 ml-3'),
    
    dbc.Card(html.H1("Prediction of Mobility Change on Transit Station"), 
             body=True, color="light", outline = False, className='mb-2 mt-2'),
],fluid=True)

@app.callback(
    Output('covid_per_10k','figure'),
    [Input('covid_per_10k','figure')],)
def covid_per10k(figure):
    df = df_data_1[['date','average transit stations(5d)']]
    fig = plot1(df)
    return fig

if __name__ == '__main__':
    app.run_server()
