import pandas as pd
import geopandas as gpd
import datetime 


class PrepareData:
    def __init__(self, df_path):
        self.df_path=df_path
        self.df_data= self.prepare_data() 
    
    def prepare_data(self):    
        df_data = pd.read_csv(self.df_path, index_col=0)
        df_data["size_m2"] = df_data["GROSS SQUARE FEET"]/10.764
        
        df_data=df_data[df_data["YEAR BUILT"]>0]
        df_data['SALE DATE'] = pd.to_datetime(df_data['SALE DATE']) 
        df_data.loc[df_data['size_m2']>10000, "size_m2"]=10000
        df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000
        df_data.loc[df_data["SALE PRICE"]< 10000,  "SALE PRICE"]=10000
        
    
        return df_data

    def set_coordxy(self, df_data):
        mean_lat= df_data["LATITUDE"].mean()
        mean_lon= df_data["LONGITUDE"].mean()
        return mean_lat, mean_lon
    
    def run(self):
        return 0
    