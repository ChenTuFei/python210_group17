# -*- coding: utf-8 -*-
"""
宠物领养分析高级Dashboard
基于Plotly Dash构建的专业级数据分析平台
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc

# 加载数据
df = pd.read_csv("pet_adoption.csv")

# 数据预处理
df['AgeYears'] = df['AgeMonths'] / 12
df['AgeGroup'] = pd.cut(df['AgeYears'], bins=[0, 1, 3, 7, 15, 100], 
                        labels=['幼年(0-1岁)', '青年(1-3岁)', '成年(3-7岁)', '中年(7-15岁)', '老年(15+岁)'])
df['Vaccinated_Text'] = df['Vaccinated'].map({1: '已接种', 0: '未接种'})
df['HealthCondition_Text'] = df['HealthCondition'].map({0: '健康', 1: '有健康问题'})
df['PreviousOwner_Text'] = df['PreviousOwner'].map({1: '有前主人', 0: '无前主人'})
df['AdoptionLikelihood_Text'] = df['AdoptionLikelihood'].map({1: '被领养', 0: '未被领养'})

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = "宠物领养分析高级Dashboard"

# 计算关键指标
total_pets = len(df)
adoption_rate = df['AdoptionLikelihood'].mean() * 100
avg_age = df['AgeYears'].mean()
avg_fee = df['AdoptionFee'].mean()
vaccination_rate = df['Vaccinated'].mean() * 100

# 创建指标卡片
def create_metric_card(title, value, unit="", color="primary"):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-muted"),
            html.H2(f"{value:.1f}{unit}", className=f"text-{color} fw-bold"),
        ]),
        className="text-center shadow-sm"
    )

# 创建主布局
app.layout = dbc.Container([
    # 标题区域
    dbc.Row([
        dbc.Col([
            html.H1("🐾 宠物领养分析高级Dashboard", 
                    className="text-center text-primary mb-3 fw-bold"),
            html.P("基于2009条宠物数据的深度分析与可视化平台", 
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # 关键指标行
    dbc.Row([
        dbc.Col(create_metric_card("总宠物数量", total_pets, "", "primary"), width=3),
        dbc.Col(create_metric_card("整体领养率", adoption_rate, "%", "success"), width=3),
        dbc.Col(create_metric_card("平均年龄", avg_age, "岁", "info"), width=3),
        dbc.Col(create_metric_card("平均领养费", avg_fee, "$", "warning"), width=3),
    ], className="mb-4"),
    
    # 过滤器行
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🔍 数据过滤器", className="bg-light"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("宠物类型", className="form-label"),
                            dcc.Dropdown(
                                id='pet-type-filter',
                                options=[{'label': '全部', 'value': 'all'}] + 
                                       [{'label': x, 'value': x} for x in df['PetType'].unique()],
                                value='all',
                                clearable=False
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("年龄组", className="form-label"),
                            dcc.Dropdown(
                                id='age-group-filter',
                                options=[{'label': '全部', 'value': 'all'}] + 
                                       [{'label': x, 'value': x} for x in df['AgeGroup'].unique()],
                                value='all',
                                clearable=False
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("疫苗接种状态", className="form-label"),
                            dcc.Dropdown(
                                id='vaccinated-filter',
                                options=[{'label': '全部', 'value': 'all'}] + 
                                       [{'label': '已接种', 'value': 1}, {'label': '未接种', 'value': 0}],
                                value='all',
                                clearable=False
                            )
                        ], width=3),
                        dbc.Col([
                            html.Label("健康状态", className="form-label"),
                            dcc.Dropdown(
                                id='health-filter',
                                options=[{'label': '全部', 'value': 'all'}] + 
                                       [{'label': '健康', 'value': 0}, {'label': '有健康问题', 'value': 1}],
                                value='all',
                                clearable=False
                            )
                        ], width=3),
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # 主要图表区域
    dbc.Row([
        # 左侧：领养率分析
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 领养率分析", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='adoption-rate-chart', style={'height': '400px'})
                ])
            ])
        ], width=6),
        
        # 右侧：年龄分布
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 年龄分布与领养关系", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='age-distribution-chart', style={'height': '400px'})
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # 第二行图表
    dbc.Row([
        # 左侧：疫苗接种影响
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💉 疫苗接种对领养的影响", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='vaccination-impact-chart', style={'height': '350px'})
                ])
            ])
        ], width=6),
        
        # 右侧：健康状态影响
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🏥 健康状态对领养的影响", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='health-impact-chart', style={'height': '350px'})
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # 第三行图表
    dbc.Row([
        # 左侧：品种分析
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🐕 品种领养率分析", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='breed-analysis-chart', style={'height': '400px'})
                ])
            ])
        ], width=6),
        
        # 右侧：颜色分析
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🎨 颜色对领养的影响", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='color-analysis-chart', style={'height': '400px'})
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # 第四行：高级分析
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🔬 多因素交互分析", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='interaction-analysis-chart', style={'height': '500px'})
                ])
            ])
        ])
    ], className="mb-4"),
    
    # 第五行：领养费分析
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💰 领养费分析", className="bg-light"),
                dbc.CardBody([
                    dcc.Graph(id='fee-analysis-chart', style={'height': '400px'})
                ])
            ])
        ])
    ], className="mb-4"),
    
    # 底部：数据表格
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📋 详细数据表格", className="bg-light"),
                dbc.CardBody([
                    html.Div(id='data-table-container')
                ])
            ])
        ])
    ]),
    
    # 页脚
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("🕐 最后更新时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                   className="text-center text-muted")
        ])
    ])
    
], fluid=True, className="py-4")

# 回调函数：过滤数据
@callback(
    Output('adoption-rate-chart', 'figure'),
    Output('age-distribution-chart', 'figure'),
    Output('vaccination-impact-chart', 'figure'),
    Output('health-impact-chart', 'figure'),
    Output('breed-analysis-chart', 'figure'),
    Output('color-analysis-chart', 'figure'),
    Output('interaction-analysis-chart', 'figure'),
    Output('fee-analysis-chart', 'figure'),
    Output('data-table-container', 'children'),
    [Input('pet-type-filter', 'value'),
     Input('age-group-filter', 'value'),
     Input('vaccinated-filter', 'value'),
     Input('health-filter', 'value')]
)
def update_charts(pet_type, age_group, vaccinated, health):
    # 应用过滤器
    filtered_df = df.copy()
    
    if pet_type != 'all':
        filtered_df = filtered_df[filtered_df['PetType'] == pet_type]
    if age_group != 'all':
        filtered_df = filtered_df[filtered_df['AgeGroup'] == age_group]
    if vaccinated != 'all':
        filtered_df = filtered_df[filtered_df['Vaccinated'] == vaccinated]
    if health != 'all':
        filtered_df = filtered_df[filtered_df['HealthCondition'] == health]
    
    # 1. 领养率分析图表
    adoption_by_type = filtered_df.groupby('PetType')['AdoptionLikelihood'].agg(['mean', 'count']).reset_index()
    adoption_by_type['mean'] = adoption_by_type['mean'] * 100
    
    adoption_rate_fig = px.bar(
        adoption_by_type, x='PetType', y='mean',
        title="各宠物类型领养率",
        labels={'mean': '领养率 (%)', 'PetType': '宠物类型'},
        color='mean',
        color_continuous_scale='viridis',
        text='mean'
    )
    adoption_rate_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    adoption_rate_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    
    # 2. 年龄分布图表
    age_dist_fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('年龄分布', '年龄与领养率关系'),
        vertical_spacing=0.1
    )
    
    # 年龄分布直方图
    age_dist_fig.add_trace(
        go.Histogram(x=filtered_df['AgeYears'], nbinsx=20, name='年龄分布'),
        row=1, col=1
    )
    
    # 年龄与领养率关系
    age_bins = pd.cut(filtered_df['AgeYears'], bins=10)
    age_adoption = filtered_df.groupby(age_bins)['AdoptionLikelihood'].mean()
    age_dist_fig.add_trace(
        go.Scatter(x=[i.mid for i in age_adoption.index], 
                  y=age_adoption.values * 100,
                  mode='lines+markers', name='领养率'),
        row=2, col=1
    )
    
    age_dist_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    # 3. 疫苗接种影响图表
    vacc_impact = filtered_df.groupby('Vaccinated_Text')['AdoptionLikelihood'].agg(['mean', 'count']).reset_index()
    vacc_impact['mean'] = vacc_impact['mean'] * 100
    
    vacc_fig = px.bar(
        vacc_impact, x='Vaccinated_Text', y='mean',
        title="疫苗接种状态对领养的影响",
        labels={'mean': '领养率 (%)', 'Vaccinated_Text': '疫苗接种状态'},
        color='mean',
        color_continuous_scale='RdYlGn',
        text='mean'
    )
    vacc_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    vacc_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    
    # 4. 健康状态影响图表
    health_impact = filtered_df.groupby('HealthCondition_Text')['AdoptionLikelihood'].agg(['mean', 'count']).reset_index()
    health_impact['mean'] = health_impact['mean'] * 100
    
    health_fig = px.bar(
        health_impact, x='HealthCondition_Text', y='mean',
        title="健康状态对领养的影响",
        labels={'mean': '领养率 (%)', 'HealthCondition_Text': '健康状态'},
        color='mean',
        color_continuous_scale='RdYlGn',
        text='mean'
    )
    health_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    health_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    
    # 5. 品种分析图表
    breed_analysis = filtered_df.groupby('Breed')['AdoptionLikelihood'].agg(['mean', 'count']).reset_index()
    breed_analysis['mean'] = breed_analysis['mean'] * 100
    breed_analysis = breed_analysis.sort_values('mean', ascending=True)
    
    breed_fig = px.bar(
        breed_analysis, y='Breed', x='mean',
        title="各品种领养率分析",
        labels={'mean': '领养率 (%)', 'Breed': '品种'},
        color='mean',
        color_continuous_scale='plasma',
        orientation='h'
    )
    breed_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
        height=400
    )
    
    # 6. 颜色分析图表
    color_analysis = filtered_df.groupby('Color')['AdoptionLikelihood'].agg(['mean', 'count']).reset_index()
    color_analysis['mean'] = color_analysis['mean'] * 100
    
    color_fig = px.bar(
        color_analysis, x='Color', y='mean',
        title="颜色对领养的影响",
        labels={'mean': '领养率 (%)', 'Color': '颜色'},
        color='mean',
        color_continuous_scale='viridis',
        text='mean'
    )
    color_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    color_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    
    # 7. 多因素交互分析
    interaction_data = filtered_df.groupby(['PetType', 'Vaccinated_Text'])['AdoptionLikelihood'].mean().reset_index()
    interaction_data['AdoptionLikelihood'] = interaction_data['AdoptionLikelihood'] * 100
    
    interaction_fig = px.bar(
        interaction_data, x='PetType', y='AdoptionLikelihood',
        color='Vaccinated_Text',
        title="宠物类型与疫苗接种状态的交互影响",
        labels={'AdoptionLikelihood': '领养率 (%)', 'PetType': '宠物类型', 'Vaccinated_Text': '疫苗接种状态'},
        barmode='group'
    )
    interaction_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    
    # 8. 领养费分析
    fee_fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('领养费分布', '领养费与领养率关系'),
        specs=[[{"type": "histogram"}, {"type": "scatter"}]]
    )
    
    # 领养费分布
    fee_fig.add_trace(
        go.Histogram(x=filtered_df['AdoptionFee'], nbinsx=20, name='领养费分布'),
        row=1, col=1
    )
    
    # 领养费与领养率关系
    fee_bins = pd.cut(filtered_df['AdoptionFee'], bins=10)
    fee_adoption = filtered_df.groupby(fee_bins)['AdoptionLikelihood'].mean()
    fee_fig.add_trace(
        go.Scatter(x=[i.mid for i in fee_adoption.index], 
                  y=fee_adoption.values * 100,
                  mode='lines+markers', name='领养率'),
        row=1, col=2
    )
    
    fee_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    
    # 9. 数据表格
    table_data = filtered_df.head(20)[['PetType', 'Breed', 'AgeYears', 'Color', 'Size', 
                                       'Vaccinated_Text', 'HealthCondition_Text', 'AdoptionFee', 'AdoptionLikelihood_Text']]
    
    table = dbc.Table.from_dataframe(
        table_data, 
        striped=True, 
        bordered=True, 
        hover=True,
        className="table-sm"
    )
    
    return (adoption_rate_fig, age_dist_fig, vacc_fig, health_fig, 
            breed_fig, color_fig, interaction_fig, fee_fig, table)

if __name__ == '__main__':
    print("🚀 启动宠物领养分析高级Dashboard...")
    print("📊 数据加载完成，共", len(df), "条记录")
    print("🌐 正在启动服务器，请稍候...")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
