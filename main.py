import cv2
from ultralytics import YOLO
import torch
from src.detect_face import detect
from src.get_similarity import get_embeddings, compute_scores
import json
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid

# Initialize YOLO model
model = YOLO('./train_face_detection/runs/detect/train/weights/best.pt')

class Item(BaseModel):
    name: str
    employee_id: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def test():
    return "pong"

@app.post('/create_entry')
async def add_data(
    name: str = Form(...),
    age: int = Form(...),
    employee_id: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    try:
        with open('embeddings.json', 'r') as f:
            embeddings_data = json.load(f)
    except FileNotFoundError:
        embeddings_data = {}

    try:
        img = np.asarray(bytearray(await file.read()), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

    face = detect(img)

    if face is None or len(face) == 0:
        return {"code": "face-unavailable", "error": True, "message": "No Face Found"}
    
    ori_emb = get_embeddings(face)

    if not employee_id:
        employee_id = str(uuid.uuid4())

    embeddings_data[employee_id] = {
        'name': name,
        'age': age,
        'emb': ori_emb.tolist()
    }
    with open('embeddings.json', 'w') as f:
        json.dump(embeddings_data, f, indent=4)

    return {"code": "success", "error": False, "message": "Entry added successfully"}

@app.post('/recognise')
async def match_data(
    file: UploadFile = File(...),
    employee_id: Optional[str] = Form(None)
):
    try:
        with open('embeddings.json', 'r') as f:
            embeddings_data = json.load(f)
    except FileNotFoundError:
        embeddings_data = {}

    try:
        img = np.asarray(bytearray(await file.read()), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

    face = detect(img)
    if face is None or len(face) == 0:
        return {"code": "face-unavailable", "error": True, "message": "No Face Found"}
    
    emb = get_embeddings(face)
    result = []

    for uid, data in embeddings_data.items():
        ori_emb = np.array(data['emb'])
        ori_emb = torch.tensor(ori_emb)
        sim = compute_scores(ori_emb, emb)
        res = {
            'employee_id': uid,
            'name': data["name"],
            'similarity': sim[0][0][0]
        }
        result.append(res)

    sorted_result = sorted(result, key=lambda x: x['similarity'], reverse=True)

    if sorted_result and sorted_result[0]['similarity'] > 0.89:
        return {
            "code": "success",
            "error": False,
            "message": "Recognition successful",
            "data": sorted_result[0]
        }

    return {
        "code": "success",
        "error": False,
        "message": "No Data Found",
        "data": {}
    }
