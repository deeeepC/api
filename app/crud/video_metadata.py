from sqlmodel import Session, select
from app.models.video_metadata import VideoMetadata
from datetime import datetime

def get_video_metadata_range(session: Session, start: datetime, end: datetime):
    statement = select(VideoMetadata).where(VideoMetadata.start_timestamp.between(start, end))
    return session.exec(statement).all()

def get_all_video_metadata(session: Session):
    statement = select(VideoMetadata)
    return session.exec(statement).all()

def get_video_metadata_by_id_range(session: Session, video_id: str, start: datetime, end: datetime):
    statement = select(VideoMetadata).where(
        VideoMetadata.video_id == video_id,
        VideoMetadata.start_timestamp.between(start, end)
    )
    return session.exec(statement).all()

def get_all_video_metadata_by_id(session: Session, video_id: str):
    statement = select(VideoMetadata).where(VideoMetadata.video_id == video_id)
    return session.exec(statement).all()

def create_video_metadata(session: Session, video_metadata: VideoMetadata):
    session.add(video_metadata)
    session.commit()
    session.refresh(video_metadata)
    return video_metadata