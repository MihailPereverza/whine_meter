from datetime import datetime, timedelta

from sqlalchemy import select, func

from whine_meter import model
from whine_meter.core import db_session


def get_users_data(chat_id: int):
    with db_session() as session:
        query = (
            select(model.User.username, func.avg(model.Message.whine_value))
            .group_by(model.User.username)
            .join(model.User)
            .where(model.Message.chat_id == chat_id)
        )

        return dict(session.execute(query).fetchall())


def get_dates_data(chat_id: int):
    return {datetime.now(): 0.8, datetime.now() - timedelta(days=1): 0.5}  # todo: select from db

