import pandas as pd
from datetime import datetime, timedelta


def fetch_data(token: str, sheet_name: str) -> pd.DataFrame:
    google_sheets_link = "https://docs.google.com/spreadsheets/d/"
    load_path = f"{google_sheets_link}{token}/export?format=xlsx"

    df = pd.read_excel(load_path, sheet_name=sheet_name)
    df['Дата'] = pd.to_datetime(df['Дата'], dayfirst=True)  
    return df


def get_tomorrow_lessons(df: pd.DataFrame) -> pd.DataFrame:
    """Фильтрует занятия, которые запланированы на будущее."""
    tomorrow = datetime.today().date() + timedelta(days=1)
    return df[df['Дата'].dt.date == tomorrow]


def get_ungraded_lessons(df: pd.DataFrame) -> pd.DataFrame:
    """Фильтрует занятия в прошлом без оценки."""
    today = datetime.today().date()
    return df[(df['Дата'].dt.date < today) & df['Оценка'].isna()]
