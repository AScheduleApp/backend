from typing import Annotated

from fastapi import Depends, FastAPI, File, UploadFile
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session

from src.dependencies import get_db

from . import crud, models, schemas
from .database import engine
from .send_email import SMPTEnvs, conf

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/schedule", response_model=schemas.Schedule)
async def schedule_create_or_update(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    obj = crud.create_or_update_schedule(db=db, file=file)
    await file.seek(0)
    message = MessageSchema(
        subject="Aktualizacja planu zajeć",
        recipients=SMPTEnvs.MAILS_TO,
        body="<p>Hej! Właśnie został zaktualizowany twój plan zajeć :)!<br>Plik w załączniku.</p>",
        subtype="html",
        attachments=[file],
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return obj
