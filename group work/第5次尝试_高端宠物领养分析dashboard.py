# -*- coding: utf-8 -*-
"""
高端宠物领养分析Dashboard
基于Plotly Dash创建的高端数据可视化界面
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 加载数据
df = pd.read_csv("pet_adoption.csv")

# 数据预处理
df['AgeYears'] = df['AgeMonths'] / 12
df['AgeGroup'] = pd.cut(df['AgeYears'], bins=[0, 1, 3, 7, 15, 100], 
                        labels=['幼年(0-1岁)', '青年(1-3岁)', '成年(3-7岁)', '中年(7-15岁)', '老年(15+岁)'])

# 创建Dash应用
app = dash.Dash(__name__, 
                external_stylesheets=[
                    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
                ])

# 自定义CSS样式
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>高端宠物领养分析Dashboard</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .dashboard-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                margin: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }
            .header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                position: relative;
                z-index: 1;
            }
            .header p {
                font-size: 1.1rem;
                opacity: 0.9;
                margin: 10px 0 0 0;
                position: relative;
                z-index: 1;
            }
            .controls {
                background: white;
                padding: 25px;
                border-bottom: 1px solid #e1e8ed;
                display: flex;
                gap: 20px;
                align-items: center;
                flex-wrap: wrap;
            }
            .control-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .control-group label {
                font-weight: 600;
                color: #2c3e50;
                font-size: 0.9rem;
            }
            .tabs {
                background: white;
                padding: 0 25px;
                border-bottom: 1px solid #e1e8ed;
            }
            .tab-content {
                padding: 30px;
                background: white;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                transition: transform 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-5px);
            }
            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 10px 0;
            }
            .metric-label {
                font-size: 0.9rem;
                opacity: 0.9;
            }
            .charts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 25px;
                margin-bottom: 30px;
            }
            .chart-container {
                background: white;
                border-radius: 16px;
                padding: 25px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border: 1px solid #e1e8ed;
            }
            .chart-title {
                font-size: 1.3rem;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .chart-title i {
                color: #667eea;
            }
            .full-width {
                grid-column: 1 / -1;
            }
            .insights-section {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 30px;
                border-radius: 16px;
                margin-top: 30px;
            }
            .insights-title {
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 20px;
                text-align: center;
            }
            .insights-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .insight-card {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
            }
            .insight-title {
                font-weight: 600;
                margin-bottom: 10px;
                font-size: 1.1rem;
            }
            .insight-text {
                opacity: 0.9;
                line-height: 1.6;
            }
            @media (max-width: 768px) {
                .controls {
                    flex-direction: column;
                    align-items: stretch;
                }
                .charts-grid {
                    grid-template-columns: 1fr;
                }
                .header h1 {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <div id="react-entry-point"></div>
    </body>
</html>
'''

# 应用布局
app.layout = html.Div([
    html.Div([
        # 头部
        html.Div([
            html.H1("🐾 高端宠物领养分析Dashboard"),
            html.P("深度分析宠物领养数据，发现关键影响因素")
        ], className="header"),
        
        # 控制面板
        html.Div([
            html.Div([
                html.Label("选择宠物类型"),
                dcc.Dropdown(
                    id='pet-type-filter',
                    options=[{'label': '全部类型', 'value': 'All'}] + 
                            [{'label': pet_type, 'value': pet_type} for pet_type in df['PetType'].unique()],
                    value='All',
                    style={'borderRadius': '8px', 'border': '1px solid #e1e8ed'}
                )
            ], className="control-group"),
            
            html.Div([
                html.Label("年龄范围 (岁)"),
                dcc.RangeSlider(
                    id='age-filter',
                    min=0,
                    max=20,
                    step=0.5,
                    value=[0, 20],
                    marks={i: f'{i}岁' for i in range(0, 21, 2)},
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    style={'marginTop': '10px'}
                )
            ], className="control-group"),
            
            html.Div([
                html.Label("疫苗接种状态"),
                dcc.Dropdown(
                    id='vaccine-filter',
                    options=[
                        {'label': '全部', 'value': 'All'},
                        {'label': '已接种', 'value': 1},
                        {'label': '未接种', 'value': 0}
                    ],
                    value='All',
                    style={'borderRadius': '8px', 'border': '1px solid #e1e8ed'}
                )
            ], className="control-group"),
            
            html.Div([
                html.Label("健康状况"),
                dcc.Dropdown(
                    id='health-filter',
                    options=[
                        {'label': '全部', 'value': 'All'},
                        {'label': '健康', 'value': 0},
                        {'label': '有健康问题', 'value': 1}
                    ],
                    value='All',
                    style={'borderRadius': '8px', 'border': '1px solid #e1e8ed'}
                )
            ], className="control-group")
        ], className="controls"),
        
        # 标签页
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='📊 概览', value='overview'),
                dcc.Tab(label='🏆 领养率分析', value='adoption-rates'),
                dcc.Tab(label='📈 趋势分析', value='trends'),
                dcc.Tab(label='🔍 深度分析', value='deep-analysis'),
                dcc.Tab(label='💡 洞察发现', value='insights')
            ], id='tabs', style={'fontWeight': '600'})
        ], className="tabs"),
        
        # 标签页内容
        html.Div(id='tab-content', className="tab-content")
    ], className="dashboard-container")
])

# 回调函数：更新标签页内容
@callback(Output('tab-content', 'children'), Input('tabs', 'value'))
def render_tab_content(selected_tab):
    if selected_tab == 'overview':
        return render_overview_tab()
    elif selected_tab == 'adoption-rates':
        return render_adoption_rates_tab()
    elif selected_tab == 'trends':
        return render_trends_tab()
    elif selected_tab == 'deep-analysis':
        return render_deep_analysis_tab()
    elif selected_tab == 'insights':
        return render_insights_tab()

# 概览标签页
def render_overview_tab():
    return html.Div([
        # 关键指标卡片
        html.Div([
            html.Div([
                html.I(className="fas fa-paw"),
                html.Div(f"{len(df):,}", className="metric-value"),
                html.Div("总宠物数量", className="metric-label")
            ], className="metric-card"),
            
            html.Div([
                html.I(className="fas fa-heart"),
                html.Div(f"{df['AdoptionLikelihood'].mean()*100:.1f}%", className="metric-value"),
                html.Div("整体领养率", className="metric-label")
            ], className="metric-card"),
            
            html.Div([
                html.I(className="fas fa-syringe"),
                html.Div(f"{df['Vaccinated'].mean()*100:.1f}%", className="metric-value"),
                html.Div("疫苗接种率", className="metric-label")
            ], className="metric-card"),
            
            html.Div([
                html.I(className="fas fa-dollar-sign"),
                html.Div(f"${df['AdoptionFee'].mean():.0f}", className="metric-value"),
                html.Div("平均领养费用", className="metric-label")
            ], className="metric-card")
        ], className="metrics-grid"),
        
        # 图表网格
        html.Div([
            # 宠物类型分布
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-pie"),
                    "宠物类型分布"
                ], className="chart-title"),
                dcc.Graph(
                    id='pet-type-distribution',
                    figure=create_pet_type_distribution(),
                    style={'height': '400px'}
                )
            ], className="chart-container"),
            
            # 年龄分布直方图
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-bar"),
                    "年龄分布直方图"
                ], className="chart-title"),
                dcc.Graph(
                    id='age-distribution',
                    figure=create_age_distribution(),
                    style={'height': '400px'}
                )
            ], className="chart-container"),
            
            # 领养率对比
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line"),
                    "各因素领养率对比"
                ], className="chart-title"),
                dcc.Graph(
                    id='adoption-comparison',
                    figure=create_adoption_comparison(),
                    style={'height': '400px'}
                )
            ], className="chart-container full-width"),
            
            # 体重与领养费用散点图
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-scatter"),
                    "体重与领养费用关系"
                ], className="chart-title"),
                dcc.Graph(
                    id='weight-fee-scatter',
                    figure=create_weight_fee_scatter(),
                    style={'height': '400px'}
                )
            ], className="chart-container"),
            
            # 收容所停留时间分析
            html.Div([
                html.Div([
                    html.I(className="fas fa-clock"),
                    "收容所停留时间分析"
                ], className="chart-title"),
                dcc.Graph(
                    id='shelter-time-analysis',
                    figure=create_shelter_time_analysis(),
                    style={'height': '400px'}
                )
            ], className="chart-container")
        ], className="charts-grid")
    ])

# 领养率分析标签页
def render_adoption_rates_tab():
    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-trophy"),
                "各宠物类型领养率"
            ], className="chart-title"),
            dcc.Graph(
                id='pet-type-adoption-rates',
                figure=create_pet_type_adoption_rates(),
                style={'height': '500px'}
            )
        ], className="chart-container full-width"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-palette"),
                "颜色对领养率的影响"
            ], className="chart-title"),
            dcc.Graph(
                id='color-adoption-rates',
                figure=create_color_adoption_rates(),
                style={'height': '400px'}
            )
        ], className="chart-container"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-dna"),
                "品种领养率分析"
            ], className="chart-title"),
            dcc.Graph(
                id='breed-adoption-rates',
                figure=create_breed_adoption_rates(),
                style={'height': '400px'}
            )
        ], className="chart-container")
    ], className="charts-grid")

# 趋势分析标签页
def render_trends_tab():
    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line"),
                "年龄与领养率趋势"
            ], className="chart-title"),
            dcc.Graph(
                id='age-adoption-trend',
                figure=create_age_adoption_trend(),
                style={'height': '500px'}
            )
        ], className="chart-container full-width"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-area"),
                "多因素交互分析"
            ], className="chart-title"),
            dcc.Graph(
                id='multi-factor-analysis',
                figure=create_multi_factor_analysis(),
                style={'height': '500px'}
            )
        ], className="chart-container full-width")
    ])

# 深度分析标签页
def render_deep_analysis_tab():
    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-microscope"),
                "疫苗接种与健康状况交互分析"
            ], className="chart-title"),
            dcc.Graph(
                id='vaccine-health-interaction',
                figure=create_vaccine_health_interaction(),
                style={'height': '500px'}
            )
        ], className="chart-container full-width"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-box"),
                "领养费用分布分析"
            ], className="chart-title"),
            dcc.Graph(
                id='adoption-fee-analysis',
                figure=create_adoption_fee_analysis(),
                style={'height': '400px'}
            )
        ], className="chart-container"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-scatter"),
                "体重与年龄关系分析"
            ], className="chart-title"),
            dcc.Graph(
                id='weight-age-analysis',
                figure=create_weight_age_analysis(),
                style={'height': '400px'}
            )
        ], className="chart-container")
    ], className="charts-grid")

# 洞察发现标签页
def render_insights_tab():
    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-lightbulb"),
                "关键洞察与实用建议"
            ], className="insights-title"),
            
            html.Div([
                html.Div([
                    html.Div("🏥 疫苗接种的重要性", className="insight-title"),
                    html.Div([
                        "已接种疫苗的宠物领养率比未接种的高出",
                        html.Span(f" {df[df['Vaccinated']==1]['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold'}),
                        "，建议收容所优先为宠物接种疫苗以提高领养成功率。"
                    ], className="insight-text")
                ], className="insight-card"),
                
                html.Div([
                    html.Div("🐕 宠物类型偏好", className="insight-title"),
                    html.Div([
                        "狗的领养率最高，达到",
                        html.Span(f" {df[df['PetType']=='Dog']['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold'}),
                        "，而兔子的领养率最低，仅为",
                        html.Span(f" {df[df['PetType']=='Rabbit']['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold'}),
                        "。"
                    ], className="insight-text")
                ], className="insight-card"),
                
                html.Div([
                    html.Div("🎨 颜色偏好分析", className="insight-title"),
                    html.Div([
                        "橙色宠物的领养率最高，达到",
                        html.Span(f" {df[df['Color']=='Orange']['AdoptionLikelihood'].mean()*100:.1f}%", style={'fontWeight': 'bold'}),
                        "，白色宠物的领养率最低，建议加强白色宠物的推广。"
                    ], className="insight-text")
                ], className="insight-card"),
                
                html.Div([
                    html.Div("📊 年龄因素影响", className="insight-title"),
                    html.Div([
                        "年轻宠物（1岁以下）的领养率比老年宠物高出",
                        html.Span(f" {(df[df['AgeYears']<1]['AdoptionLikelihood'].mean() - df[df['AgeYears']>7]['AdoptionLikelihood'].mean())*100:.1f}%", style={'fontWeight': 'bold'}),
                        "，建议为老年宠物制定特殊的推广策略。"
                    ], className="insight-text")
                ], className="insight-card")
            ], className="insights-grid")
        ], className="insights-section")
    ])

# 创建图表的函数
def create_pet_type_distribution():
    pet_counts = df['PetType'].value_counts()
    fig = px.pie(
        values=pet_counts.values,
        names=pet_counts.index,
        title="",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_age_distribution():
    fig = px.histogram(
        df, 
        x='AgeYears', 
        nbins=30,
        title="",
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        xaxis_title="年龄 (岁)",
        yaxis_title="数量",
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_adoption_comparison():
    # 计算各因素的领养率
    factors = {
        '疫苗接种': df.groupby('Vaccinated')['AdoptionLikelihood'].mean(),
        '健康状况': df.groupby('HealthCondition')['AdoptionLikelihood'].mean(),
        '体型': df.groupby('Size')['AdoptionLikelihood'].mean()
    }
    
    fig = go.Figure()
    
    for i, (factor_name, factor_data) in enumerate(factors.items()):
        fig.add_trace(go.Bar(
            name=factor_name,
            x=[f"{factor_name}-{idx}" for idx in factor_data.index],
            y=factor_data.values * 100,
            marker_color=px.colors.qualitative.Set3[i],
            text=[f"{val*100:.1f}%" for val in factor_data.values],
            textposition='auto'
        ))
    
    fig.update_layout(
        title="",
        xaxis_title="因素类别",
        yaxis_title="领养率 (%)",
        barmode='group',
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_weight_fee_scatter():
    fig = px.scatter(
        df.sample(n=500),  # 随机采样以避免过度拥挤
        x='WeightKg',
        y='AdoptionFee',
        color='PetType',
        title="",
        opacity=0.7
    )
    fig.update_layout(
        xaxis_title="体重 (kg)",
        yaxis_title="领养费用 ($)",
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_shelter_time_analysis():
    fig = px.box(
        df,
        x='PetType',
        y='TimeInShelterDays',
        title="",
        color='PetType'
    )
    fig.update_layout(
        xaxis_title="宠物类型",
        yaxis_title="收容所停留时间 (天)",
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_pet_type_adoption_rates():
    adoption_rates = df.groupby('PetType')['AdoptionLikelihood'].mean().sort_values(ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=adoption_rates.index,
        x=adoption_rates.values * 100,
        orientation='h',
        marker_color=px.colors.qualitative.Set3,
        text=[f"{val*100:.1f}%" for val in adoption_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="领养率 (%)",
        yaxis_title="宠物类型",
        margin=dict(t=0, b=0, l=0, r=0),
        height=500
    )
    return fig

def create_color_adoption_rates():
    color_rates = df.groupby('Color')['AdoptionLikelihood'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=color_rates.index,
        y=color_rates.values * 100,
        title="",
        color=color_rates.values * 100,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_title="颜色",
        yaxis_title="领养率 (%)",
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_breed_adoption_rates():
    breed_rates = df.groupby('Breed')['AdoptionLikelihood'].mean().sort_values(ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=breed_rates.index,
        x=breed_rates.values * 100,
        orientation='h',
        marker_color=px.colors.qualitative.Set3,
        text=[f"{val*100:.1f}%" for val in breed_rates.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="领养率 (%)",
        yaxis_title="品种",
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_age_adoption_trend():
    # 创建年龄组
    age_bins = [0, 1, 3, 7, 15, 100]
    age_labels = ['0-1岁', '1-3岁', '3-7岁', '7-15岁', '15+岁']
    df['AgeGroup2'] = pd.cut(df['AgeYears'], bins=age_bins, labels=age_labels)
    
    age_group_rates = df.groupby('AgeGroup2')['AdoptionLikelihood'].mean()
    
    fig = px.line(
        x=age_group_rates.index,
        y=age_group_rates.values * 100,
        title="",
        markers=True
    )
    
    fig.update_layout(
        xaxis_title="年龄组",
        yaxis_title="领养率 (%)",
        margin=dict(t=0, b=0, l=0, r=0),
        height=500
    )
    return fig

def create_multi_factor_analysis():
    # 创建交叉表
    cross_table = pd.pivot_table(
        df, 
        values='AdoptionLikelihood', 
        index='Vaccinated', 
        columns='HealthCondition',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        cross_table.values * 100,
        x=['有健康问题', '健康'],
        y=['未接种', '已接种'],
        title="",
        color_continuous_scale='viridis',
        aspect="auto"
    )
    
    fig.update_layout(
        xaxis_title="健康状况",
        yaxis_title="疫苗接种状态",
        margin=dict(t=0, b=0, l=0, r=0),
        height=500
    )
    
    # 添加数值标签
    for i in range(len(cross_table.index)):
        for j in range(len(cross_table.columns)):
            fig.add_annotation(
                x=j, y=i,
                text=f"{cross_table.iloc[i, j]*100:.1f}%",
                showarrow=False,
                font=dict(color="white", size=14)
            )
    
    return fig

def create_vaccine_health_interaction():
    # 创建3D散点图
    fig = px.scatter_3d(
        df.sample(n=300),
        x='AgeYears',
        y='WeightKg',
        z='AdoptionFee',
        color='AdoptionLikelihood',
        size='TimeInShelterDays',
        title="",
        opacity=0.7
    )
    
    fig.update_layout(
        scene=dict(
            xaxis_title="年龄 (岁)",
            yaxis_title="体重 (kg)",
            zaxis_title="领养费用 ($)"
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        height=500
    )
    return fig

def create_adoption_fee_analysis():
    fig = px.histogram(
        df,
        x='AdoptionFee',
        nbins=30,
        title="",
        color_discrete_sequence=['#f093fb']
    )
    
    fig.update_layout(
        xaxis_title="领养费用 ($)",
        yaxis_title="数量",
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

def create_weight_age_analysis():
    fig = px.scatter(
        df.sample(n=500),
        x='AgeYears',
        y='WeightKg',
        color='PetType',
        size='AdoptionLikelihood',
        title="",
        opacity=0.7
    )
    
    fig.update_layout(
        xaxis_title="年龄 (岁)",
        yaxis_title="体重 (kg)",
        margin=dict(t=0, b=0, l=0, r=0),
        height=400
    )
    return fig

if __name__ == '__main__':
    print("🚀 启动高端宠物领养分析Dashboard...")
    print("📊 数据加载完成，共", len(df), "条记录")
    print("🌐 请在浏览器中访问: http://127.0.0.1:8050")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
