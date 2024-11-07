import contextlib
import os
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.params import Depends
from sqlalchemy import text, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from starlette.responses import Response

from whine_meter import model
from whine_meter.aggregation import get_users_data, get_dates_data
from whine_meter.core import EngineGlobal, database, db_session
from whine_meter.data import Chat, User, Message, GenericChatIDParams
from whine_meter.graph import generate_for_dates, generate_for_users
from whine_meter.ml import calculate_whine


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    EngineGlobal.setup(os.getenv("DB_URL"))
    EngineGlobal.make_databases()
    yield
    EngineGlobal.destroy()


app = FastAPI(lifespan=lifespan)


@app.get("/healthcheck")
async def healthcheck(session: Session = Depends(database)):
    try:
        session.execute(text("SELECT 1"))
        return {"healthy": True}
    except Exception as e:
        raise HTTPException(500, f"failed to connect to db: {e}") from e


@app.put("/chat")
def save_chat(chat: Chat, session: Session = Depends(database)):
    item = dict(
        id=chat.id, title=chat.title, type=chat.type, created_at=chat.created_at, updated_at=chat.updated_at
    )
    query = insert(model.Chat).values([item]).on_conflict_do_nothing()
    session.execute(query)
    session.commit()
    return {"success": True}


@app.put("/user")
def save_user(user: User, session: Session = Depends(database)):
    item = dict(
        id=user.id, created_at=user.created_at, updated_at=user.updated_at, role=user.role, username=user.username
    )
    query = insert(model.User).values([item]).on_conflict_do_nothing()
    session.execute(query)
    session.commit()
    return {"success": True}


async def compute_message_data(message: Message):
    value = await calculate_whine(message.text)
    if value is None:
        # cannot log this message :(
        return

    message_model = model.Message(
        id=message.id, chat_id=message.chat_id, user_id=message.user_id,
        whine_value=value, created_at=message.created_at, updated_at=message.updated_at
    )

    with db_session() as session:
        session.add(message_model)
        session.commit()


@app.put("/message")
# put into action pool because ML is slow
async def save_message(message: Message, pool: BackgroundTasks):
    pool.add_task(compute_message_data, message)
    return {"success": True}


@app.get("/whiner_otw")
def get_whiner_of_the_week(params: GenericChatIDParams = Depends(), session: Session = Depends(database)):
    # max(count(whine_value > 0.5))
    query = (
        select(model.User)
        .join(model.Message)
        .where(model.Message.whine_value > 0.5)
        .where(model.Message.chat_id == params.chat_id)
        .where(model.Message.created_at > datetime.now() - timedelta(days=7))
        .group_by(model.User.id)
        .order_by(text('count(messages) DESC'))
        .limit(1)
    )

    cursor = session.execute(query)
    item = cursor.scalar()
    if item is None:
        return None
    return User.from_model(item)


@app.get("/graph/dates")
def graph_dates(params: GenericChatIDParams = Depends()):
    graph_data = get_dates_data(params.chat_id)
    graph = generate_for_dates(graph_data)
    graph.seek(0)
    return Response(graph.getvalue(), headers={"Content-Type": "image/png"})


@app.get("/graph/users")
def graph_users(params: GenericChatIDParams = Depends()):
    graph_data = get_users_data(params.chat_id)
    graph = generate_for_users(graph_data)
    graph.seek(0)
    return Response(graph.getvalue(), headers={"Content-Type": "image/png"})
