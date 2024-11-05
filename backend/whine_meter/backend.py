import contextlib
import os

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from whine_meter.core import EngineGlobal, database


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    EngineGlobal.setup(os.getenv("DB_URL"))
    yield
    EngineGlobal.destroy()


app = FastAPI(lifespan=lifespan)


@app.get("/healthcheck")
async def healthcheck():
    return {"healthy": True}


@app.get("/info")
async def get_info(db: Session = Depends(database)):
    return {"success": db.info}
