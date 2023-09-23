import pandas as pd

def load_data(path:str, filetype:str)->str:
    
    if filetype == ("csv"):
     df_fraude = pd.read_csv(path)
     return df_fraude