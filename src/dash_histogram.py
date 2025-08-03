from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

class Histogram:
    def __init__(self, data):
        self.data = data

    def render(self):
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)")

        # O layout tem um Graph com ID fixo, para ser atualizado por callback
        layout = dbc.Row(
            [
                dcc.Graph(
                    id="histo-graph",
                    figure=fig,  # Inicial vazio
                    config={"displayModeBar": False},
                )
            ],
            style={"height": "20vh"}
        )
        return layout