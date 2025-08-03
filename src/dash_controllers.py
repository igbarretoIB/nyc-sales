from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app


class Controllers:
    slider_size = [250, 500, 1000, 10000, 100000, 10000000]
    borough_map = {
            "All": 0,
            "Bronx": 2,
            "Brooklyn": 3,  # Corrigido
            "Manhattan": 1,
            "Queens": 4,
            "Staten Island": 5
        }
    def __init__(self):
        self.logo = self.load_logo()
        self.dpbx_bairro = self.drop_box_bairros()
        self.dpbx_variaveis= self.drop_box_variaveis()
        self.slider_bar = self.slider()
        self.titles,  self.subtitles= self.load_text()
        self.slider_size = [100, 500, 1000, 10000, 100000, 10000000]
        self.borough_map = {
            "All": 0,
            "Bronx": 2,
            "Brooklyn": 3,  # Corrigido
            "Manhattan": 1,
            "Queens": 4,
            "Staten Island": 5
        }

    def drop_box_bairros(self):
        dpbox = dcc.Dropdown(
            id="borough-dropdown",
            options=[{"label": k, "value": v} for k, v in Controllers.borough_map.items()],
            value=0,
            #clearable=False,
            placeholder="Selecione um distrito",
        )
        return dpbox
    
    
    def drop_box_variaveis(self):
        variables_map = {
            "YEAR BUILT":"YEAR BUILT",
            "TOTAL UNITS":"TOTAL UNITS",
            "SALE PRICE":"SALE PRICE", 
        }
        
        dpbox = dcc.Dropdown(
            id="variable-dropdown",
            options=[{"label": k, "value": v} for k, v in variables_map.items()],
            value="SALE PRICE",
            #clearable=False,
            placeholder="Selecione uma variável",
        )
        return dpbox

    def slider(self):
        slider_bar = dcc.Slider(
            id="square_feet-slider",
            min=0,
            max=5,
            step=None,
            marks={i: str(j) for i, j in enumerate(Controllers.slider_size)},
            value=0,
            #tooltip={"placement": "bottom", "always_visible": True, "style":{"color": "#cccccc", "font-size": "10px"}}
        )
        return slider_bar

    def load_logo(self):
        logo = html.Img(
            id="logo",
            src=app.get_asset_url("logo.png"),  # Corrigido para uso correto da pasta assets
            style={"width": "85%",
                   "margin-top":"70px",
                   "margin-botton":"30px"
                   }
        )
        return logo
    
    def load_text(self):
        titles = {"titulo": html.H3("Vendas de imóveis - NYC", style={"margin-top":"40px", "fontWeight": "bold"}),
                 "dropbox_bairro": html.H4("Distrito", style={"margin-top":"40px", "fontWeight": "bold"}),
                 "dropbox_voi": html.H4("Variável de análise", style={"margin-top":"40px", "fontWeight": "bold"}),
                 "slider": html.H4("Área (m²)", style={"margin-top":"40px", "fontWeight": "bold"}) }
        
        
        subtitles={ "titulo": html.P("""Utilize esse Dashboard para analisar as vendas de imóveis ocorridas em Nova York dos anos de 2016 a 2017.""",
                      style={"fontSize": "12px"} ), 
                     "dropbox_bairro":  html.P("""Selecione um distrito.""",
                      style={"fontSize": "10px"} ),
                     "dropbox_voi":  html.P("""Selecione uma variável de interesse.""",
                      style={"fontSize": "10px"} ),
                     "slider":  html.P("""Selecione um valor de área""",
                      style={"fontSize": "10px"} ),
                }
        
        return titles,  subtitles
    

    def render(self):
        controllers = dbc.Row([
            self.logo,
            self.titles["titulo"], 
            self.subtitles["titulo"], 
            html.Hr(id="line-1", style={"margin-top":"10px"}),
            self.titles["dropbox_bairro"],
            self.subtitles["dropbox_bairro"],
            self.dpbx_bairro,
            self.titles["slider"],
            self.subtitles["slider"],
            self.slider_bar,
            self.titles["dropbox_voi"],
            self.subtitles["dropbox_voi"],
            self.dpbx_variaveis

            # dbc.Col(self.logo, width=4),
            # dbc.Col(self.dpbx, width=4),
            # dbc.Col(self.slider_bar, width=4)
        ])
        return controllers
