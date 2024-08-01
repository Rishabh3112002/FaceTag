import pandas as pd
import os

def make_txt(image_name, w, h, x0, y0, x1, y1):
  save_path = 'data/lables'
  if not os.path.exists(save_path):
    os.makedirs(save_path)
  cx = (x0+x1) / 2.0
  cy = (y0+y1) / 2.0
  box_width = x1 - x0
  box_height = y1 - y0

  cx /= w
  cy /= h
  box_width /= w
  box_height /= h
  label = f'0 {cx} {cy} {box_width} {box_height}'
  label_path = image_name.replace('.jpg', '.txt')
  with open(os.path.join(save_path, label_path), 'w') as f:
    f.write(label)

file_path = 'data/faces.csv'

data = pd.read_csv(file_path)

for i in range(len(data)):
  image_name = data.iloc[i]['image_name']
  w = data.iloc[i]['width']
  h = data.iloc[i]['height']
  x0 = data.iloc[i]['x0']
  y0 = data.iloc[i]['y0']
  x1 = data.iloc[i]['x1']
  y1 = data.iloc[i]['y1']
  make_txt(image_name, w, h, x0, y0, x1, y1)
