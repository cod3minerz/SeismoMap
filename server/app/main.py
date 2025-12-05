from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json

from .processing import process_three_stations

app = FastAPI(title="Seismo Localization API")

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],     
)


@app.post("/process_server_files")
async def process_server_files():
    files_paths = [
        "./sample_data/stationA.mseed",
        "./sample_data/stationB.mseed",
        "./sample_data/stationC.mseed",
    ]

    file_bytes = []
    for path in files_paths:
        with open(path, "rb") as f:
            file_bytes.append(f.read())

    stations = [
        {"name":"TIXI","lat":71.63,"lon":128.87,"elevation":40},
        {"name":"YAK","lat":62.03,"lon":129.68,"elevation":110},
        {"name":"MA2","lat":59.58,"lon":150.77,"elevation":337},
    ]

    result = process_three_stations(stations, file_bytes)
    return result
