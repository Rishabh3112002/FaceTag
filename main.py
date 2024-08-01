import cv2
from ultralytics import YOLO
import torch
from src.detect_face import detect
from src.get_similarity import get_embeddings, compute_scores
import uuid
import json
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import requests

model = YOLO('./train_face_detection/runs/detect/train/weights/best.pt')

class Item(BaseModel):
  name: str
  image_url: str
  employee_id: str

app = FastAPI()

@app.get('/')
def test():
  return "pong"

@app.post('/create_entry')
def add_data(item: Item):
  try:
    with open('embeddings.json', 'r') as f:
       embeddings_data = json.load(f)
  except FileNotFoundError:
    embeddings_data = {}

  resp = requests.get(item.image_url)
  arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
  img = cv2.imdecode(arr, -1)
  face = detect(img)
  ori_emb = get_embeddings(face)
  embeddings_data[item.employee_id] = {
    'name': item.name,
    'emb': ori_emb.tolist()
    }

  with open('embeddings.json', 'w') as f:
    json.dump(embeddings_data, f, indent=4)


@app.get('/recognise')
def match_data(item: Item):
  try:
    with open('embeddings.json', 'r') as f:
       embeddings_data = json.load(f)
  except FileNotFoundError:
    embeddings_data = {}

  resp = requests.get(item.image_url)
  arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
  img = cv2.imdecode(arr, -1)
  face = detect(img)
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
  sorted_result = sorted(result, key=lambda x: x['similarity'])
  sorted_result.reverse()
  if sorted_result[0]['similarity'] > 0.90:
    return {
        "code": "success",
        "error": False,
        "message": "Successful",
        "data": sorted_result[0]
        }
  return {
      "code": "success",
      "error": False,
      "message": "Successful",
      "data": {}
      }


