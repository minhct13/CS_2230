import os
import torch
import torch.nn as nn

from torchvision import transforms
import pickle as p

from app.utils.datasets import ImagesFromList
import requests
from flask import current_app
from app.utils.whiten import whitenapply



def extract_vectors(state, net, images, image_size, transform, bbxs=None, ms=[1], msp=1, print_freq=10):
    # moving network to gpu and eval mode
    # net.cuda()
    net.cpu()
    net.eval()

    whiten_ss = state['meta']['Lw']['retrieval-SfM-120k']['ss']

    # creating dataset loader
    loader = torch.utils.data.DataLoader(
        ImagesFromList(root='', images=images, imsize=image_size, bbxs=bbxs, transform=transform),
        batch_size=1, shuffle=False, num_workers=8, pin_memory=True
    )

    # extracting vectors
    with torch.no_grad():
        vecs = torch.zeros(net.meta['outputdim'], len(images))
        # vecs = torch.zeros(len(images), net.meta['outputdim'])
        for i, input in enumerate(loader):
            # input = input.cuda()
            input = input.cpu()
 

            if len(ms) == 1 and ms[0] == 1:
                vecs[:, i] = extract_ss(net, input.cpu())
                vecs[:, i] = vecs[:, i].data.cpu()
                vecs[:, i] = torch.from_numpy(whitenapply(vecs[:, i].reshape(-1,1), whiten_ss['m'], whiten_ss['P']).reshape(-1))
            else:
                vecs[:, i] = extract_ms(net, input, ms, msp)

            if (i+1) % print_freq == 0 or (i+1) == len(images):
                print('\r>>>> {}/{} done...'.format((i+1), len(images)), end='')
        print('')

    return vecs

def extract_image(state, net, images):
    normalize = transforms.Normalize(
        mean=net.meta['mean'],
        std=net.meta['std']
    )
    transform = transforms.Compose([
        transforms.ToTensor(),
        normalize
    ])

    # setting up the multi-scale parameters
    ms = list(eval('[1]'))
    if len(ms)>1 and net.meta['pooling'] == 'gem' and not net.meta['regional'] and not net.meta['whitening']:
        msp = net.pool.p.item()
        print(">> Set-up multiscale:")
        print(">>>> ms: {}".format(ms))            
        print(">>>> msp: {}".format(msp))
    else:
        msp = 1

    vecs = extract_vectors(
        state=state,
        net=net,
        images=images, 
        image_size=current_app.config['IMAGE_SIZE'], 
        transform=transform,
        ms=ms,
        msp=msp)
        
    return vecs

def extract_dataset(state, net, dataset_dir):
    images = os.listdir(dataset_dir)
    images = [os.path.join(dataset_dir, img_file) for img_file
                in images]
     # set up the transform
    normalize = transforms.Normalize(
        mean=net.meta['mean'],
        std=net.meta['std']
    )

    transform = transforms.Compose([
        transforms.ToTensor(),
        normalize
    ])

    # setting up the multi-scale parameters
    ms = list(eval('[1]'))
    if len(ms)>1 and net.meta['pooling'] == 'gem' and not net.meta['regional'] and not net.meta['whitening']:
        msp = net.pool.p.item()
        print(">> Set-up multiscale:")
        print(">>>> ms: {}".format(ms))            
        print(">>>> msp: {}".format(msp))
    else:
        msp = 1
    
    vecs = extract_vectors(
        state=state,
        net=net,
        images=images, 
        image_size=current_app.config['IMAGE_SIZE'], 
        transform=transform,
        ms=ms,
        msp=msp)   
    # save extracted features to file
    torch.save(vecs, current_app.config['FEATURE_PATH'])
    with open(current_app.config['IMAGEFILE_PATH'], 'a') as f:
        for line in images:
            f.write(line+'\n')
    vec_map = {}
    for img_path, img_vec in zip(images, vecs):
        vec_map[img_path] = img_vec
    p.dump(vec_map, open(current_app.config["VEC_MAP_PATH"], 'wb'))
    return f"Done extract for {dataset_dir}", requests.codes.ok

def extract_ss(net, input):
    return net(input).cpu().data.squeeze()

def extract_ms(net, input, ms, msp):
    
    v = torch.zeros(net.meta['outputdim'])
    
    for s in ms: 
        if s == 1:
            input_t = input.clone()
        else:    
            input_t = nn.functional.interpolate(input, scale_factor=s, mode='bilinear', align_corners=False)
        v += net(input_t).pow(msp).cpu().data.squeeze()
        
    v /= len(ms)
    v = v.pow(1./msp)
    v /= v.norm()

    return v

