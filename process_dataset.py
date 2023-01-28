import os 
import shutil
import pickle
from glob import glob
from pathlib import Path

def main():
    data_dir = './data'
    dataset = 'oxford5k'
    dataset_dir = os.path.join(data_dir, dataset)
    data_ext = '.pkl'

    data_file = None
    data_file =  [os.path.join(
                dataset_dir, p.name) for p in Path(
                    dataset_dir
                    ).rglob("*"+data_ext)]

    if not data_file:
        raise Exception("No dataset description file found!")
    else: data_file = data_file[0]

    # print(data_file)
    with open(data_file, 'rb') as f:
        cfg = pickle.load(f)
    
    all_dir = os.path.join(data_dir,'all')
    if not os.path.isdir(all_dir):
        print('>> All images {} directory does not exist. Creating: {}'.format(data_dir, all_dir))
        os.makedirs(all_dir)
    
    query_dir = os.path.join(data_dir,'query')
    if not os.path.isdir(query_dir):
        print('>> Query {} directory does not exist. Creating: {}'.format(data_dir, query_dir))
        os.makedirs(query_dir)

    image_dir = os.path.join(data_dir, dataset, 'jpg')
    for img_name in cfg['imlist']:
        img_file = os.path.join(image_dir, img_name +'.jpg')
        if img_name not in cfg['qimlist']:
            shutil.move(img_file, all_dir)
        else:
            shutil.move(img_file, query_dir)
    


main()