import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
from app import app
from src.dash_controllers import Controllers
import numpy as np
import pandas as pd

def set_colorscale_from_quantiles(df, variable, cmap_colors):
    quantiles = np.linspace(0, 1, len(cmap_colors))
    values = df[variable].quantile(quantiles).values

    # Normalização para [0, 1] para o Scattermapbox
    vmin = df[variable].min()
    vmax = df[variable].max()
    norm = (values - vmin) / (vmax - vmin)

    # Gera o colorscale no formato [[val_normalizado, cor], ...]
    colorscale = [[float(n), color] for n, color in zip(norm, cmap_colors)]
    return colorscale, vmin, vmax


def register_map_callbacks(df_data):
    @app.callback(
        Output("map-graph", "figure"),
        [
            Input("borough-dropdown", 'value'),
            Input("square_feet-slider", 'value'),
            Input("variable-dropdown", 'value')
        ]
    )
    
    def update_map(location, square_m2, variable):
        df_filtered = df_data.copy()
        # Filtro por local
        if location is not None and location != 0:
            df_filtered = df_filtered[df_filtered["BOROUGH"] == location]

        # Filtro por tamanho
        if square_m2 is not None:
            limit_size = Controllers.slider_size[square_m2]
            df_filtered = df_filtered[df_filtered["GROSS SQUARE FEET"] <= limit_size]
        
        df_filtered["size_scaled"] =5+ 20*(
                (df_filtered["size_m2"] - df_filtered["size_m2"].min()) /
                (df_filtered["size_m2"].max() - df_filtered["size_m2"].min())
            )
        cmap_colors = px.colors.sequential.GnBu  # ou outro
        colorscale, vmin, vmax = set_colorscale_from_quantiles(df_filtered, variable, cmap_colors)
        
        fig = go.Figure()
        print(variable)    
        if variable is not None:
            fig.add_trace(
                go.Scattermapbox(
                    lat=df_filtered["LATITUDE"],
                    lon=df_filtered["LONGITUDE"],
                    mode="markers",
                    marker=go.scattermapbox.Marker(
                        size=df_filtered["size_scaled"],
                        sizemode="diameter",  #"area ou "diameter", dependendo do efeito desejado
                        sizemin=5,
                        color=df_filtered[variable],
                        colorscale=colorscale,
                        cmin=vmin,
                        cmax=vmax,
                        opacity=0.5,
                        showscale=True,
                        colorbar=dict(
                            title=dict(text=variable, font=dict(color="#d8d8d8")),
                            tickfont=dict(color="#d8d8d8"),
                            bgcolor="#111111"
                        ),
                    ),
                    text=df_filtered["BUILDING CLASS CATEGORY"],
                    hoverinfo="text+lat+lon",
                )
            )

            fig.update_layout(
                autosize=True,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                mapbox=dict(
                    style="carto-darkmatter",
                    center=dict(
                        lat=df_filtered["LATITUDE"].mean(),
                        lon=df_filtered["LONGITUDE"].mean()
                    ),
                    zoom=11,
                ),
                paper_bgcolor="rgba(0, 0, 0, 0)",
                template="plotly_dark",
                updatemenus=[
                    dict(
                        buttons=[
                            dict(
                                args=[{
                                    "mapbox.zoom": 15,
                                    "mapbox.center.lon": df_filtered["LONGITUDE"].mean(),
                                    "mapbox.center.lat": df_filtered["LATITUDE"].mean(),
                                    "mapbox.bearing": 0,
                                    "mapbox.style": "carto-darkmatter",
                                }],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ],
                        direction="left",
                        showactive=False,
                        type="buttons",
                        x=0.45,
                        y=0.02,
                        xanchor="left",
                        yanchor="bottom",
                        bgcolor="#323130",
                        borderwidth=1,
                        bordercolor="#6d6d6d",
                        font=dict(color="#FFFFFF"),
                    )
                ],
            )
            
        else:
            print("ASDF")
            # Mapa apenas com fundo escuro centralizado
            fig = go.Figure()
            fig.add_trace(
            go.Scattermapbox(
                lat=[df_filtered["LATITUDE"].mean()],
                lon=[df_filtered["LONGITUDE"].mean()],
                mode="markers",
                marker=go.scattermapbox.Marker(opacity=0.005, size=1, color="red"),
                text=[" "],
                hoverinfo="skip"
            )
        )

            # Layout apenas do mapa
            fig.update_layout(
                autosize=True,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                mapbox=dict(
                    style="carto-darkmatter",
                    center=dict(
                        lat=df_filtered["LATITUDE"].mean(),
                        lon=df_filtered["LONGITUDE"].mean()
                    ),
                    zoom=11,
                ),
                paper_bgcolor="rgba(0, 0, 0, 0)",
                template="plotly_dark",
                updatemenus=[
                    dict(
                        buttons=[
                            dict(
                                args=[{
                                    "mapbox.zoom": 15,
                                    "mapbox.center.lon": df_filtered ["LONGITUDE"].mean(),
                                    "mapbox.center.lat": df_filtered ["LATITUDE"].mean(),
                                    "mapbox.bearing": 0,
                                    "mapbox.style": "carto-darkmatter",
                                }],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ],
                        direction="left",
                        showactive=False,
                        type="buttons",
                        x=0.45,
                        y=0.02,
                        xanchor="left",
                        yanchor="bottom",
                        bgcolor="#323130",
                        borderwidth=1,
                        bordercolor="#6d6d6d",
                        font=dict(color="#FFFFFF"),
                    )
                ],
            )



        return fig
