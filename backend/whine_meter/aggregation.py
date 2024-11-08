import dataclasses
import statistics
from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import select

from whine_meter import model
from whine_meter.core import db_session
from whine_meter.data import PartialUser


@dataclasses.dataclass
class WhinerData:
    username: str
    user_id: int
    whine_value: float
    date: datetime

    whine_count: float = dataclasses.field(init=False)

    def __post_init__(self):
        self.whine_count = (self.whine_value >= 0.25) + (self.whine_value >= 0.5) - 0.6 * (self.whine_value < 0.01)


def get_whining(chat_id: int, interval: timedelta = timedelta(days=1)) -> list[WhinerData]:
    query = (
        select(model.User.username, model.User.id, model.Message.whine_value, model.Message.created_at)
        .join(model.User)
        .where(model.Message.chat_id == chat_id)
        .where(model.Message.created_at > datetime.now() - interval)
    )

    with db_session() as session:
        values = [WhinerData(*x) for x in session.execute(query).fetchall()]
    return [v for v in values if v.whine_count]


def user_partition(data: list[WhinerData]) -> dict[str, list[WhinerData]]:
    messages = defaultdict(list)
    for w in data:
        messages[w.username].append(w)
    return messages


def daily_partition(data: list[WhinerData], blocksize: timedelta = timedelta(hours=1)) -> list[tuple[datetime, float]]:
    if not data:
        return []

    values = sorted(data, key=lambda s: s.date)
    # day: 06:00 morning - 06:00 next morning
    start_date = values[0].date  # .replace(hour=6, minute=0, second=0)
    end_date = values[-1].date
    i = 0
    output = []
    while start_date < end_date:
        next_date = start_date + blocksize
        current_count = 0
        while i < len(values) and values[i].date < next_date:
            current_count += values[i].whine_count
            i += 1
        output.append((start_date, max(0, current_count)))
        start_date = next_date

    return output


def daily_average(data: list[WhinerData]) -> float:
    daily_data = [x[1] for x in daily_partition(data)] or [0.0]
    return statistics.fmean(daily_data)


def max_whine_count(data: list[WhinerData]) -> float:
    daily_data = [value[1] for part in user_partition(data).values() for value in daily_partition(part)] or [0.0]
    return max(daily_data)


def get_users_data(chat_id: int):
    whining = get_whining(chat_id)
    if not whining:
        return [], {}

    output = {}
    mwc = max_whine_count(whining)
    messages = user_partition(whining)
    for user, msgs in messages.items():
        output[user] = daily_average(msgs) / mwc if mwc else 0

    return whining, output


def get_dates_data(chat_id: int):
    whining = get_whining(chat_id, timedelta(days=21))
    partition = daily_partition(whining)
    maxx = max(x[1] for x in partition)
    output = {x: y / maxx for x, y in partition}
    # some days might have had nothing, set them to 0
    min_day = min(output.keys())
    max_day = max(output.keys())
    while min_day < max_day:
        if min_day not in output:
            output[min_day] = 0
        min_day += timedelta(days=1)

    return output


def whine_of_the_week(chat_id: int) -> PartialUser | None:
    whining, d = get_users_data(chat_id)
    best_username = max([(v, k) for k, v in d.items()])[1] if d else None
    for w in whining:
        if w.username == best_username:
            return PartialUser(id=w.user_id, username=w.username)
    return None
