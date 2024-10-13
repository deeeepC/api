from sqlmodel import Session, select
from app.models.can_messages import CANMessage
from datetime import datetime

def get_can_messages_range(session: Session, start: datetime, end: datetime):
    statement = select(CANMessage).where(CANMessage.timestamp.between(start, end))
    return session.exec(statement).all()

def get_all_can_messages(session: Session):
    statement = select(CANMessage)
    return session.exec(statement).all()

def get_can_messages_by_id_range(session: Session, message_id: int, start: datetime, end: datetime):
    statement = select(CANMessage).where(
        CANMessage.message_id == message_id,
        CANMessage.timestamp.between(start, end)
    )
    return session.exec(statement).all()

def get_all_can_messages_by_id(session: Session, message_id: int):
    statement = select(CANMessage).where(CANMessage.message_id == message_id)
    return session.exec(statement).all()

def create_can_message(session: Session, can_message: CANMessage):
    session.add(can_message)
    session.commit()
    session.refresh(can_message)
    return can_message