from typing import Annotated

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session

from src.dependencies import get_db

from . import crud, models, schemas
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/schedule", response_model=schemas.Schedule)
async def schedule_create_or_update(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    return crud.create_or_update_schedule(db=db, file=file)
