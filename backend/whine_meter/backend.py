import contextlib
import os

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from whine_meter.core import EngineGlobal, database


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    EngineGlobal.setup(os.getenv("DB_URL"))
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
