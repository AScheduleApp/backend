import os
from typing import List

from fastapi import File, UploadFile
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from starlette.responses import JSONResponse


class SMPTEnvs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    MAILS_TO = os.getenv("MAILS_TO").split(",")
    MAIL_STARTTLS = bool(int(os.getenv("MAIL_STARTTLS")))
    MAIL_TLS = bool(int(os.getenv("MAIL_TLS")))
    MAIL_SSL = bool(int(os.getenv("MAIL_SSL")))
    USE_CREDENTIALS = bool(int(os.getenv("USE_CREDENTIALS")))


conf = ConnectionConfig(
    MAIL_USERNAME=SMPTEnvs.MAIL_USERNAME,
    MAIL_PASSWORD=SMPTEnvs.MAIL_PASSWORD,
    MAIL_FROM=SMPTEnvs.MAIL_FROM,
    MAIL_PORT=SMPTEnvs.MAIL_PORT,
    MAIL_SERVER=SMPTEnvs.MAIL_SERVER,
    MAIL_STARTTLS=SMPTEnvs.MAIL_STARTTLS,
    MAIL_TLS=SMPTEnvs.MAIL_TLS,
    MAIL_SSL=SMPTEnvs.MAIL_SSL,
    USE_CREDENTIALS=SMPTEnvs.USE_CREDENTIALS,
)


async def send_email_async(file: UploadFile = File(...)):
    message = MessageSchema(
        subject="Aktualizacja planu zajeć",
        recipients=SMPTEnvs.MAILS_TO,
        body="<p>Hej! Właśnie został zaktualizowany twój plan zajeć :)!<br>Plik w załączniku.</p>",
        subtype="html",
        attachments=[file],
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
