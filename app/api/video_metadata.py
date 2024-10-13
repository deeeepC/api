from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List
from datetime import datetime
from app.database import engine
from app.models.video_metadata import VideoMetadata
from app.crud.video_metadata import (
    get_video_metadata_range,
    get_all_video_metadata,
    get_video_metadata_by_id_range,
    get_all_video_metadata_by_id,
    create_video_metadata
)

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/range", response_model=List[VideoMetadata])
def read_video_metadata_range(
    start: datetime = Query(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    end: datetime = Query(default_factory=datetime.now),
    session: Session = Depends(get_session)
):
    return get_video_metadata_range(session, start, end)

@router.get("/all", response_model=List[VideoMetadata])
def read_all_video_metadata(session: Session = Depends(get_session)):
    return get_all_video_metadata(session)

@router.get("/video_id/{video_id}/range", response_model=List[VideoMetadata])
def read_video_metadata_by_id_range(
    video_id: str,
    start: datetime = Query(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    end: datetime = Query(default_factory=datetime.now),
    session: Session = Depends(get_session)
):
    return get_video_metadata_by_id_range(session, video_id, start, end)

@router.get("/video_id/{video_id}/all", response_model=List[VideoMetadata])
def read_all_video_metadata_by_id(video_id: str, session: Session = Depends(get_session)):
    return get_all_video_metadata_by_id(session, video_id)

@router.post("/", response_model=VideoMetadata)
def create_new_video_metadata(video_metadata: VideoMetadata, session: Session = Depends(get_session)):
    return create_video_metadata(session, video_metadata)