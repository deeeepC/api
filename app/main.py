from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api import can_messages, sensor_data, video_metadata
from app.database import create_db_and_tables

app = FastAPI(title="deepAPI")

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

app.include_router(can_messages.router, prefix="/can_messages", tags=["CAN Messages"])
app.include_router(sensor_data.router, prefix="/sensor_data", tags=["Sensor Data"])
app.include_router(video_metadata.router, prefix="/video_metadata", tags=["Video Metadata"])

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