from pydantic import BaseModel
from typing import List
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="deepAPI")

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

# Construct the DATABASE_URL
DATABASE_URL = f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD} host={DATABASE_HOST} port={DATABASE_PORT}"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Models for incoming requests
class CANMessage(BaseModel):
    message_id: int
    signal_name: str
    signal_value: float
    timestamp: datetime

class SensorData(BaseModel):
    sensor_id: int
    value: float
    timestamp: datetime 

class VideoMetadata(BaseModel):
    video_id: str
    start_timestamp: datetime
    end_timestamp: datetime
    file_path: str

# Route to get all can_messages within a timestamp range
@app.get("/can_messages/range", response_model=List[CANMessage])
def get_can_messages_range(start: datetime, end: datetime):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT message_id, signal_name, signal_value, timestamp FROM can_messages WHERE timestamp BETWEEN %s AND %s',
        (start, end)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [CANMessage(message_id=row[0], signal_name=row[1], signal_value=row[2], timestamp=row[3].isoformat()) for row in rows]

# Route to insert new can_message
@app.post("/can_messages")
def add_can_message(msg: CANMessage):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO can_messages (message_id, signal_name, signal_value, timestamp) VALUES (%s, %s, %s, %s)',
            (msg.message_id, msg.signal_name, msg.signal_value, msg.timestamp)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting can_message: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"status": "success"}

# Route to get all sensor_data within a timestamp range
@app.get("/sensor_data/range", response_model=List[SensorData])
def get_sensor_data_range(start: datetime, end: datetime):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT sensor_id, value, timestamp FROM sensor_data WHERE timestamp BETWEEN %s AND %s',
        (start, end)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [SensorData(sensor_id=row[0], value=row[1], timestamp=row[2].isoformat()) for row in rows]

# Route to insert new sensor_data
@app.post("/sensor_data")
def add_sensor_data(data: SensorData):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO sensor_data (sensor_id, value, timestamp) VALUES (%s, %s, %s)',
            (data.sensor_id, data.value, data.timestamp)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting sensor_data: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"status": "success"}

# Route to get all video_metadata within a timestamp range
@app.get("/video_metadata/range", response_model=List[VideoMetadata])
def get_video_metadata_range(start: datetime, end: datetime):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT video_id, start_timestamp, end_timestamp, file_path FROM video_metadata WHERE start_timestamp BETWEEN %s AND %s',
        (start, end)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [VideoMetadata(video_id=row[0], start_timestamp=row[1].isoformat(), end_timestamp=row[2].isoformat(), file_path=row[3]) for row in rows]

# Route to insert new video_metadata
@app.post("/video_metadata")
def add_video_metadata(metadata: VideoMetadata):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO video_metadata (video_id, start_timestamp, end_timestamp, file_path) VALUES (%s, %s, %s, %s)',
            (metadata.video_id, metadata.start_timestamp, metadata.end_timestamp, metadata.file_path)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting video_metadata: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"status": "success"}

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head>
            <title>deepAPI</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f4f7;
                    text-align: center;
                    padding-top: 50px;
                }
                h1 {
                    color: #333;
                    font-size: 3em;
                }
                p {
                    font-size: 1.2em;
                    color: #555;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-size: 1.2em;
                }
                a:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to deepAPI</h1>
            <p>Your data management API for the autonomous driving dataset</p>
            <a href="/docs">Go to API Documentation</a>
        </body>
    </html>
    """



# Running the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
