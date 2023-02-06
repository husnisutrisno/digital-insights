import types
import pandas as pd
from botocore.client import Config
import ibm_boto3

import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc  
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
pio.templates.default = "simple_white"

## Color palette
Lightblue = '#D8E6F0'
Red = '#F9423A'
Charcoal_dark = '#1E252B'
Charcoal_blue = "#343E48"
Light_gray = '#D9D9D6'
Light_gray_50 = '#EFECEA'

################################## Download data from IBM Cloud #######################################################
def __iter__(self): return 0
endpoint_access = 'https://s3.eu.cloud-object-storage.appdomain.cloud'

client_access = ibm_boto3.client(
    service_name='s3',
    ibm_api_key_id='Ok05yixj-YW-zXdte-irTwTCu6UGQhpROV8kPd6SYaIH',
    ibm_auth_endpoint="https://iam.cloud.ibm.com/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url=endpoint_access)

def download_data(file):
    body = client_access.get_object(Bucket='digitalinsightspublictransport-donotdelete-pr-zraerohsdy8fer',Key=file)['Body']
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    df = pd.read_csv(body)
    return df

# ## London data
# df_london = download_data('London_processed_data_for_Dashboard.csv')
# df_london_var = download_data('London_prediction_for_Dashboard.csv')
# df_london_mob = download_data('London_mobility_data_for_Dashboard.csv')

# ## Stockholm data
# df_stockholm = download_data('Stockholm_processed_data_for_Dashboard.csv')
# df_stockholm_var = download_data('Stockholm_prediction_for_Dashboard.csv')
# df_stockholm_mob = download_data('Stockholm_mobility_data_for_Dashboard.csv')

# ## Copenhagen data
# df_copenhagen = download_data('Copenhagen_processed_data_for_Dashboard.csv')
# df_copenhagen_var = download_data('Copenhagen_prediction_for_Dashboard.csv')
# df_copenhagen_mob = download_data('Copenhagen_mobility_data_for_Dashboard.csv')

# ## Tel Aviv data
# df_telaviv = download_data('Tel_Aviv_processed_data_for_Dashboard.csv')
# df_telaviv_var = download_data('Tel_Aviv_prediction_for_Dashboard.csv')
# df_telaviv_mob = download_data('Tel_Aviv_mobility_data_for_Dashboard.csv')

# ## Oslo data
# df_oslo = download_data('Oslo_processed_data_for_Dashboard.csv')
# df_oslo_var = download_data('Oslo_prediction_for_Dashboard.csv')
# df_oslo_mob = download_data('Oslo_mobility_data_for_Dashboard.csv')

# ## Helsinki data
# df_helsinki = download_data('Helsinki_processed_data_for_Dashboard.csv')
# df_helsinki_var = download_data('Helsinki_prediction_for_Dashboard.csv')
# df_helsinki_mob = download_data('Helsinki_mobility_data_for_Dashboard.csv')



def update_datasets():
    global df_london, df_london_var, df_london_mob, df_stockholm, df_stockholm_var, df_stockholm_mob, df_copenhagen, df_copenhagen_var, df_copenhagen_mob, df_telaviv, df_telaviv_var, df_telaviv_mob, df_oslo, df_oslo_var, df_oslo_mob, df_helsinki, df_helsinki_var, df_helsinki_mob
    ## London data
    df_london = download_data('London_processed_data_for_Dashboard.csv')
    df_london_var = download_data('London_prediction_for_Dashboard.csv')
    df_london_mob = download_data('London_mobility_data_for_Dashboard.csv')

    ## Stockholm data
    df_stockholm = download_data('Stockholm_processed_data_for_Dashboard.csv')
    df_stockholm_var = download_data('Stockholm_prediction_for_Dashboard.csv')
    df_stockholm_mob = download_data('Stockholm_mobility_data_for_Dashboard.csv')

    ## Copenhagen data
    df_copenhagen = download_data('Copenhagen_processed_data_for_Dashboard.csv')
    df_copenhagen_var = download_data('Copenhagen_prediction_for_Dashboard.csv')
    df_copenhagen_mob = download_data('Copenhagen_mobility_data_for_Dashboard.csv')

    ## Tel Aviv data
    df_telaviv = download_data('Tel_Aviv_processed_data_for_Dashboard.csv')
    df_telaviv_var = download_data('Tel_Aviv_prediction_for_Dashboard.csv')
    df_telaviv_mob = download_data('Tel_Aviv_mobility_data_for_Dashboard.csv')

    ## Oslo data
    df_oslo = download_data('Oslo_processed_data_for_Dashboard.csv')
    df_oslo_var = download_data('Oslo_prediction_for_Dashboard.csv')
    df_oslo_mob = download_data('Oslo_mobility_data_for_Dashboard.csv')

    ## Helsinki data
    df_helsinki = download_data('Helsinki_processed_data_for_Dashboard.csv')
    df_helsinki_var = download_data('Helsinki_prediction_for_Dashboard.csv')
    df_helsinki_mob = download_data('Helsinki_mobility_data_for_Dashboard.csv')

update_datasets()
## Historical weather data
df_weather = download_data('Historical_weather_data_for_dashboard.csv')

######################################## Plots function ################################################################
def plot1(df1, df2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['covid per10k'], name='Covid per 10K Population', fill='tozeroy',
                             line=dict(color='coral')), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=df2['date'], y=df2['average transit stations(5d)'], name='Mobility Change at Transit Stations',
                   line=dict(color='green')), secondary_y=True)
    
#     if int(round(df1['covid per10k'].max())>100:
#            range1 = int(round(df1['covid per10k'].max(), -1))
#     range2 = int(round(df2['average transit stations(5d)'].min(), -1))
    range1 = 100
    range2 = -80
    fig.update_yaxes(title='Covid Cases', range=[range1 * (-1), range1], secondary_y=False)
    fig.update_yaxes(title='Mobility Change (%)', range=[range2, range2 * (-1)], secondary_y=True)
    fig.update_layout(margin=dict(l=0, r=0, b=100, t=50),
                      legend=dict(orientation='h', yanchor="bottom", y=-0.35, xanchor="center", x=0.5))
    #fig.update_layout(title='<b>Mobility Change in Response to Covid Cases')
    return fig


def plot2(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['average transit stations(5d)'], name='Transit Stations',
                             line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['date'], y=df['average workplaces(5d)'], name='Workplaces', line=dict(color='orange'),
                             opacity=0.7))
    
    fig.add_hline(y=0, line_width=2, line_dash="dash", line_color="#F9423A", opacity=0.5,
                  annotation=dict(text="Baseline pre-pandemic", 
                                  font_size=15, font_family="Montserrat"),
                  annotation_position="top left")
    
    fig.add_annotation(text="*Excluding weekends", xref="paper", yref="paper", x=1, y=0, showarrow=False, font=dict(size=10))
    fig.update_yaxes(title='Mobility Change (%)', range=[-80, 40])
    fig.update_layout(
        margin=dict(l=0, r=50, b=100, t=50),
        legend=dict(orientation='h', yanchor="bottom", y=-0.35, xanchor="center", x=0.5))
    #fig.update_layout(title='<b>Mobility Comparison Between Transit Stations & Workplaces')
    return fig


def plot3(df1, df2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['percent of 1st dose'], name='vaccinated first dose (%)',
                             line=dict(color='mediumpurple'), opacity=0.7, fill='tozeroy'), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=df1['date'], y=df1['percent of 2nd dose'], name='vaccinated second dose (%)', line=dict(color='red'),
                   opacity=0.7, fill='tozeroy'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['percent of 3rd dose'], name='vaccinated third dose (%)',
                             line=dict(color='greenyellow'), opacity=0.7, fill='tozeroy'), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=df2['date'], y=df2['average transit stations(5d)'], name='Mobility Change at Transit Stations',
                   line=dict(color='green')), secondary_y=True)

#     range2 = int(round(df2['average transit stations(5d)'].min(), -1))
    range2 = -80
    fig.update_yaxes(title='Vaccination Percentage', range=[-100, 100], secondary_y=False)
    fig.update_yaxes(title='Mobility Change (%)', range=[range2, range2 * (-1)], secondary_y=True)
    fig.update_layout(
        margin=dict(l=0, r=0, b=150, t=50),
        legend=dict(orientation='h', yanchor="top", y=-0.2, xanchor="center", x=0.5))
    #fig.update_layout(title='<b>Vaccination vs Transit Stations Mobility')
    return fig


def plot4(df1, df2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df2 = df2[(df2['date'] > '2021-01-01') & (df2['date'] < '2022-01-01')]
    fig.add_trace(go.Scatter(x=df1['DATE'], y=df1['TAVG'], name="Average Temp", line=dict(color='hotpink')),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df2['date'], y=df2['average workplaces(5d)'], name='Mobility Change at Workplaces',
                             line=dict(color='orange')), secondary_y=True)

    range2 = int(round(df2['average workplaces(5d)'].min(), -1))

    fig.update_yaxes(title='Average Temperature (C)', range=[-25, 35], secondary_y=False)
    fig.update_yaxes(title='Mobility Change (%)', range=[range2, range2 * (-1)], secondary_y=True)
    fig.update_layout(margin=dict(l=0, r=0, b=100, t=50),
                      legend=dict(orientation='h', yanchor="bottom", y=-0.35, xanchor="center", x=0.5))
    #fig.update_layout(title='<b>Historical Weather vs Workplaces Mobility')
    return fig


def plot5(df1, df2):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df2['date'], y=df2['lower'], showlegend=False, hoverinfo='none', line=dict(color='darksalmon')))
    fig.add_trace(
        go.Scatter(x=df2['date'], y=df2['upper'], hoverinfo='none', line=dict(color='darksalmon'), fill='tonexty',
                   name='Confidence Interval'))
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['average transit stations(5d)'], name='Transit Stations',
                             line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df2['date'], y=df2['predicted_mean'], name='Prediction', line=dict(color='darkred')))
    # fig.add_hline(y=0, line_color=Lightblue, annotation_text='Baseline Feb 2020', annotation_position='top right')

    # fig.update_xaxes(showgrid=True)
    fig.update_yaxes(title='% Mobility Change from Baseline', showgrid=True)
    fig.update_layout(
        margin=dict(l=50, r=50, b=100, t=50),
        legend=dict(orientation='h', yanchor="bottom", y=-0.35, xanchor="center", x=0.5,bordercolor="Black",
                    borderwidth=2))
    #fig.update_layout(title='<b>Mobility Forecast using Multivariate Prediction Model')

    return fig


def plot6(df1, df2, city):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['percent of 1st dose'], name='vaccinated first dose (%)',
                             line=dict(color='mediumpurple'), fill='tozeroy', opacity=0.1, yaxis='y1'))
    fig.add_trace(
        go.Scatter(x=df1['date'], y=df1['percent of 2nd dose'], name='vaccinated second dose (%)', line=dict(color='red'),
                   fill='tozeroy', opacity=0.1, yaxis='y1'))
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['percent of 3rd dose'], name='vaccinated third dose (%)',
                             line=dict(color='greenyellow'), fill='tozeroy', opacity=0.1, yaxis='y1'))
    fig.add_trace(go.Scatter(x=df1['date'], y=df1['covid per10k'], name='Covid per 10K Population', fill='tozeroy',
                             line=dict(color='lightsalmon'), yaxis='y2'))
    fig.add_trace(
        go.Scatter(x=df2['date'], y=df2['average transit stations(5d)'], name='Mobility Change at Transit Stations',
                   line=dict(color='green'), yaxis='y1'))
    fig.add_annotation(x='2021-04-28', y=0, text="Delta variant<br>28-Apr", align='center', showarrow=True, arrowhead=5,
                       arrowwidth=2, arrowside='end', arrowcolor='blue',
                       ax=0, ay=-80, xanchor='right', yanchor='bottom', font=dict(color="maroon", size=11))
    fig.add_annotation(x='2021-11-26', y=0, text='Omicron variant<br>26-nov', align='left', showarrow=True, arrowhead=2,
                       arrowwidth=1.5, arrowside='end', arrowcolor='blue',
                       ax=0, ay=-100, xanchor='right', yanchor='bottom', font=dict(color="maroon", size=11))
    
#     range1 = int(round(df1['covid per10k'].max(), -1)) + 10

#     range2 = int(round(df2['average transit stations(5d)'].min(), -1))
#     if range2 > -100:
#         range2 = -100
    range1 = 100
    range2 = -100
    

    fig.update_layout(
        yaxis=dict(title='Vaccination Rate / Mobility Change', side='right', range=[range2, range2 * (-1)]),
        yaxis2=dict(title='Covid Cases', side='left', overlaying='y', range=[range1 * (-1), range1]),
        legend=dict(orientation='h', yanchor="top", y=-0.2, xanchor="center", x=0.5, bordercolor="Black",
                    borderwidth=2))
    fig.update_layout(title=city, title_font_size=25)

    return fig

def kpi(df):        
    return df[['percent of 1st dose','percent of 2nd dose','percent of 3rd dose']].max()

def kpi2(df):
    latest = datetime.strptime(df['date'].iloc[-10], '%Y-%m-%d').strftime('%d-%b')
    return [round(df['average workplaces(5d)'].iloc[-10:].mean()-df['average workplaces(5d)'].iloc[:-10].mean()), round(df['average transit stations(5d)'].iloc[-10:].mean()-df['average transit stations(5d)'].iloc[:-10].mean()), latest]

########################################### Layout Functions ##########################################################
def title1(city, df):
    latest = df['date'].iloc[-1]
    layout = dbc.Card([
        dbc.Row([
            dbc.Col([dbc.CardImg(src="assets/wsp_logo.png", className="img-fluid rounded-start")
            ], width=2, xl=2, className = "mr-2"),
            dbc.Col([dbc.CardBody(id=f'title_{city}')
            ], width=8, xl=8),
        ],className="g-0 d-flex align-items-center"),
    ],color=Lightblue, outline = False, className='mb-3 mt-3', style={'font-family':'Montserrat'})
    return layout


def title_over(city):
    title = dbc.Card([
        dbc.Row([
            dbc.Col([dbc.CardImg(src="assets/wsp_logo.png", className="img-fluid rounded-start")
            ], width=2, xl=2),
            dbc.Col([dbc.CardBody([html.H1("Comparing mobility change in different cities"),
                                html.P(t6, className="card-text")]),
                    ], width=10, xl=10),
        ],className="g-0 d-flex align-items-center")        
    ],color=Lightblue, outline = False, className='mb-3 mt-3', style={'font-family':'Montserrat'})
    return title      

def kpi_vacc1(city):
    return dbc.Card([dbc.CardBody(id=f'kpi1_{city}',
                    className='border-0 text-white rounded-lg')], color=Red)

def kpi_vacc2(city):
    return dbc.Card([dbc.CardBody(id=f'kpi2_{city}',
                    className='border-0 text-white rounded-lg')], color=Red)

def kpi_vacc3(city):
    return dbc.Card([dbc.CardBody(id=f'kpi3_{city}',
                    className='border-0 text-white rounded-lg')], color=Red)

def kpi_workplace(city):
    return dbc.Card([dbc.CardBody(id=f'kpiwork_{city}',
                    className='border-0 text-white rounded-lg')], color = Charcoal_blue)

def kpi_transit(city):
    return dbc.Card([dbc.CardBody(id=f'kpitrans_{city}',
                    className='border-0 text-white rounded-lg')], color = Charcoal_blue)

def graph1(city):
    return dbc.Card([dbc.CardBody([
        html.H5("Transit Stations Mobility vs Covid Cases"),
        html.P(t1, className="card-text"),
        dcc.Graph(id=f'covid_mob_{city}',figure={},config = {'staticPlot': True}),])])

def graph2(city):
    return dbc.Card([dbc.CardBody([
        html.H5("Mobility at Transit Stations vs Workplaces"),
        html.P(t2, className="card-text"),
        dcc.Graph(id=f'work_trans_{city}',figure={},config = {'staticPlot': True}),])])
    
def graph3(city):
    return dbc.Card([dbc.CardBody([
        html.H5("Vaccination vs Transit Stations Mobility"),
        html.P(t3, className="card-text"),
        dcc.Graph(id=f'vacc123_{city}',figure={},config = {'staticPlot': True}),])])

def graph4(city):
    return dbc.Card([dbc.CardBody([
        html.H5("Historical Weather vs Workplaces Mobility"),
        html.P(t4, className="card-text"),
        dcc.Graph(id=f'weather_{city}',figure={},config = {'staticPlot': True}),])])

def graph5(city):
    return dbc.Card([dbc.CardBody([
        html.H5("Mobility Forecast"),
        html.P(t5, className="card-text"),
        dcc.Graph(id=f'pred_{city}',figure={},config = {'staticPlot': True}),])])

def graph6(city):
    return dbc.Card([dbc.CardBody([
        #html.H5(city.title()),
        #html.P(t6, className="card-text"),
        dcc.Graph(id=f'overview_{city}',figure={},config = {'staticPlot': True}),])])

title2 = dbc.Card(html.H1("Can we forecast mobility change on transit station?"), 
                  body=True, color=Lightblue, outline = False, className='mb-2 mt-2')


## Update Text on about
about_text = '''
# Digital Insights from WSP Advisory

---

### The purpose

The purpose of this dashboard is to present insights on mobility changes in response to the pandemic and 
specifically answer the question how the pandemic impacting public transportation. The aim is that 
this will help everyone working with public transportation to have the necessary data for decision making 
that is needed for recovery in the sector.

Several cities’ data are retrieved from [Google Mobility](https://www.google.com/covid19/mobility/) and other governmental 
institutions e.g., [United Kingdom Government website](https://coronavirus.data.gov.uk/), 
[Israel Government Database](https://info.data.gov.il/datagov/home/), 
[Sweden Public Health Agency](https://www.folkhalsomyndigheten.se/), and 
[Denmark Statens Serum Institut](https://www.ssi.dk/) and combined to give better understanding of the status in 
those cities with regards to mobility, covid cases, vaccination status etc and the impact that each have on the other.

### The dashboard

The Tabs along the top allows you to see the data for the various cities and the Overview tab allows you to compare 
the cities.

### Insights so far

The data shows that even with a high vaccination rate a Covid outbreak can still occur as the key variable is 
the virus variant and its ability to evade the vaccine. This is in other word the vaccine efficacy. 
Other variables such as the need to reach herd immunity is of less significance. The data also shows that 
recovery will be in the longer term and attitudes towards public transportation has changed meaning a bounce 
back to 2019 levels is a longer-term aspiration.

---

###### the small print

These following information provide an understanding of how KPIs (Key Performance Indicators) are 
calculated and how statistical methods are chosen. Cities such as London and Tel Aviv are chosen since those are 
advanced in vaccination rate and the impact can be observed. The approach then could be applied for nordic cities 
in the future as well.

###### Google mobility data

See here for more information on this data [COVID-19 Community Mobility Reports](https://www.google.com/covid19/mobility/data_documentation.html?hl=en)

###### Mobility Change data:

This includes mobility data for the following trip purposes Workplaces and Transit Stations. 
For these graphs, the weekend data (sat and sun) has been omitted as the weekday is the main focus of the study. 
Workplaces represent trips to and from places of work and Transit Stations collect trips to and from public transport 
hubs. The mobility change baseline is Jan 3 – Feb 6, 2020, from Google Mobility.

###### Covid data:

Covid data is based on population in order to compare covid density for various cities. 
Official sources of the data have been used as much as possible however accuracy cannot be guaranteed.

###### Vaccine data:

Vaccination ratio is based on all-age population. Although third dose program has started in most cities in 
some cases there are no accumulated data available. Vaccine data has a delay of around 2 weeks compared to 
other data types which reflects the delay of the dashboard.

###### KPI for population vaccinated:

This is a ratio of total number of persons vaccinated in the country divided by total population.

###### KPI for mobility change:

The KPI captures the last 2 weeks mobility change from the average of the mobility data up to the last two weeks.

###### Prediction method:

For each city, a prediction model has been chosen to give the best validation. This has with the current data 
proved to be the Vector Autoregression from Stats model. This model has captured the relationship between 
multiple variables as they change over time to make predictions. Research into other models is ongoing.

---

'''

sm1 = "Developed by Desmond Wright, Shiyi Peng, Husni Sutrisno"
sm2 = "Digital Rail Systems (DRS), WSP Advisory"

## graph small text
t6 = "Combining mobility change, covid cases, and vaccination rates, all in one graph"
t1 = "Correlation between covid cases and mobility at transit stations"
t2 = "Are people that using transit stations going to work?"
t3 = "How is mobility reacting to increasing vaccinated population?"
t4 = "Is there any correlation between outside average temperature and mobility?"
t5 = "Forecast of future mobility based on current state of covid cases and vaccination rates in the city"

## Insights for overview tab
stock1 = "Stockholm’s transit change went down from the baseline but has been relatively stable regardless several outbreaks. Under Stockholm tab in this dashboard, a comparison shows public transit has not been impacted strongly during summer vacation when majority population are on vacation."
stock2 = "Do people rely on public transport less and less for commuting trips in Stockholm?"
lond1 = "People in Greater London still used public transport even though delta variant appeared and covid cases increased after april 2021. When almost 50% population is vaccinated for second dose after August 2021, activity at transit stations was jumped almost 10% compared to before summer."
lond2 = "Do people tend to be more confidence to use public transport when covid vaccination rate is high?"
tel1 = "As one of the vaccine pioneer's cities, Tel Aviv commenced its early vaccine journey among society. With a fairly high vaccination rate, the mobility change at transit stations went to a strike at almost every Covid outbreak. Under Tel Aviv tab in this dashboard, it depicts workplace mobility has become higher than transit mobility."
tel2 = "Does people's travel behaviour shift away from public transit because of the fear of Covid?"
cop1 = "Public transports mobility in Copenhagen at beginning of 2021 was below 50% from baseline. Then it increased quickly almost back to mobility baseline level February 2020 before going down as winter vacation came and at the same time the covid cases was at highest peak. Starting 2022, workplaces mobility is increasing again but transit stations mobility is still lower than before christmas."
cop2 = "Do people prefer to use private transport for commuting since covid cases are still high?"
osl1 = "Oslo has same trend with other Nordic cities in term of people's travel behaviour during 2021. Compared to baseline level, mobility in public transit stations is reduced to 50% in the first quarter of 2021. However, after August it was steadily increased 20% below winter vacation. By observing the mobility at workplaces and transit stations, it shows that people tend to use public transports for commuting to office which is indicated by the same trend between those two data. On the other hand, high number of covid cases at beginning of 2022 is not diverting people from using public transport."
osl2 = "Does public transport in Oslo withstand the impact of Covid-19 pandemic?"
hel1 = "Mobility in Helsinki's public transits was at stable level around 35% from baseline starting Autumn until the end of 2021. This similar trend with other Nordic capitals shows that same people's travel behaviour between their neighbours. Although vaccination rate is slower than other, reaching 70% for second dose just before late December 2021, people still used public transport to travel to workplaces. As mobility at transit stations was increased during 2021, the covid cases was lower than other cities. This means that Helsinki could minimize the covid spreading in public transport."
hel2 = "Will people's mobility bounce back sooner? or stable as new normal behaviour prevails?"

########################## Layout Structure ###########################################################################
## Stockholm Tab
tab1_content = [
    title1('Stockholm', df_stockholm),
    dbc.Row([
        dbc.Col([kpi_vacc1('Stockholm')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_vacc2('Stockholm')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_vacc3('Stockholm')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_workplace('Stockholm')],width=6, xl=3),
        dbc.Col([kpi_transit('Stockholm')],width=6, xl=3)]),
    
    dbc.Row([
        dbc.Col([graph1('stockholm')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph2('stockholm')],xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([graph3('stockholm')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph4('stockholm')],xl=6, className = 'mt-3 mb-3')]),
    
    title2,
    dbc.Row([
        dbc.Col(graph5('stockholm'))], className = 'mt-3 mb-3')
]

## London Tab
tab2_content = [
    title1('Greater London', df_london),
    dbc.Row([
        dbc.Col([kpi_vacc1('Greater London')],width=4, xl=2),
        dbc.Col([kpi_vacc2('Greater London')],width=4, xl=2),
        dbc.Col([kpi_vacc3('Greater London')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_workplace('Greater London')],width=6, xl=3),
        dbc.Col([kpi_transit('Greater London')],width=6, xl=3)]),
    
    dbc.Row([
        dbc.Col([graph1('london')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph2('london')],xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([graph3('london')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph4('london')],xl=6, className = 'mt-3 mb-3')]),
    
    title2,
    dbc.Row([
        dbc.Col(graph5('london'))], className = 'mt-3 mb-3')
]

## Copenhagen Tab
tab3_content = [
    title1('Copenhagen', df_copenhagen),
    dbc.Row([
        dbc.Col([kpi_vacc1('Copenhagen')],width=4, xl=2),
        dbc.Col([kpi_vacc2('Copenhagen')],width=4, xl=2),
        dbc.Col([kpi_vacc3('Copenhagen')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_workplace('Copenhagen')],width=6, xl=3),
        dbc.Col([kpi_transit('Copenhagen')],width=6, xl=3)]),
    
    dbc.Row([
        dbc.Col([graph1('copenhagen')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph2('copenhagen')],xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([graph3('copenhagen')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph4('copenhagen')],xl=6, className = 'mt-3 mb-3')]),
    
    title2,
    dbc.Row([
        dbc.Col([graph5('copenhagen')])], className = 'mt-3 mb-3')
]

## Tel-Aviv Tab
tab4_content = [
    title1('Tel Aviv', df_telaviv),
    dbc.Row([
        dbc.Col([kpi_vacc1('Tel Aviv')],width=4, xl=2),
        dbc.Col([kpi_vacc2('Tel Aviv')],width=4, xl=2),
        dbc.Col([kpi_vacc3('Tel Aviv')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_workplace('Tel Aviv')],width=6, xl=3),
        dbc.Col([kpi_transit('Tel Aviv')],width=6, xl=3)]),
    
    dbc.Row([
        dbc.Col([graph1('telaviv')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph2('telaviv')],xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([graph3('telaviv')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph4('telaviv')],xl=6, className = 'mt-3 mb-3')]),
    
    title2,
    dbc.Row([
        dbc.Col([graph5('telaviv')])], className = 'mt-3 mb-3')
]

## Oslo Tab
tab5_content = [
    title1('Oslo', df_oslo),
    dbc.Row([
        dbc.Col([kpi_vacc1('Oslo')],width=4, xl=2),
        dbc.Col([kpi_vacc2('Oslo')],width=4, xl=2),
        dbc.Col([kpi_vacc3('Oslo')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_workplace('Oslo')],width=6, xl=3),
        dbc.Col([kpi_transit('Oslo')],width=6, xl=3)]),
    
    dbc.Row([
        dbc.Col([graph1('oslo')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph2('oslo')],xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([graph3('oslo')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph4('oslo')],xl=6, className = 'mt-3 mb-3')]),
    
    title2,
    dbc.Row([
        dbc.Col([graph5('oslo')])], className = 'mt-3 mb-3')
]

## Helsinki Tab
tab6_content = [
    title1('Helsinki', df_helsinki),
    dbc.Row([
        dbc.Col([kpi_vacc1('Helsinki')],width=4, xl=2),
        dbc.Col([kpi_vacc2('Helsinki')],width=4, xl=2),
        dbc.Col([kpi_vacc3('Helsinki')],width=4, xl=2, className = 'mb-3'),
        dbc.Col([kpi_workplace('Helsinki')],width=6, xl=3),
        dbc.Col([kpi_transit('Helsinki')],width=6, xl=3)]),
    
    dbc.Row([
        dbc.Col([graph1('helsinki')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph2('helsinki')],xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([graph3('helsinki')],xl=6, className = 'mt-3 mb-3'),
        dbc.Col([graph4('helsinki')],xl=6, className = 'mt-3 mb-3')]),
    
    title2,
    dbc.Row([
        dbc.Col([graph5('helsinki')])], className = 'mt-3 mb-3')
]

## Overview Tab
tab7_content = [
    title_over('All Observed Cities'),
     dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col([graph6('stockholm')])),
            dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([html.P(stock1), html.Strong(stock2)])],color=Light_gray_50)))
        ],width=12, xl=6, className = 'mt-3 mb-3'),
        dbc.Col([
            dbc.Row(dbc.Col(graph6('london'))),
            dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([html.P(lond1), html.Strong(lond2)])],color=Light_gray_50)))
        ],width=12, xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col([graph6('copenhagen')])),
            dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([html.P(cop1), html.Strong(cop2)])],color=Light_gray_50)))
        ],width=12, xl=6, className = 'mt-3 mb-3'),
        dbc.Col([
            dbc.Row(dbc.Col(graph6('tel aviv'))),
            dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([html.P(tel1), html.Strong(tel2)])],color=Light_gray_50)))
        ],width=12, xl=6, className = 'mt-3 mb-3')]),
    
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col([graph6('oslo')])),
            dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([html.P(osl1), html.Strong(osl2)])],color=Light_gray_50)))
        ],width=12, xl=6, className = 'mt-3 mb-3'),
        dbc.Col([
            dbc.Row(dbc.Col(graph6('helsinki'))),
            dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([html.P(hel1), html.Strong(hel2)])],color=Light_gray_50)))
        ],width=12, xl=6, className = 'mt-3 mb-3')])
]

## About Tab
tab8_content = [
    dbc.Card([
        dbc.CardBody([
            dcc.Markdown(about_text),
            html.Small("Developed by Desmond Wright, Shiyi Peng, Husni Sutrisno", className="card-text", style={'font-family':'Montserrat'}),
            html.Br(),
            html.Small("Digital Rail Systems (DRS), WSP Advisory", className="card-text", style={'font-family':'Montserrat'}),
            html.Br(),
        ])
    ], color=Lightblue, inverse=False, outline=True, className='mb-3 mt-3'),
    dbc.Card([
        dbc.Row([
            dbc.Col([dbc.CardImg(src="assets/wsp_logo.png", className="img-fluid rounded-start")
                     ], className="col-md-2"),
        ], className="g-0 d-flex align-items-right")
    ], color="light", outline=True, className='mb-3'),
    
    dcc.Interval(
        id='live-update',
        interval=86400*1000, ## To refresh the dashboard each day --> 1 day = 86400 second
        n_intervals=0
    )
]

tabs = dbc.Tabs([
    dbc.Tab(tab1_content, label="Stockholm", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab2_content, label="London", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab3_content, label="Copenhagen", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab4_content, label="Tel Aviv", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab5_content, label="Oslo", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab6_content, label="Helsinki", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab7_content, label="Overview", activeLabelClassName="text-danger fw-bold"),
    dbc.Tab(tab8_content, label="About", activeLabelClassName="text-danger fw-bold"),
]) 


########################################### Dash python ################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], title='Digital Insights WSP', meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=0.5, maximum-scale=1"}]) 
server = app.server
app.layout = dbc.Container([tabs],fluid=True)

######################################## Callback Functions for Graphs #################################################


#### Function for refreshing the latest date on title

def title_refresh(df, city):
    latest = df['date'].iloc[-1]
    text = [html.H1(f"COVID-19 vs Mobility Change in {city}"), html.P(f'Latest data: {latest}', style={'font-family':'Montserrat'})]
    return text

#### Function for refreshing the KPI number on each city

def kpi_refresh(df1, df2):
    kp1 = [html.H2(str(round(kpi(df1)[0]))+'%', className="card-title text-center"),
            html.H6("Population Vaccinated", className="text-center"),
            html.H6("First Dose", className="text-center mt-0")]
    
    kp2 = [html.H2(str(round(kpi(df1)[1]))+'%', className="card-title text-center"),
           html.H6("Population Vaccinated", className="text-center"),
           html.H6("Second Dose", className="text-center p-0")]
    
    kp3 = [html.H2(str(round(kpi(df1)[2]))+'%', className="card-title text-center"),
            html.H6("Population Vaccinated", className="text-center"),
            html.H6("Third Dose", className="text-center")]
    
    kpi_work = [html.H2(str(kpi2(df2)[0])+'%', className="card-title text-center"),
                html.H6("Workplaces Mobility Change", className="text-center"),
                html.H6(f"from last 2 weeks ({kpi2(df2)[2]})", className="text-center")]
    
    kpi_trans = [html.H2(str(kpi2(df2)[1])+'%', className="card-title text-center"),
                html.H6("Transit Stations Mobility Change", className="text-center"),
                html.H6(f"from last 2 weeks ({kpi2(df2)[2]})", className="text-center")]
    
    return kp1, kp2, kp3, kpi_work, kpi_trans

@app.callback(
    [Output('kpi1_Stockholm', 'children'),
    Output('kpi2_Stockholm', 'children'),
    Output('kpi3_Stockholm', 'children'),
    Output('kpiwork_Stockholm', 'children'),
    Output('kpitrans_Stockholm', 'children')],
    [Input('live-update', 'n_intervals')])
def kpi_text(n):
    kp1, kp2, kp3, kpi_work, kpi_trans = kpi_refresh(df_stockholm, df_stockholm_mob)
    return kp1, kp2, kp3, kpi_work, kpi_trans

@app.callback(
    [Output('kpi1_Greater London', 'children'),
    Output('kpi2_Greater London', 'children'),
    Output('kpi3_Greater London', 'children'),
    Output('kpiwork_Greater London', 'children'),
    Output('kpitrans_Greater London', 'children')],
    [Input('live-update', 'n_intervals')])
def kpi_text(n):
    kp1, kp2, kp3, kpi_work, kpi_trans = kpi_refresh(df_london, df_london_mob)
    return kp1, kp2, kp3, kpi_work, kpi_trans

@app.callback(
    [Output('kpi1_Copenhagen', 'children'),
    Output('kpi2_Copenhagen', 'children'),
    Output('kpi3_Copenhagen', 'children'),
    Output('kpiwork_Copenhagen', 'children'),
    Output('kpitrans_Copenhagen', 'children')],
    [Input('live-update', 'n_intervals')])
def kpi_text(n):
    kp1, kp2, kp3, kpi_work, kpi_trans = kpi_refresh(df_copenhagen, df_copenhagen_mob)
    return kp1, kp2, kp3, kpi_work, kpi_trans

@app.callback(
    [Output('kpi1_Tel Aviv', 'children'),
    Output('kpi2_Tel Aviv', 'children'),
    Output('kpi3_Tel Aviv', 'children'),
    Output('kpiwork_Tel Aviv', 'children'),
    Output('kpitrans_Tel Aviv', 'children')],
    [Input('live-update', 'n_intervals')])
def kpi_text(n):
    kp1, kp2, kp3, kpi_work, kpi_trans = kpi_refresh(df_telaviv, df_telaviv_mob)
    return kp1, kp2, kp3, kpi_work, kpi_trans

@app.callback(
    [Output('kpi1_Helsinki', 'children'),
    Output('kpi2_Helsinki', 'children'),
    Output('kpi3_Helsinki', 'children'),
    Output('kpiwork_Helsinki', 'children'),
    Output('kpitrans_Helsinki', 'children')],
    [Input('live-update', 'n_intervals')])
def kpi_text(n):
    kp1, kp2, kp3, kpi_work, kpi_trans = kpi_refresh(df_helsinki, df_helsinki_mob)
    return kp1, kp2, kp3, kpi_work, kpi_trans

@app.callback(
    [Output('kpi1_Oslo', 'children'),
    Output('kpi2_Oslo', 'children'),
    Output('kpi3_Oslo', 'children'),
    Output('kpiwork_Oslo', 'children'),
    Output('kpitrans_Oslo', 'children')],
    [Input('live-update', 'n_intervals')])
def kpi_text(n):
    kp1, kp2, kp3, kpi_work, kpi_trans = kpi_refresh(df_oslo, df_oslo_mob)
    return kp1, kp2, kp3, kpi_work, kpi_trans


## Tab 1 - Stockholm
@app.callback(
    [Output('title_Stockholm','children'),
    Output('title_Greater London','children'),
    Output('title_Copenhagen','children'),
    Output('title_Tel Aviv','children'),
    Output('title_Helsinki','children'),
    Output('title_Oslo','children')],
    [Input('live-update', 'n_intervals')])
def title_text(n):
    text_stockholm = title_refresh(df_stockholm, 'Stockholm')
    text_london = title_refresh(df_london, 'Greater London')
    text_copenhagen = title_refresh(df_copenhagen, 'Copenhagen')
    text_telaviv = title_refresh(df_telaviv, 'Tel Aviv')
    text_helsinki = title_refresh(df_helsinki, 'Helsinki')
    text_oslo = title_refresh(df_oslo, 'Oslo')
    return text_stockholm, text_london, text_copenhagen, text_telaviv, text_helsinki, text_oslo


@app.callback(
    Output('covid_mob_stockholm','figure'),
    [Input('live-update','n_intervals')],)
def covid_mob_fig(figure):
    update_datasets()
    fig = plot1(df_stockholm, df_stockholm_mob)
    return fig

@app.callback(
    Output('work_trans_stockholm','figure'),
    [Input('live-update','n_intervals')],)
def work_trans_fig(figure):
    fig = plot2(df_stockholm_mob)
    return fig

@app.callback(
    Output('vacc123_stockholm','figure'),
    [Input('live-update','n_intervals')],)
def vacc_fig(figure):
    fig = plot3(df_stockholm, df_stockholm_mob)
    return fig

@app.callback(
    Output('weather_stockholm','figure'),
    [Input('weather_stockholm','figure')],)
def weather_fig(figure):
    fig = plot4(df_weather[df_weather['NAME']=='STOCKHOLM, SW'], df_stockholm_mob)
    return fig

@app.callback(
    Output('pred_stockholm','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot5(df_stockholm_mob, df_stockholm_var)
    return fig

## Tab 2 - London

@app.callback(
    Output('covid_mob_london','figure'),
    [Input('live-update','n_intervals')],)
def covid_mob_fig(figure):
    fig = plot1(df_london, df_london_mob)
    return fig

@app.callback(
    Output('work_trans_london','figure'),
    [Input('live-update','n_intervals')],)
def work_trans_fig(figure):
    fig = plot2(df_london_mob)
    return fig

@app.callback(
    Output('vacc123_london','figure'),
    [Input('live-update','n_intervals')],)
def vacc_fig(figure):
    fig = plot3(df_london, df_london_mob)
    return fig

@app.callback(
    Output('weather_london','figure'),
    [Input('weather_london','figure')],)
def weather_fig(figure):
    fig = plot4(df_weather[df_weather['NAME']=='HEATHROW, UK'], df_london_mob)
    return fig

@app.callback(
    Output('pred_london','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot5(df_london_mob, df_london_var)
    return fig

## Tab 3 - Copenhagen

@app.callback(
    Output('covid_mob_copenhagen','figure'),
    [Input('live-update','n_intervals')],)
def covid_mob_fig(figure):
    fig = plot1(df_copenhagen, df_copenhagen_mob)
    return fig

@app.callback(
    Output('work_trans_copenhagen','figure'),
    [Input('live-update','n_intervals')],)
def work_trans_fig(figure):
    fig = plot2(df_copenhagen_mob)
    return fig

@app.callback(
    Output('vacc123_copenhagen','figure'),
    [Input('live-update','n_intervals')],)
def vacc_fig(figure):
    fig = plot3(df_copenhagen, df_copenhagen_mob)
    return fig

@app.callback(
    Output('weather_copenhagen','figure'),
    [Input('weather_copenhagen','figure')],)
def weather_fig(figure):
    fig = plot4(df_weather[df_weather['NAME']=='STOCKHOLM, SW'], df_copenhagen_mob)
    return fig

@app.callback(
    Output('pred_copenhagen','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot5(df_copenhagen_mob, df_copenhagen_var)
    return fig

## Tab 4 - Tel Aviv

@app.callback(
    Output('covid_mob_telaviv','figure'),
    [Input('live-update','n_intervals')],)
def covid_mob_fig(figure):
    fig = plot1(df_telaviv, df_telaviv_mob)
    return fig

@app.callback(
    Output('work_trans_telaviv','figure'),
    [Input('live-update','n_intervals')],)
def work_trans_fig(figure):
    fig = plot2(df_telaviv_mob)
    return fig

@app.callback(
    Output('vacc123_telaviv','figure'),
    [Input('live-update','n_intervals')],)
def vacc_fig(figure):
    fig = plot3(df_telaviv, df_telaviv_mob)
    return fig

@app.callback(
    Output('weather_telaviv','figure'),
    [Input('weather_telaviv','figure')],)
def weather_fig(figure):
    fig = plot4(df_weather[df_weather['NAME']=='BEN GURION, IS'], df_telaviv_mob)
    return fig

@app.callback(
    Output('pred_telaviv','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot5(df_telaviv_mob, df_telaviv_var)
    return fig

## Tab 5 - Oslo

@app.callback(
    Output('covid_mob_oslo','figure'),
    [Input('live-update','n_intervals')],)
def covid_mob_fig(figure):
    fig = plot1(df_oslo, df_oslo_mob)
    return fig

@app.callback(
    Output('work_trans_oslo','figure'),
    [Input('live-update','n_intervals')],)
def work_trans_fig(figure):
    fig = plot2(df_oslo_mob)
    return fig

@app.callback(
    Output('vacc123_oslo','figure'),
    [Input('live-update','n_intervals')],)
def vacc_fig(figure):
    fig = plot3(df_oslo, df_oslo_mob)
    return fig

@app.callback(
    Output('weather_oslo','figure'),
    [Input('weather_oslo','figure')],)
def weather_fig(figure):
    fig = plot4(df_weather[df_weather['NAME']=='STOCKHOLM, SW'], df_oslo_mob)
    return fig

@app.callback(
    Output('pred_oslo','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot5(df_oslo_mob, df_oslo_var)
    return fig

## Tab 6 - Helsinki

@app.callback(
    Output('covid_mob_helsinki','figure'),
    [Input('live-update','n_intervals')],)
def covid_mob_fig(figure):
    fig = plot1(df_helsinki, df_helsinki_mob)
    return fig

@app.callback(
    Output('work_trans_helsinki','figure'),
    [Input('live-update','n_intervals')],)
def work_trans_fig(figure):
    fig = plot2(df_helsinki_mob)
    return fig

@app.callback(
    Output('vacc123_helsinki','figure'),
    [Input('live-update','n_intervals')],)
def vacc_fig(figure):
    fig = plot3(df_helsinki, df_helsinki_mob)
    return fig

@app.callback(
    Output('weather_helsinki','figure'),
    [Input('weather_helsinki','figure')],)
def weather_fig(figure):
    fig = plot4(df_weather[df_weather['NAME']=='STOCKHOLM, SW'], df_helsinki_mob)
    return fig

@app.callback(
    Output('pred_helsinki','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot5(df_helsinki_mob, df_helsinki_var)
    return fig

## Tab Overview

@app.callback(
    Output('overview_stockholm','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot6(df_stockholm, df_stockholm_mob, 'Stockholm')
    return fig

@app.callback(
    Output('overview_london','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot6(df_london, df_london_mob, 'Greater London')
    return fig

@app.callback(
    Output('overview_copenhagen','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot6(df_copenhagen, df_copenhagen_mob, 'Copenhagen')
    return fig

@app.callback(
    Output('overview_tel aviv','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot6(df_telaviv, df_telaviv_mob, 'Tel Aviv')
    return fig

@app.callback(
    Output('overview_oslo','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot6(df_oslo, df_oslo_mob, 'Oslo')
    return fig

@app.callback(
    Output('overview_helsinki','figure'),
    [Input('live-update','n_intervals')],)
def pred_fig(figure):
    fig = plot6(df_helsinki, df_helsinki_mob, 'Helsinki')
    return fig

if __name__ == '__main__':
    app.run_server()
