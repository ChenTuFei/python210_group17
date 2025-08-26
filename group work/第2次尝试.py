import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import webbrowser
import threading

df = pd.read_csv("pet_adoption.csv")
age_min = int(df['AgeMonths'].min())
age_max = int(df['AgeMonths'].max())

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("宠物领养数据 Dashboard 第2次尝试"),
    html.Div([
        html.Div([
            html.H3("过滤条件"),
            dcc.Checklist(
                id='vaccinated-filter',
                options=[
                    {'label': '已打疫苗', 'value': 1},
                    {'label': '未打疫苗', 'value': 0}
                ],
                value=[1, 0],
                inline=True
            ),
            html.Br(),
            html.Label("年龄区间（单位：月）"),
            dcc.RangeSlider(
                id='age-slider',
                min=age_min,
                max=age_max,
                step=1,
                value=[age_min, age_max],
                marks={age_min: str(age_min), age_max: str(age_max)}
            ),
            html.Br(),
            html.Label("图表类型"),
            dcc.Dropdown(
                id='chart-type',
                options=[
                    {'label': '宠物类型', 'value': 'PetType'},
                    {'label': '颜色', 'value': 'Color'},
                    {'label': '品种', 'value': 'Breed'},
                    {'label': '体型', 'value': 'Size'}
                ],
                value='PetType'
            ),
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        html.Div([
            dcc.Graph(id='adoption-rate-chart'),
            html.Div(id='summary-info', style={'marginTop': '30px', 'fontSize': '18px'})
        ], style={'width': '70%', 'display': 'inline-block', 'padding': '20px'})
    ])
])

@app.callback(
    [Output('adoption-rate-chart', 'figure'),
     Output('summary-info', 'children')],
    [Input('vaccinated-filter', 'value'),
     Input('age-slider', 'value'),
     Input('chart-type', 'value')]
)
def update_dashboard(vaccinated, age_range, chart_type):
    # 数据过滤
    dff = df[df['Vaccinated'].isin(vaccinated)]
    dff = dff[(dff['AgeMonths'] >= age_range[0]) & (dff['AgeMonths'] <= age_range[1])]

    # 领养率统计
    adoption_rate = dff.groupby(chart_type)['AdoptionLikelihood'].mean().reset_index()
    adoption_rate['AdoptionLikelihood'] = adoption_rate['AdoptionLikelihood'] * 100

    fig = px.bar(adoption_rate, x=chart_type, y='AdoptionLikelihood',
                 title=f"不同{chart_type}下的领养率", text='AdoptionLikelihood',
                 labels={chart_type: chart_type, 'AdoptionLikelihood': '领养率 (%)'})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(yaxis_range=[0, 100])

    # summary
    avg_age = dff['AgeMonths'].mean()
    total = len(dff)
    adopted = dff['AdoptionLikelihood'].sum()
    adoption_percent = dff['AdoptionLikelihood'].mean() * 100 if total > 0 else 0

    summary = [
        html.P(f"筛选后宠物总数：{total}"),
        html.P(f"平均年龄：{avg_age:.2f} 月"),
        html.P(f"被领养率：{adoption_percent:.2f}%")
    ]

    return fig, summary

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8051")

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True, port=8051)
