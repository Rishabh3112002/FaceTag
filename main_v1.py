import cv2
from ultralytics import YOLO
import torch
from src.detect_face import detect
from src.get_similarity import get_embeddings, compute_scores
import uuid
import json
import numpy as np

model = YOLO('./train_face_detection/runs/detect/train/weights/best.pt')

def add_data():
  name = input('enter the name of the person: ')
  cap = cv2.VideoCapture(0)

  try:
    with open('embeddings.json', 'r') as f:
       embeddings_data = json.load(f)
  except FileNotFoundError:
    embeddings_data = {}

  while cap.isOpened():
    success, frame = cap.read()
    if success:
      cv2.imshow('Frame', frame)
      face = detect(frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Printing...')
        ori_emb = get_embeddings(face)
        uniq_no = str(uuid.uuid4())
        embeddings_data[uniq_no] = {
          'name': name,
          'emb': ori_emb.tolist()
          }
        break

  cap.release()
  cv2.destroyAllWindows()
  with open('embeddings.json', 'w') as f:
    json.dump(embeddings_data, f, indent=4)

def match_data():
  cap = cv2.VideoCapture(0)

  try:
    with open('embeddings.json', 'r') as f:
       embeddings_data = json.load(f)
  except FileNotFoundError:
    embeddings_data = {}

  while cap.isOpened():
    success, frame = cap.read()
    if success:
      cv2.imshow('Frame', frame)
      face = detect(frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Checking...')
        emb = get_embeddings(face)
        for uid, data in embeddings_data.items():
          ori_emb = np.array(data['emb'])
          ori_emb = torch.tensor(ori_emb)
          sim = compute_scores(ori_emb, emb)
          print(f'{data["name"]}: {sim}', sep='\n\n')
        break

  cap.release()
  cv2.destroyAllWindows()

# add_data()
match_data()
