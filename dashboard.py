import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import json
import threading
import time
from collections import deque

# Global data storage (in memory)
data_store = {
    'timestamps': deque(maxlen=50),  # Keep last 50 points
    'temperatures': deque(maxlen=50),
    'humidity': deque(maxlen=50),
    'device_ids': deque(maxlen=50)
}

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("IoT Dashboard", style={'text-align': 'center'}),
    
    # Temperature Chart
    dcc.Graph(id='temperature-chart'),
    
    # Humidity Chart  
    dcc.Graph(id='humidity-chart'),
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every 1 second
        n_intervals=0
    )
])

# Callback for temperature chart
@app.callback(
    Output('temperature-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_temperature_chart(n):
    if len(data_store['timestamps']) == 0:
        return {'data': [], 'layout': {'title': 'Temperature Over Time'}}
    
    fig = go.Figure()
    
    # Convert timestamps to proper format
    timestamps = list(data_store['timestamps'])
    temperatures = list(data_store['temperatures'])
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=temperatures,
        mode='lines+markers',
        name='Temperature',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title='Temperature Over Time',
        xaxis_title='Time',
        yaxis_title='Temperature (C)',
        xaxis=dict(type='date')
    )
    
    return fig

# Callback for humidity chart
@app.callback(
    Output('humidity-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_humidity_chart(n):
    if len(data_store['timestamps']) == 0:
        return {'data': [], 'layout': {'title': 'Humidity Over Time'}}
    
    fig = go.Figure()
    
    timestamps = list(data_store['timestamps'])
    humidity = list(data_store['humidity'])
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=humidity,
        mode='lines+markers',
        name='Humidity',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title='Humidity Over Time',
        xaxis_title='Time',
        yaxis_title='Humidity (%)',
        xaxis=dict(type='date')
    )
    
    return fig

# Function to add data to store
def add_data_to_store(data):
    """Add new data point to the global store"""
    data_store['timestamps'].append(data['timestamp'])
    data_store['temperatures'].append(data['temperature'])
    data_store['humidity'].append(data['humidity'])
    data_store['device_ids'].append(data['device_id'])

if __name__ == '__main__':
    app.run(debug=True, port=8050)