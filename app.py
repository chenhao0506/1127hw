from dash import Dash, dcc, html, Input, Output, State, callback 
import plotly.express as px 
import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
app = Dash() 

app.layout = html.Div([
    html.H1("🌍 Gapminder 動態資料儀表板", style={'textAlign': 'center'}),

    dcc.Store(id='continent-filter-store', data=None),

    dcc.Slider(df['year'].min(),
               df['year'].max(),
               step=None,
               value=df['year'].min(),
               marks={str(year): str(year) for year in df['year'].unique()},
               id='year-slider'
               ),
    
    html.Div([
        html.Div([
            html.H3("散佈圖 (GDP vs 預期壽命)"),
            dcc.Graph(id='graph-with-slider')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            html.H3("旭日圖 (人口結構)"),
            dcc.Graph(id='sunburst-graph')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ])
])

# callback 1：讀取contenet狀態
@callback(
    Output('continent-filter-store', 'data'), 
    Input('sunburst-graph', 'clickData'),     
    State('continent-filter-store', 'data'), 
)
def toggle_continent_filter(clickData, current_selected_continent):
    if not clickData:
        return current_selected_continent

    clicked_label = clickData.get('points', [{}])[0].get('label')    

    if clicked_label == current_selected_continent:
        return None

    else:
        return clicked_label

# callback 2: 畫散佈圖
@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('continent-filter-store', 'data')
)
def update_figure(selected_year, selected_continent): 
    
    filtered_df = df[df.year == selected_year]
    plot_df = filtered_df.copy() 
    
    fig = px.scatter(plot_df,
                     x="gdpPercap",
                     y="lifeExp",
                     size="pop",
                     color="continent",
                     hover_name="country",
                     log_x=True,
                     size_max=55
                     )
    
    # 調整透明度
    if selected_continent:
        for trace in fig.data:
            if trace.name != selected_continent:
                trace.marker.opacity = 0.1 
            else:
                trace.marker.opacity = 1.0
    else:
        for trace in fig.data:
             trace.marker.opacity = 1.0
             
    title_text = f"年份: {selected_year}"
    if selected_continent:
        title_text += f" (已選: {selected_continent})"
        
    fig.update_layout(transition_duration=500, title=title_text)
    return fig

# callback 3: 旭日圖
@callback(
    Output('sunburst-graph', 'figure'),
    Input('year-slider', 'value'))
def update_sunburst_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    midpoint = np.average(filtered_df['lifeExp'], weights=filtered_df['pop'])
    fig = px.sunburst(
        filtered_df, 
        path=['continent', 'country'],
        values='pop', 
        color='lifeExp', 
        color_continuous_scale='RdBu', 
        color_continuous_midpoint=midpoint
    )
    
    fig.update_layout(title=f'人口結構與預期壽命 (年份: {selected_year})')
    
    return fig

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=False)