from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List
from datetime import datetime
from app.database import engine
from app.models.sensor_data import SensorData
from app.crud.sensor_data import (
    get_sensor_data_range,
    get_all_sensor_data,
    get_sensor_data_by_id_range,
    get_all_sensor_data_by_id,
    create_sensor_data
)

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/range", response_model=List[SensorData])
def read_sensor_data_range(
    start: datetime = Query(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    end: datetime = Query(default_factory=datetime.now),
    session: Session = Depends(get_session)
):
    return get_sensor_data_range(session, start, end)

@router.get("/all", response_model=List[SensorData])
def read_all_sensor_data(session: Session = Depends(get_session)):
    return get_all_sensor_data(session)

@router.get("/sensor_id/{sensor_id}/range", response_model=List[SensorData])
def read_sensor_data_by_id_range(
    sensor_id: int,
    start: datetime = Query(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    end: datetime = Query(default_factory=datetime.now),
    session: Session = Depends(get_session)
):
    return get_sensor_data_by_id_range(session, sensor_id, start, end)

@router.get("/sensor_id/{sensor_id}/all", response_model=List[SensorData])
def read_all_sensor_data_by_id(sensor_id: int, session: Session = Depends(get_session)):
    return get_all_sensor_data_by_id(session, sensor_id)

@router.post("/", response_model=SensorData)
def create_new_sensor_data(sensor_data: SensorData, session: Session = Depends(get_session)):
    return create_sensor_data(session, sensor_data)