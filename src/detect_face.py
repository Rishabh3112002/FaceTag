import cv2
from ultralytics import YOLO

def detect(image):
  model = YOLO("./train_face_detection/runs/detect/train/weights/best.pt")
  # try:
  res = model(image)
  if len(res[0].boxes.xyxy.tolist()) != 0:
    print(res[0].boxes.xyxy.tolist())
    x0, y0, x1, y1 = res[0].boxes.xyxy.tolist()[0]
    return image[int(y0):int(y1), int(x0):int(x1)]
  # except:
  #   return None
