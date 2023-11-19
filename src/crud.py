import hashlib

from fastapi import File, UploadFile
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session

from . import models
from .send_email import SMPTEnvs, conf


def get_last_schedule(db: Session):
    try:
        schedule = db.query(models.Schedule).first()
    except Exception:
        return None
    return schedule


def create_or_update_schedule(db: Session, file: UploadFile = File(...)):
    content_file = file.file.read()
    md5_hash = hashlib.md5(content_file).hexdigest()
    old_schedule = get_last_schedule(db)
    if not old_schedule:
        db_schedule = models.Schedule(md5_hash=md5_hash)
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        db.close()
        return db_schedule

    if old_schedule.md5_hash != md5_hash:
        old_schedule.md5_hash = md5_hash
        db.add(old_schedule)
        db.commit()
        db.refresh(old_schedule)
        db.close()

        file.file.seek(0)
        file.seek(0)

    message = MessageSchema(
        subject="Aktualizacja planu zajeć",
        recipients=SMPTEnvs.MAILS_TO,
        body="<p>Hej! Właśnie został zaktualizowany twój plan zajeć :)!<br>Plik w załączniku.</p>",
        subtype="html",
        attachments=[file],
    )
    fm = FastMail(conf)
    fm.send_message(message)

    return old_schedule
