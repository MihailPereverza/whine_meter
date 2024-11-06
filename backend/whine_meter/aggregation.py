from datetime import datetime, timedelta


def get_users_data(chat_id: int):
    return {"Студент": 0.8, "Менеджер программы": 0.1}  # todo: select from db


def get_dates_data(chat_id: int):
    return {datetime.now(): 0.8, datetime.now() - timedelta(days=1): 0.5}  # todo: select from db

