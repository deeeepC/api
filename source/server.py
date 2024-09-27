from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import os
import asyncpg
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# postgresql connection settings
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# collaborator credentials
COLLABORATOR_USER = os.getenv("COLLABORATOR_USER")
COLLABORATOR_PASSWORD = os.getenv("COLLABORATOR_PASSWORD")

app = FastAPI()

# websocket connection manager to handle multiple connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_text(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.on_event("startup")
async def startup():
    # create connection pool
    app.state.db_pool = await asyncpg.create_pool(
        host=DB_HOST,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD,
    )

@app.on_event("shutdown")
async def shutdown():
    # close connection pool
    await app.state.db_pool.close()

@app.get("/")
async def ping():
    return {"message": "websocket server is up and running."}

# websocket endpoint for rlog sensor data
@app.websocket("/ws/sensor")
async def websocket_sensor(websocket: WebSocket):
    await manager.connect(websocket)
    sensor_file_path = "sensor_data.rlog"

    # create sensor data log file if it does not exist
    if not os.path.exists(sensor_file_path):
        with open(sensor_file_path, "w") as f:
            f.write("Sensor Data Log (RLOG Format)\n")

    try:
        while True:
            # receive rlog formatted data (plain text)
            sensor_data = await websocket.receive_text()
            print(f"Received sensor data: {sensor_data}")

            # save rlog format data to .rlog file
            with open(sensor_file_path, "a") as f:
                f.write(sensor_data + "\n")

            # send acknowledgment back to the client
            await manager.send_text("Sensor data received and logged", websocket)

            # insert sensor data into the postgresql database
            async with app.state.db_pool.acquire() as connection:
                await connection.execute(
                    "INSERT INTO sensor_data (data) VALUES ($1)", sensor_data
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Sensor client disconnected")

# websocket endpoint for hevc video data
@app.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    await manager.connect(websocket)
    video_file_path = "received_video_stream.hevc"

    try:
        while True:
            # receive hevc video data in binary format (chunks)
            video_data = await websocket.receive_bytes()
            print(f"Received video chunk: {len(video_data)} bytes")

            # save hevc video data in chunks to file
            with open(video_file_path, "ab") as f:
                f.write(video_data)

            # send acknowledgment back to the client
            await websocket.send_text("Video chunk received")

            # insert metadata into the postgresql database if necessary
            async with app.state.db_pool.acquire() as connection:
                await connection.execute(
                    "INSERT INTO video_metadata (file_path, chunk_size) VALUES ($1, $2)",
                    video_file_path, len(video_data)
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Video client disconnected")

# run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)