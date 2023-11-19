import hashlib
from typing import Annotated

from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from . import models
from .send_email import send_email_async


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
        send_email_async(file=file)
    return old_schedule
