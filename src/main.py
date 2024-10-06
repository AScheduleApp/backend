from fastapi import Depends, FastAPI, File, UploadFile
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session

from src.dependencies import get_db

from . import crud, models, schemas
from .database import engine
from .email_config import SMPTEnvs, conf

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/schedule", response_model=schemas.Schedule)
async def schedule_create_or_update(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    obj, is_send_email = crud.create_or_update_schedule(db=db, file=file)

    if is_send_email:
        await file.seek(0)
        message = MessageSchema(
            subject="Aktualizacja planu zajęć - AŚ - Lekarski semestr 5",
            recipients=SMPTEnvs.MAILS_TO,
            body=SMPTEnvs.MESSAGE,
            subtype="html",
            attachments=[file],
        )
        fm = FastMail(conf)
        await fm.send_message(message)

    return obj


@app.post("/send", response_model=schemas.Email)
async def send_mails(email: schemas.Email):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.addresses.split(","),
        body=email.message,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return email.dict()