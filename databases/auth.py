from sqlalchemy.orm import Session
from databases.auth_helper import getAuthStatusORM

from utils.enum import AuthHistoryType


def createLoginRecord(db: Session, id: int):
    dbAuthHistoryRecord = getAuthStatusORM(id, AuthHistoryType.SIGNEDIN)
    db.add(dbAuthHistoryRecord)
    db.commit()


def createLogoutRecord(db: Session, id: int):
    dbAuthHistoryRecord = getAuthStatusORM(id, AuthHistoryType.SIGNEDOUT)
    db.add(dbAuthHistoryRecord)
    db.commit()
