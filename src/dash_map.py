from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go 



class Map:
    def __init__(self, data):
        self.data=data
    

    def render(self):
        fig = go.Figure()
        
        fig.add_trace(
            go.Scattermapbox(
                lat=[self.data["LATITUDE"].mean()],
                lon=[self.data["LONGITUDE"].mean()],
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
                    lat=self.data["LATITUDE"].mean(),
                    lon=self.data["LONGITUDE"].mean()
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
                                "mapbox.center.lon": self.data["LONGITUDE"].mean(),
                                "mapbox.center.lat": self.data["LATITUDE"].mean(),
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



        layout_map=dbc.Row([
            dcc.Graph(id="map-graph", figure=fig)], 
            style={"height":"80vh"}
            )
    
        
        return layout_map