# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Analysis Dashboard - Business Edition
High-end business dashboard with interactive filtering and relationship analysis
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv("pet_adoption.csv")

# Data preprocessing
df['AgeYears'] = df['AgeMonths'] / 12
df['AgeGroup'] = pd.cut(df['AgeYears'], bins=[0, 1, 3, 7, 15, 100], 
                        labels=['Young (0-1y)', 'Youth (1-3y)', 'Adult (3-7y)', 'Middle (7-15y)', 'Senior (15+y)'])

# Create Dash app
app = dash.Dash(__name__)

# Function to apply filters
def apply_filters(data, pet_type, age_range, vaccine_status, health_condition):
    filtered_data = data.copy()
    
    # Apply pet type filter
    if pet_type != 'All':
        filtered_data = filtered_data[filtered_data['PetType'] == pet_type]
    
    # Apply age range filter
    if age_range:
        filtered_data = filtered_data[
            (filtered_data['AgeYears'] >= age_range[0]) & 
            (filtered_data['AgeYears'] <= age_range[1])
        ]
    
    # Apply vaccination filter
    if vaccine_status != 'All':
        filtered_data = filtered_data[filtered_data['Vaccinated'] == vaccine_status]
    
    # Apply health condition filter
    if health_condition != 'All':
        filtered_data = filtered_data[filtered_data['HealthCondition'] == health_condition]
    
    return filtered_data

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🐾 Premium Pet Adoption Analytics Dashboard", 
                style={
                    'background': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                    'color': 'white',
                    'padding': '40px',
                    'textAlign': 'center',
                    'margin': '0',
                    'fontSize': '2.8rem',
                    'fontWeight': '300',
                    'letterSpacing': '1px',
                    'borderRadius': '0'
                }),
        html.P("Advanced Data Analytics for Pet Adoption Success",
               style={
                   'background': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                   'color': 'rgba(255,255,255,0.9)',
                   'padding': '0 40px 40px 40px',
                   'textAlign': 'center',
                   'margin': '0',
                   'fontSize': '1.2rem',
                   'fontWeight': '300',
                   'letterSpacing': '0.5px'
               })
    ]),
    
    # Premium filter panel - business focused
    html.Div([
        html.Div([
            html.Div([
                html.Label("PET TYPE", style={
                    'fontWeight': '700', 
                    'color': '#1e3c72', 
                    'fontSize': '0.9rem',
                    'textTransform': 'uppercase',
                    'letterSpacing': '1px',
                    'marginBottom': '12px'
                }),
                dcc.Dropdown(
                    id='pet-type-filter',
                    options=[{'label': 'All Types', 'value': 'All'}] + 
                            [{'label': pet_type, 'value': pet_type} for pet_type in df['PetType'].unique()],
                    value='All',
                    style={
                        'borderRadius': '8px',
                        'border': '2px solid #e1e8ed',
                        'backgroundColor': '#ffffff',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                    }
                )
            ], style={'flex': '1', 'minWidth': '220px'}),
            
            html.Div([
                html.Label("AGE RANGE (YEARS)", style={
                    'fontWeight': '700', 
                    'color': '#1e3c72', 
                    'fontSize': '0.9rem',
                    'textTransform': 'uppercase',
                    'letterSpacing': '1px',
                    'marginBottom': '12px'
                }),
                dcc.RangeSlider(
                    id='age-filter',
                    min=0,
                    max=20,
                    step=0.5,
                    value=[0, 20],
                    marks={i: f'{i}y' for i in range(0, 21, 2)},
                    tooltip={'placement': 'bottom', 'always_visible': True}
                )
            ], style={'flex': '2.5', 'minWidth': '350px'}),
            
            html.Div([
                html.Label("VACCINATION STATUS", style={
                    'fontWeight': '700', 
                    'color': '#1e3c72', 
                    'fontSize': '0.9rem',
                    'textTransform': 'uppercase',
                    'letterSpacing': '1px',
                    'marginBottom': '12px'
                }),
                dcc.Dropdown(
                    id='vaccine-filter',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Vaccinated', 'value': 1},
                        {'label': 'Not Vaccinated', 'value': 0}
                    ],
                    value='All',
                    style={
                        'borderRadius': '8px',
                        'border': '2px solid #e1e8ed',
                        'backgroundColor': '#ffffff',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                    }
                )
            ], style={'flex': '1', 'minWidth': '220px'}),
            
            html.Div([
                html.Label("HEALTH CONDITION", style={
                    'fontWeight': '700', 
                    'color': '#1e3c72', 
                    'fontSize': '0.9rem',
                    'textTransform': 'uppercase',
                    'letterSpacing': '1px',
                    'marginBottom': '12px'
                }),
                dcc.Dropdown(
                    id='health-filter',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Healthy', 'value': 0},
                        {'label': 'Health Issues', 'value': 1}
                    ],
                    value='All',
                    style={
                        'borderRadius': '8px',
                        'border': '2px solid #e1e8ed',
                        'backgroundColor': '#ffffff',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                    }
                )
            ], style={'flex': '1', 'minWidth': '220px'})
        ], style={
            'display': 'flex',
            'gap': '35px',
            'alignItems': 'flex-end',
            'padding': '35px',
            'backgroundColor': 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
            'borderBottom': '2px solid #1e3c72',
            'boxShadow': '0 4px 20px rgba(30, 60, 114, 0.15)',
            'borderRadius': '0 0 12px 12px'
        })
    ]),
    
    # Tabs
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='📊 Overview', value='overview', style={'fontWeight': '500'}),
            dcc.Tab(label='🏆 Adoption Rates', value='adoption-rates', style={'fontWeight': '500'}),
            dcc.Tab(label='📈 Trends', value='trends', style={'fontWeight': '500'}),
            dcc.Tab(label='🔍 Deep Analysis', value='deep-analysis', style={'fontWeight': '500'}),
            dcc.Tab(label='💡 Insights', value='insights', style={'fontWeight': '500'})
        ], id='tabs', style={'fontWeight': '500'})
    ], style={'background': 'white', 'padding': '0 30px', 'borderBottom': '1px solid #e1e8ed'}),
    
    # Tab content
    html.Div(id='tab-content', style={'padding': '30px', 'background': 'white'})
], style={
    'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    'minHeight': '100vh',
    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
})

# Callback function: update tab content with filters
@callback(Output('tab-content', 'children'), 
          [Input('tabs', 'value'),
           Input('pet-type-filter', 'value'),
           Input('age-filter', 'value'),
           Input('vaccine-filter', 'value'),
           Input('health-filter', 'value')])
def render_tab_content(selected_tab, pet_type, age_range, vaccine_status, health_condition):
    if selected_tab == 'overview':
        return render_overview_tab(pet_type, age_range, vaccine_status, health_condition)
    elif selected_tab == 'adoption-rates':
        return render_adoption_rates_tab(pet_type, age_range, vaccine_status, health_condition)
    elif selected_tab == 'trends':
        return render_trends_tab(pet_type, age_range, vaccine_status, health_condition)
    elif selected_tab == 'deep-analysis':
        return render_deep_analysis_tab(pet_type, age_range, vaccine_status, health_condition)
    elif selected_tab == 'insights':
        return render_insights_tab(pet_type, age_range, vaccine_status, health_condition)

# Overview tab - with filter functionality
def render_overview_tab(pet_type, age_range, vaccine_status, health_condition):
    # Apply filters to data
    filtered_df = apply_filters(df, pet_type, age_range, vaccine_status, health_condition)
    
    return html.Div([
        # Key metrics cards - now showing filtered data
        html.Div([
            html.Div([
                html.Div("🐾", style={'fontSize': '2rem', 'marginBottom': '15px'}),
                html.Div(f"{len(filtered_df):,}", style={'fontSize': '2.2rem', 'fontWeight': '600', 'margin': '10px 0'}),
                html.Div("Total Pets", style={'fontSize': '0.85rem', 'opacity': '0.8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'})
            ], style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'color': 'white',
                'padding': '25px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'boxShadow': '0 4px 15px rgba(102, 126, 234, 0.3)'
            }),
            
            html.Div([
                html.Div("❤️", style={'fontSize': '2rem', 'marginBottom': '15px'}),
                html.Div(f"{filtered_df['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontSize': '2.2rem', 'fontWeight': '600', 'margin': '10px 0'}),
                html.Div("Adoption Rate", style={'fontSize': '0.85rem', 'opacity': '0.8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'})
            ], style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'color': 'white',
                'padding': '25px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'boxShadow': '0 4px 15px rgba(102, 126, 234, 0.3)'
            }),
            
            html.Div([
                html.Div("💉", style={'fontSize': '2rem', 'marginBottom': '15px'}),
                html.Div(f"{filtered_df['Vaccinated'].mean()*100:.1f}%", style={'fontSize': '2.2rem', 'fontWeight': '600', 'margin': '10px 0'}),
                html.Div("Vaccination Rate", style={'fontSize': '0.85rem', 'opacity': '0.8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'})
            ], style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'color': 'white',
                'padding': '25px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'boxShadow': '0 4px 15px rgba(102, 126, 234, 0.3)'
            }),
            
            html.Div([
                html.Div("💰", style={'fontSize': '2rem', 'marginBottom': '15px'}),
                html.Div(f"${filtered_df['AdoptionFee'].mean():.0f}", style={'fontSize': '2.2rem', 'fontWeight': '600', 'margin': '10px 0'}),
                html.Div("Avg. Adoption Fee", style={'fontSize': '0.85rem', 'opacity': '0.8', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'})
            ], style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'color': 'white',
                'padding': '25px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'boxShadow': '0 4px 15px rgba(102, 126, 234, 0.3)'
            })
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        }),
        
        # Charts showing relationships between filter variables
        html.Div([
            # Pet Type vs Adoption Rate
            html.Div([
                html.Div([
                    html.Span("📊", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                    "Pet Type vs Adoption Rate"
                ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
                dcc.Graph(
                    id='pet-type-adoption-overview',
                    figure=create_pet_type_adoption_overview(filtered_df),
                    style={'height': '300px'},
                    config={'displayModeBar': False, 'staticPlot': True}
                )
            ], style={
                'background': 'white',
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
                'border': '1px solid #e1e8ed'
            }),
            
            # Vaccination vs Adoption Rate
            html.Div([
                html.Div([
                    html.Span("💉", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                    "Vaccination vs Adoption Rate"
                ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
                dcc.Graph(
                    id='vaccine-adoption-overview',
                    figure=create_vaccine_adoption_overview(filtered_df),
                    style={'height': '300px'},
                    config={'displayModeBar': False, 'staticPlot': True}
                )
            ], style={
                'background': 'white',
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
                'border': '1px solid #e1e8ed'
            }),
            
            # Health vs Adoption Rate
            html.Div([
                html.Div([
                    html.Span("🏥", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                    "Health vs Adoption Rate"
                ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
                dcc.Graph(
                    id='health-adoption-overview',
                    figure=create_health_adoption_overview(filtered_df),
                    style={'height': '300px'},
                    config={'displayModeBar': False, 'staticPlot': True}
                )
            ], style={
                'background': 'white',
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
                'border': '1px solid #e1e8ed',
                'gridColumn': '1 / -1'
            }),
            
            # Age vs Adoption Rate
            html.Div([
                html.Div([
                    html.Span("📈", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                    "Age vs Adoption Rate"
                ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
                dcc.Graph(
                    id='age-adoption-overview',
                    figure=create_age_adoption_overview(filtered_df),
                    style={'height': '300px'},
                    config={'displayModeBar': False, 'staticPlot': True}
                )
            ], style={
                'background': 'white',
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
                'border': '1px solid #e1e8ed'
            }),
            
            # Size vs Adoption Rate
            html.Div([
                html.Div([
                    html.Span("📏", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                    "Size vs Adoption Rate"
                ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
                dcc.Graph(
                    id='size-adoption-overview',
                    figure=create_size_adoption_overview(filtered_df),
                    style={'height': '300px'},
                    config={'displayModeBar': False, 'staticPlot': True}
                )
            ], style={
                'background': 'white',
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
                'border': '1px solid #e1e8ed'
            })
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))',
            'gap': '20px',
            'marginBottom': '25px'
        })
    ])

# Other tab functions (simplified)
def render_adoption_rates_tab(pet_type, age_range, vaccine_status, health_condition):
    filtered_df = apply_filters(df, pet_type, age_range, vaccine_status, health_condition)
    return html.Div([
        html.Div([
            html.Div([
                html.Span("🏆", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                "Adoption Rates by Pet Type"
            ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
            dcc.Graph(
                id='pet-type-adoption-rates',
                figure=create_pet_type_adoption_rates(filtered_df),
                style={'height': '350px'},
                config={'displayModeBar': False, 'staticPlot': True}
            )
        ], style={
            'background': 'white',
            'borderRadius': '8px',
            'padding': '20px',
            'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
            'border': '1px solid #e1e8ed',
            'gridColumn': '1 / -1'
        })
    ])

def render_trends_tab(pet_type, age_range, vaccine_status, health_condition):
    filtered_df = apply_filters(df, pet_type, age_range, vaccine_status, health_condition)
    return html.Div([
        html.Div([
            html.Div([
                html.Span("📈", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                "Age vs Adoption Rate Trend"
            ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
            dcc.Graph(
                id='age-adoption-trend',
                figure=create_age_adoption_trend(filtered_df),
                style={'height': '350px'},
                config={'displayModeBar': False, 'staticPlot': True}
            )
        ], style={
            'background': 'white',
            'borderRadius': '8px',
            'padding': '20px',
            'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
            'border': '1px solid #e1e8ed',
            'gridColumn': '1 / -1'
        })
    ])

def render_deep_analysis_tab(pet_type, age_range, vaccine_status, health_condition):
    filtered_df = apply_filters(df, pet_type, age_range, vaccine_status, health_condition)
    return html.Div([
        html.Div([
            html.Div([
                html.Span("🔬", style={'fontSize': '1.2rem', 'marginRight': '8px', 'color': '#1e3c72'}),
                "Vaccination & Health Interaction"
            ], style={'fontSize': '1rem', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '15px'}),
            dcc.Graph(
                id='vaccine-health-interaction',
                figure=create_vaccine_health_interaction(filtered_df),
                style={'height': '350px'},
                config={'displayModeBar': False, 'staticPlot': True}
            )
        ], style={
            'background': 'white',
            'borderRadius': '8px',
            'padding': '20px',
            'boxShadow': '0 1px 5px rgba(0,0,0,0.08)',
            'border': '1px solid #e1e8ed',
            'gridColumn': '1 / -1'
        })
    ])

def render_insights_tab(pet_type, age_range, vaccine_status, health_condition):
    filtered_df = apply_filters(df, pet_type, age_range, vaccine_status, health_condition)
    return html.Div([
        html.Div([
            html.Div([
                html.Span("💡", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                "Key Insights & Recommendations"
            ], style={'fontSize': '1.3rem', 'fontWeight': '600', 'marginBottom': '25px', 'textAlign': 'center'}),
            
            html.Div([
                html.Div([
                    html.Div("🏥 Vaccination Impact", style={'fontWeight': '600', 'marginBottom': '12px', 'fontSize': '1.1rem'}),
                    html.Div([
                        "Vaccinated pets have ",
                        html.Span(f"{filtered_df[filtered_df['Vaccinated']==1]['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold', 'color': '#667eea'}),
                        " higher adoption rate than non-vaccinated pets. Prioritize vaccination programs."
                    ], style={'opacity': '0.9', 'lineHeight': '1.6'})
                ], style={
                    'background': 'rgba(255, 255, 255, 0.15)',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'backdropFilter': 'blur(10px)'
                }),
                
                html.Div([
                    html.Div("🐕 Pet Type Preference", style={'fontWeight': '600', 'marginBottom': '12px', 'fontSize': '1.1rem'}),
                    html.Div([
                        "Dogs show highest adoption rate at ",
                        html.Span(f"{filtered_df[filtered_df['PetType']=='Dog']['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold', 'color': '#667eea'}),
                        ", while rabbits have lowest at ",
                        html.Span(f"{filtered_df[filtered_df['PetType']=='Rabbit']['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold', 'color': '#667eea'}),
                        "."
                    ], style={'opacity': '0.9', 'lineHeight': '1.6'})
                ], style={
                    'background': 'rgba(255, 255, 255, 0.15)',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'backdropFilter': 'blur(10px)'
                }),
                
                html.Div([
                    html.Div("📊 Age Factor", style={'fontWeight': '600', 'marginBottom': '12px', 'fontSize': '1.1rem'}),
                    html.Div([
                        "Young pets (under 1 year) have ",
                        html.Span(f"{(filtered_df[filtered_df['AgeYears']<1]['AdoptionLikelihood'].mean() - filtered_df[filtered_df['AgeYears']>7]['AdoptionLikelihood'].mean())*100:.1f}%", style={'fontWeight': 'bold', 'color': '#667eea'}),
                        " higher adoption rate than senior pets."
                    ], style={'opacity': '0.9', 'lineHeight': '1.6'})
                ], style={
                    'background': 'rgba(255, 255, 255, 0.15)',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'backdropFilter': 'blur(10px)'
                })
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
                'gap': '20px'
            })
        ], style={
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'color': 'white',
            'padding': '30px',
            'borderRadius': '16px',
            'marginTop': '30px'
        })
    ])

# Chart creation functions for Overview tab
def create_pet_type_adoption_overview(filtered_df):
    adoption_rates = filtered_df.groupby('PetType')['AdoptionLikelihood'].mean().sort_values(ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=adoption_rates.index,
        x=adoption_rates.values * 100,
        orientation='h',
        marker_color='#1e3c72',
        text=[f"{val*100:.1f}%" for val in adoption_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="Adoption Rate (%)",
        yaxis_title="Pet Type",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_vaccine_adoption_overview(filtered_df):
    vaccine_rates = filtered_df.groupby('Vaccinated')['AdoptionLikelihood'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Not Vaccinated', 'Vaccinated'],
        y=vaccine_rates.values * 100,
        marker_color=['#2a5298', '#1e3c72'],
        text=[f"{val*100:.1f}%" for val in vaccine_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="Vaccination Status",
        yaxis_title="Adoption Rate (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_health_adoption_overview(filtered_df):
    health_rates = filtered_df.groupby('HealthCondition')['AdoptionLikelihood'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Healthy', 'Health Issues'],
        y=health_rates.values * 100,
        marker_color=['#1e3c72', '#2a5298'],
        text=[f"{val*100:.1f}%" for val in health_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="Health Condition",
        yaxis_title="Adoption Rate (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_age_adoption_overview(filtered_df):
    # Create age groups
    age_bins = [0, 1, 3, 7, 15, 100]
    age_labels = ['0-1y', '1-3y', '3-7y', '7-15y', '15+y']
    filtered_df['AgeGroup2'] = pd.cut(filtered_df['AgeYears'], bins=age_bins, labels=age_labels)
    
    age_group_rates = filtered_df.groupby('AgeGroup2')['AdoptionLikelihood'].mean()
    
    fig = px.line(
        x=age_group_rates.index,
        y=age_group_rates.values * 100,
        title="",
        markers=True,
        color_discrete_sequence=['#1e3c72']
    )
    
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Adoption Rate (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_size_adoption_overview(filtered_df):
    size_rates = filtered_df.groupby('Size')['AdoptionLikelihood'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=size_rates.index,
        y=size_rates.values * 100,
        marker_color='#1e3c72',
        text=[f"{val*100:.1f}%" for val in size_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="Size",
        yaxis_title="Adoption Rate (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Chart creation functions for other tabs
def create_pet_type_adoption_rates(filtered_df):
    adoption_rates = filtered_df.groupby('PetType')['AdoptionLikelihood'].mean().sort_values(ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=adoption_rates.index,
        x=adoption_rates.values * 100,
        orientation='h',
        marker_color='#1e3c72',
        text=[f"{val*100:.1f}%" for val in adoption_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="Adoption Rate (%)",
        yaxis_title="Pet Type",
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_age_adoption_trend(filtered_df):
    age_bins = [0, 1, 3, 7, 15, 100]
    age_labels = ['0-1y', '1-3y', '3-7y', '7-15y', '15+y']
    filtered_df['AgeGroup2'] = pd.cut(filtered_df['AgeYears'], bins=age_bins, labels=age_labels)
    
    age_group_rates = filtered_df.groupby('AgeGroup2')['AdoptionLikelihood'].mean()
    
    fig = px.line(
        x=age_group_rates.index,
        y=age_group_rates.values * 100,
        title="",
        markers=True,
        color_discrete_sequence=['#1e3c72']
    )
    
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Adoption Rate (%)",
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_vaccine_health_interaction(filtered_df):
    cross_table = pd.pivot_table(
        filtered_df, 
        values='AdoptionLikelihood', 
        index='Vaccinated', 
        columns='HealthCondition',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        cross_table.values * 100,
        x=['Health Issues', 'Healthy'],
        y=['Not Vaccinated', 'Vaccinated'],
        title="",
        color_continuous_scale='Blues',
        aspect="auto"
    )
    
    fig.update_layout(
        xaxis_title="Health Condition",
        yaxis_title="Vaccination Status",
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add value labels
    for i in range(len(cross_table.index)):
        for j in range(len(cross_table.columns)):
            fig.add_annotation(
                x=j, y=i,
                text=f"{cross_table.iloc[i, j]*100:.1f}%",
                showarrow=False,
                font=dict(color="white", size=14)
            )
    
    return fig

if __name__ == '__main__':
    print("🚀 Starting Interactive Pet Adoption Analytics Dashboard...")
    print("📊 Data loaded successfully, total records:", len(df))
    print("🌐 Please visit: http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)
