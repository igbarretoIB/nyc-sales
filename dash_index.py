from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.dash_preparedata import PrepareData
from src.dash_controllers import Controllers
from src.dash_histogram import Histogram
from src.dash_histogram_callbacks import register_histogram_callbacks
from src.dash_map_callbacks import register_map_callbacks
from src.dash_map import Map 
from app import app


# Prepare dataset
df_path= "/Dataleke/Gold/cleaned_data.csv"
PD = PrepareData(df_path)
df_data = PD.prepare_data()
# print(df_data.head(2))


# Prepare Map
mapa= Map(df_data)
map_layout = mapa.render()

# Registro dos callbacks separados
register_map_callbacks(df_data)

# Prepare Histogram
histo = Histogram(df_data)
histo_layout = histo.render()

# Registro dos callbacks separados
register_histogram_callbacks(df_data)


# Prepare Controllers
controllers = Controllers()
controllers_layout= controllers.render()

app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col([controllers_layout], md=3),
                dbc.Col([map_layout, histo_layout], md=9),
                html.Hr(),
                html.P("© Barreto's dashboard")
            ]
        )
    ],
    fluid=True,
)


if __name__ == '__main__':
    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

    #app.run_server(debug=True)
