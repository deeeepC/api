from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List
from datetime import datetime
from app.database import engine
from app.models.can_messages import CANMessage
from app.crud.can_messages import (
    get_can_messages_range,
    get_all_can_messages,
    get_can_messages_by_id_range,
    get_all_can_messages_by_id,
    create_can_message
)

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/range", response_model=List[CANMessage])
def read_can_messages_range(
    start: datetime = Query(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    end: datetime = Query(default_factory=datetime.now),
    session: Session = Depends(get_session)
):
    return get_can_messages_range(session, start, end)

@router.get("/all", response_model=List[CANMessage])
def read_all_can_messages(session: Session = Depends(get_session)):
    return get_all_can_messages(session)

@router.get("/message_id/{message_id}/range", response_model=List[CANMessage])
def read_can_messages_by_id_range(
    message_id: int,
    start: datetime = Query(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    end: datetime = Query(default_factory=datetime.now),
    session: Session = Depends(get_session)
):
    return get_can_messages_by_id_range(session, message_id, start, end)

@router.get("/message_id/{message_id}/all", response_model=List[CANMessage])
def read_all_can_messages_by_id(message_id: int, session: Session = Depends(get_session)):
    return get_all_can_messages_by_id(session, message_id)

@router.post("/", response_model=CANMessage)
def create_new_can_message(can_message: CANMessage, session: Session = Depends(get_session)):
    return create_can_message(session, can_message)