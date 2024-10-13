from sqlmodel import Session, select
from app.models.sensor_data import SensorData
from datetime import datetime

def get_sensor_data_range(session: Session, start: datetime, end: datetime):
    statement = select(SensorData).where(SensorData.timestamp.between(start, end))
    return session.exec(statement).all()

def get_all_sensor_data(session: Session):
    statement = select(SensorData)
    return session.exec(statement).all()

def get_sensor_data_by_id_range(session: Session, sensor_id: int, start: datetime, end: datetime):
    statement = select(SensorData).where(
        SensorData.sensor_id == sensor_id,
        SensorData.timestamp.between(start, end)
    )
    return session.exec(statement).all()

def get_all_sensor_data_by_id(session: Session, sensor_id: int):
    statement = select(SensorData).where(SensorData.sensor_id == sensor_id)
    return session.exec(statement).all()

def create_sensor_data(session: Session, sensor_data: SensorData):
    session.add(sensor_data)
    session.commit()
    session.refresh(sensor_data)
    return sensor_data