import os
import pandas as pd
from config import BASE_FOLDER
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def extract_base():
    df = pd.read_excel(BASE_FOLDER / "base_presos.xlsx", sheet_name="base_resume")
    return df
    
