import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import os
import webbrowser
import threading
import time

# 强制设置工作目录
os.chdir('/Users/apple/Desktop/python bootcamp')
print("🔧 强制设置工作目录为:", os.getcwd())

# 检查文件是否存在
data_file = "210 data/pet_adoption.csv"  # 注意文件名是pet_adoption.csv
print(f"📁 检查数据文件: {data_file}")
print(f"文件是否存在: {os.path.exists(data_file)}")

if os.path.exists(data_file):
    print(f"✅ 文件存在！文件大小: {os.path.getsize(data_file)} 字节")
else:
    print("❌ 文件不存在！")
    print("当前目录内容:")
    for item in os.listdir('.'):
        print(f"  - {item}")
    
    if os.path.exists('210 data'):
        print("210 data目录内容:")
        for item in os.listdir('210 data'):
            print(f"  - {item}")
    exit(1)  # 如果找不到数据文件就退出

# 读取数据
print("\n🚀 开始读取数据...")
try:
    # 使用绝对路径读取
    absolute_path = os.path.abspath(data_file)
    print(f"绝对路径: {absolute_path}")
    
    df = pd.read_csv(absolute_path)
    print(f"✅ 数据读取成功！")
    print(f"📊 数据形状: {df.shape}")
    print(f"📋 列名: {list(df.columns)}")
    print(f"🐕 前5行数据预览:")
    print(df.head())
    
except Exception as e:
    print(f"❌ 数据读取失败: {e}")
    print("🔧 无法读取数据，程序退出")
    exit(1)

# 数据验证
print(f"\n📊 数据验证:")
print(f"数据行数: {len(df)}")
print(f"数据列数: {len(df.columns)}")
print(f"AdoptionLikelihood分布:")
print(df['AdoptionLikelihood'].value_counts())
print(f"PetType分布:")
print(df['PetType'].value_counts())

# 创建Dash应用
print("\n🎨 创建Dash应用...")
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("🐾 宠物领养分析Dashboard (第3次尝试)", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # 数据状态显示
    html.Div([
        html.H3("📊 数据状态", style={'color': '#34495e'}),
        html.Div([
            html.P(f"✅ 数据加载成功！共 {len(df)} 条记录"),
            html.P(f"📋 数据列数: {len(df.columns)}"),
            html.P(f"🐕 宠物类型: {', '.join(df['PetType'].unique())}"),
            html.P(f"📅 年龄范围: {df['AgeMonths'].min()} - {df['AgeMonths'].max()} 月"),
            html.P(f"🎯 领养率: {(df['AdoptionLikelihood'].mean()*100):.1f}%")
        ], style={'backgroundColor': '#d4edda', 'padding': 15, 'borderRadius': 5, 'color': '#155724'})
    ], style={'marginBottom': 30}),
    
    # 过滤条件
    html.Div([
        html.H3("🔍 过滤条件", style={'color': '#34495e'}),
        html.Div([
            html.Div([
                html.Label("宠物类型:"),
                dcc.Dropdown(
                    id='pet-type-filter',
                    options=[{'label': '全部类型', 'value': 'all'}] + 
                            [{'label': pet_type, 'value': pet_type} for pet_type in df['PetType'].unique()],
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '25%', 'display': 'inline-block', 'marginRight': 20}),
            
            html.Div([
                html.Label("疫苗接种:"),
                dcc.Dropdown(
                    id='vaccinated-filter',
                    options=[
                        {'label': '全部', 'value': 'all'},
                        {'label': '✅ 已接种', 'value': 1},
                        {'label': '❌ 未接种', 'value': 0}
                    ],
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '25%', 'display': 'inline-block', 'marginRight': 20}),
            
            html.Div([
                html.Label("健康状况:"),
                dcc.Dropdown(
                    id='health-filter',
                    options=[
                        {'label': '全部', 'value': 'all'},
                        {'label': '🏥 健康', 'value': 0},
                        {'label': '🤒 有健康问题', 'value': 1}
                    ],
                    value='all',
                    style={'width': '100%'}
                )
            ], style={'width': '25%', 'display': 'marginRight': 20}),
            
            html.Div([
                html.Label("年龄范围 (月):"),
                dcc.RangeSlider(
                    id='age-filter',
                    min=int(df['AgeMonths'].min()),
                    max=int(df['AgeMonths'].max()),
                    step=1,
                    value=[int(df['AgeMonths'].min()), int(df['AgeMonths'].max())],
                    marks={int(df['AgeMonths'].min()): str(int(df['AgeMonths'].min())),
                             int(df['AgeMonths'].max()): str(int(df['AgeMonths'].max()))},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'width': '25%', 'display': 'inline-block'})
        ], style={'marginBottom': 20})
    ], style={'backgroundColor': '#f8f9fa', 'padding': 20, 'borderRadius': 5, 'marginBottom': 30}),
    
    # 图表区域 - 多种图表类型
    html.Div([
        html.H3("📈 多种图表类型分析", style={'color': '#34495e', 'marginBottom': 20}),
        
        # 第一行：条形图和散点图
        html.Div([
            html.Div([
                dcc.Graph(id='bar-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='scatter-chart')
            ], style={'width': '50%', 'display': 'inline-block'})
        ], style={'marginBottom': 30}),
        
        # 第二行：直方图和饼图
        html.Div([
            html.Div([
                dcc.Graph(id='histogram-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='pie-chart')
            ], style={'width': '50%', 'display': 'inline-block'})
        ], style={'marginBottom': 30}),
        
        # 第三行：箱线图和热力图
        html.Div([
            html.Div([
                dcc.Graph(id='boxplot-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='heatmap-chart')
            ], style={'width': '50%', 'display': 'inline-block'})
        ])
    ]),
    
    # 统计摘要
    html.Div([
        html.H3("📊 统计摘要", style={'color': '#34495e'}),
        html.Div(id='summary-stats', style={'backgroundColor': '#ecf0f1', 'padding': 15, 'borderRadius': 5})
    ], style={'marginTop': 30})
])

# 回调函数
@callback(
    [Output('bar-chart', 'figure'),
     Output('scatter-chart', 'figure'),
     Output('histogram-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('boxplot-chart', 'figure'),
     Output('heatmap-chart', 'figure'),
     Output('summary-stats', 'children')],
    [Input('pet-type-filter', 'value'),
     Input('vaccinated-filter', 'value'),
     Input('health-filter', 'value'),
     Input('age-filter', 'value')]
)
def update_charts(pet_type, vaccinated, health, age_range):
    # 应用过滤
    filtered_df = df.copy()
    
    if pet_type != 'all':
        filtered_df = filtered_df[filtered_df['PetType'] == pet_type]
    
    if vaccinated != 'all':
        filtered_df = filtered_df[filtered_df['Vaccinated'] == vaccinated]
    
    if health != 'all':
        filtered_df = filtered_df[filtered_df['HealthCondition'] == health]
    
    filtered_df = filtered_df[(filtered_df['AgeMonths'] >= age_range[0]) & 
                             (filtered_df['AgeMonths'] <= age_range[1])]
    
    # 1. 条形图 - 宠物类型领养率
    type_data = filtered_df.groupby('PetType')['AdoptionLikelihood'].agg(['mean', 'count']).reset_index()
    type_data['AdoptionRate'] = type_data['mean'] * 100
    
    fig1 = px.bar(type_data, x='PetType', y='AdoptionRate',
                   title='不同宠物类型的领养率 (条形图)',
                   labels={'AdoptionRate': '领养率 (%)', 'PetType': '宠物类型'},
                   color='AdoptionRate',
                   color_continuous_scale='viridis')
    fig1.update_layout(showlegend=False, height=400)
    
    # 2. 散点图 - 年龄vs收养费用，按领养状态着色
    fig2 = px.scatter(filtered_df, x='AgeMonths', y='AdoptionFee',
                       color='AdoptionLikelihood',
                       title='年龄 vs 收养费用 (散点图)',
                       labels={'AgeMonths': '年龄 (月)', 'AdoptionFee': '收养费用 ($)'},
                       color_discrete_map={0: '#e74c3c', 1: '#27ae60'},
                       opacity=0.7)
    fig2.update_layout(height=400)
    
    # 3. 直方图 - 年龄分布
    fig3 = px.histogram(filtered_df, x='AgeMonths', 
                        nbins=20,
                        title='宠物年龄分布 (直方图)',
                        labels={'AgeMonths': '年龄 (月)', 'count': '数量'},
                        color_discrete_sequence=['#3498db'])
    fig3.update_layout(height=400)
    
    # 4. 饼图 - 疫苗接种状态分布
    vacc_counts = filtered_df['Vaccinated'].value_counts()
    fig4 = px.pie(values=vacc_counts.values, 
                   names=vacc_counts.index.map({0: '未接种', 1: '已接种'}),
                   title='疫苗接种状态分布 (饼图)',
                   color_discrete_sequence=['#e74c3c', '#27ae60'])
    fig4.update_layout(height=400)
    
    # 5. 箱线图 - 不同宠物类型的年龄分布
    fig5 = px.box(filtered_df, x='PetType', y='AgeMonths',
                   title='不同宠物类型的年龄分布 (箱线图)',
                   labels={'PetType': '宠物类型', 'AgeMonths': '年龄 (月)'})
    fig5.update_layout(height=400)
    
    # 6. 热力图 - 相关性矩阵
    numeric_cols = ['AgeMonths', 'WeightKg', 'TimeInShelterDays', 'AdoptionFee', 'AdoptionLikelihood']
    correlation_matrix = filtered_df[numeric_cols].corr()
    
    fig6 = px.imshow(correlation_matrix,
                      title='数值变量相关性热力图',
                      color_continuous_scale='RdBu',
                      aspect='auto')
    fig6.update_layout(height=400)
    
    # 统计摘要
    total_pets = len(filtered_df)
    adopted_pets = filtered_df['AdoptionLikelihood'].sum()
    adoption_rate = (adopted_pets / total_pets * 100) if total_pets > 0 else 0
    avg_age = filtered_df['AgeMonths'].mean()
    vaccinated_pets = filtered_df['Vaccinated'].sum()
    vaccination_rate = (vaccinated_pets / total_pets * 100) if total_pets > 0 else 0
    healthy_pets = (filtered_df['HealthCondition'] == 0).sum()
    health_rate = (healthy_pets / total_pets * 100) if total_pets > 0 else 0
    avg_fee = filtered_df['AdoptionFee'].mean()
    
    summary_stats = html.Div([
        html.Div([
            html.H4(f"🐕 总宠物数量: {total_pets}"),
            html.H4(f"🏠 已领养数量: {adopted_pets}"),
            html.H4(f"📊 整体领养率: {adoption_rate:.1f}%"),
            html.H4(f"📅 平均年龄: {avg_age:.1f} 月"),
            html.H4(f"💉 疫苗接种率: {vaccination_rate:.1f}%"),
            html.H4(f"🏥 健康宠物比例: {health_rate:.1f}%"),
            html.H4(f"💰 平均收养费用: ${avg_fee:.1f}")
        ], style={'textAlign': 'center'})
    ])
    
    return fig1, fig2, fig3, fig4, fig5, fig6, summary_stats

# 自动打开浏览器的函数
def open_browser():
    time.sleep(2)  # 等待服务器启动
    webbrowser.open('http://127.0.0.1:8080/')
    print("🌐 浏览器已自动打开！")

# 启动应用
if __name__ == '__main__':
    print("🚀 启动宠物领养分析Dashboard (第3次尝试)...")
    print("📱 将在浏览器中自动打开: http://127.0.0.1:8080/")
    print("⏳ 正在启动服务器...")
    
    # 启动自动打开浏览器的线程
    threading.Thread(target=open_browser).start()
    
    try:
        # 使用端口8080
        app.run(debug=False, port=8080, host='127.0.0.1')
    except Exception as e:
        print(f"❌ 端口8080启动失败: {e}")
        print("🔄 尝试端口8081...")
        try:
            # 重新启动自动打开浏览器的线程
            threading.Thread(target=lambda: webbrowser.open('http://127.0.0.1:8081/')).start()
            app.run(debug=False, port=8081, host='127.0.0.1')
        except Exception as e2:
            print(f"❌ 端口8081也失败: {e2}")
            print("🔧 请检查端口是否被占用")
            print("💡 尝试手动在浏览器中打开: http://localhost:8080/ 或 http://localhost:8081/")
