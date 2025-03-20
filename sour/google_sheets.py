import requests
import csv
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()  

token = os.getenv('TOKEN_FOR_TABLE')
sheet_name= os.getenv('sheet_name')

def fetch_data(token: str, sheet_name: str) -> pd.DataFrame:
    google_sheets_link = "https://docs.google.com/spreadsheets/d/"

    load_path = google_sheets_link + token + '/export?format=xlsx'
    df = pd.read_excel(load_path, sheet_name=sheet_name)

    return df