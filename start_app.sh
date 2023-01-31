#!/bin/bash

pip install gdown
pip install --upgrade --no-cache-dir gdown
sudo apt-get update
sudo apt-get install unzip

cd backend/docker
if [ ! -f "backend.tar" ]; then
    echo "========================= [Downloading backend docker image ...] ========================="
    gdown 1-JpanCT9FgxubOELXBJUAtatfRzq_NZ5;
    # 
fi

echo "========================= [Loading docker image ...] ========================="
docker load -i backend.tar;
docker-compose -f docker-compose.yml up -d

cd ../../data;
if [ ! -f "oxford5k.zip" ]; then
    echo "========================= [Downloading $ unzip oxford5k dataset ...] ========================="
    gdown 1ZM0jvRZGYtPvqbJ44RviH1dYSZuzB9tV;
    # https://drive.google.com/file/d/1ZM0jvRZGYtPvqbJ44RviH1dYSZuzB9tV/view?usp=share_link
fi

if [ ! -d "oxford5k/jpg" ]; then
    unzip oxford5k.zip
fi
cd ..

echo "========================= [Finished.] ========================="