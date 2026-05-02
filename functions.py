import pandas as pd
from config import BASE_FOLDER

def extract_base():
    df = pd.read_excel(BASE_FOLDER / "base_presos.xlsx")
    

    return df
    
