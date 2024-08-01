import json
import os
import random
import shutil
import yaml


def __init__():
  global config
  global training_data_path
  global training_data_files
  global errors
  training_data_path = 'data/images'

  training_data_files = os.listdir(training_data_path)



def split_train_val():
  validation_percentage = 20
  train_percentage = 100 - validation_percentage;
  allowed_extensions_data = ["jpeg", "jpg", "png", "bmp"]
  data = []

  for file in training_data_files:
    extension = file.split('.')[-1]
    if extension in allowed_extensions_data:
      data.append(file)

  random.Random(42).shuffle(data)
  data_train = data[0: int((train_percentage*len(data))/100) - 1]
  data_val = data[int((train_percentage*len(data))/100) - 1:]

  dirs = [
      'data/dataset',
      os.path.join(os.getcwd(), 'data/dataset', 'images'),
      os.path.join(os.getcwd(), 'data/dataset', 'images', 'train'),
      os.path.join(os.getcwd(), 'data/dataset', 'images', 'val'),
      os.path.join(os.getcwd(), 'data/dataset', 'labels'),
      os.path.join(os.getcwd(), 'data/dataset', 'labels', 'train'),
      os.path.join(os.getcwd(), 'data/dataset', 'labels', 'val')
      ]

  for dir in dirs:
    os.makedirs(dir)

  for file in training_data_files:
    filename = ''.join(file.split('.')[0:-1])
    extension = file.split('.')[-1]

    _src = os.path.join(os.getcwd(), training_data_path)

    if file in data_train:
      src_data = os.path.join(_src, file)
      src_label = os.path.join(_src, filename + '.txt')
      dst_data = os.path.join(
          os.getcwd(), 'data/dataset', 'images', 'train', file)
      dst_label = os.path.join(
          os.getcwd(), 'data/dataset', 'labels', 'train', filename + '.txt')
      os.replace(src_data, dst_data)
      os.replace(src_label, dst_label)

    elif file in data_val:
      src_data = os.path.join(_src, file)
      src_label = os.path.join(_src, filename + '.txt')
      dst_data = os.path.join(
          os.getcwd(), 'data/dataset', 'images', 'val', file)
      dst_label = os.path.join(
          os.getcwd(), 'data/dataset', 'labels', 'val', filename + '.txt')
      os.replace(src_data, dst_data)
      os.replace(src_label, dst_label)

  os.replace(os.path.join(_src, 'labels.txt'),
             os.path.join('data/dataset', 'labels.txt'))
  return True


def prepare_config_file():

  with open(os.path.join('data/dataset', 'labels.txt'), 'r') as labels:
    label_content = labels.readlines()
    label_content = [lab.rstrip('\n') for lab in label_content]

    custom_config_content = {}
    custom_config_content['nc'] = len(label_content)
    custom_config_content['names'] = label_content;
    custom_config_content['train'] = os.path.join(
        os.getcwd(), 'data/dataset', 'images', 'train')
    custom_config_content['val'] = os.path.join(
        os.getcwd(), 'data/dataset', 'images', 'val')

    with open(os.path.join(os.getcwd(), 'custom_config.yaml'), 'w') as custom_config:
      yaml.dump(custom_config_content, custom_config)

  return True


try:
  __init__()
  # split_train_val()
  prepare_config_file()

except Exception as e:
  print(e)
