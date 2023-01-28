import os
import requests
import torch
import numpy as np
from flask import current_app
from app.services.feature_extraction import extract_image
import base64


def save_image_base64(image_base64):
    imgdata = base64.b64decode(image_base64)
    image_file = os.path.join(
        current_app.config['QUERY_PATH'],
        "query_image.jpg")
    with open(image_file, 'wb') as f:
        f.write(imgdata)
    return image_file

def query_image(net, image):
    # save query image to disk
    image_file = save_image_base64(image)
    
    # extract q image vector
    qvecs = extract_image(
        net=net,
        images=[image_file]
    )

    # load dataset extracted features
    vecs = torch.load(current_app.config['FEATURE_PATH'])
    
    vecs = vecs.numpy()
    qvecs = qvecs.numpy()

    scores = np.dot(vecs.T, qvecs)
    ranks = np.argsort(-scores, axis=0)
    with open(current_app.config['IMAGEFILE_PATH'], 'r') as f:
        images = str(f.read()).split('\n')
    

    res = []

    num_images = current_app.config["NUM_IMAGE"]
    for i in ranks[:num_images]:
        image = images[i[0]]
        with open(image, "rb") as f:
            encoded_string= 'data:image/png;base64,'+\
                str(base64.b64encode(f.read())).replace("b'",'')[:-1]
            res.append(encoded_string)

    return res, requests.codes.ok
    