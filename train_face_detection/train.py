from ultralytics import YOLO
import shutil
import os
import json

def train_model():

    # Hyperparameters for the model from config
    data = './custom_config.yaml'
    epochs = 51
    batch_size = 8
    imgsz = 640
    save_period = -1
    optimizer = "AdamW"
    device = 'mps'

    model = YOLO('./runs/detect/train/weights/last.pt')
    results = model.train(data=data, epochs=epochs, batch=batch_size, imgsz=imgsz, save_period=save_period, optimizer=optimizer, device=device, augment=False, resume=True)

    # results = model.val()


if __name__ == '__main__':
    train_model()
    print("Model training complete!")
