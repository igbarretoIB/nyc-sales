from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from app import app
from src.dash_controllers import Controllers


def hex_to_rgba(hex_color, alpha=0):
    if hex_color.startswith('#'):
        hex_color = hex_color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        return f'rgba({r}, {g}, {b}, {alpha})'
    else:
        # já está no formato rgb ou rgba, apenas substitui a opacidade se possível
        return hex_color

def register_histogram_callbacks(df_data):
    @app.callback(
        Output("histo-graph", "figure"),
        [
            Input("borough-dropdown", 'value'),
            Input("square_feet-slider", 'value'),
            Input("variable-dropdown", 'value')
        ]
    )
    def update_histogram(location, square_m2, variable):
        if location is None:
            df_filtered = df_data.copy()
        else:
            df_filtered = df_data[df_data["BOROUGH"] == location] if location != 0 else df_data.copy()

        if square_m2 is not None:
            limit_size = Controllers.slider_size[square_m2]
            print(limit_size)
            df_filtered = df_filtered[df_filtered["GROSS SQUARE FEET"] <= limit_size]
            
        
        cmap_colors = px.colors.sequential.GnBu
        hist_color = hex_to_rgba(cmap_colors[0], alpha=0.5)  # primeira cor
        
        print(variable)
        if variable:
            fig = px.histogram(df_filtered, x=variable, opacity=0.75, color_discrete_sequence=['#1474b2']) #['#f7fcf0', '#d9f0d4', '#b4e2ba', '#7bccc4', '#42a6cc', '#1474b2', '#084081']
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=50),
                showlegend=False,
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)"
            )
        else:
            fig = go.Figure()
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)") 

        return fig
