import numpy as np
import torch
import torchvision
from PIL import Image
from torch import nn
from torchvision import transforms as tr
from torchvision import models
# from torchvision.models import vit_b_16
    
def emb_model():
    wt = torchvision.models.ResNet50_Weights.DEFAULT
    model = models.resnet50(pretrained=True)
    model = nn.Sequential(*list(model.children())[:-1])
    model.eval()
    model = model.to('cpu')
    return model

# def emb_model():
#     wt = torchvision.models.ViT_B_16_Weights.DEFAULT
#     model = vit_b_16(weights=wt)
#     model.heads = nn.Sequential(*list(model.heads.children())[:-1])
#     model = model.to('cpu')
#     return model

def process_test_image(img):
    transformations = tr.Compose([tr.ToTensor(),
                                    tr.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                    tr.Resize((512, 512))])
    img = transformations(img).float()
    img = img.unsqueeze_(0)
    
    img = img.to('cpu')

    return img

def get_embeddings(img):
    img1 = process_test_image(img)
    model = emb_model()

    emb = model(img1).detach().cpu()

    return emb

def compute_scores(emb_one, emb_two):
    # emb_one, emb_two = get_embeddings()
    scores = torch.nn.functional.cosine_similarity(emb_one, emb_two)

    return scores.numpy().tolist()
