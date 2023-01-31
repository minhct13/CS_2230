#!/bin/bash

cd backend/;

pip install gdown

cd ./docker
if [ ! -f "backend.tar" ]; then
    echo "========================= [Downloading backend docker image ...] ========================="
    gdown 1hsHOtxf2KiQO_Hn2K1A4xjdRclAPWSQ4;
fi

echo "========================= [Loading docker image ...] ========================="
docker load -i cs419.tar;
docker-compose -f docker-compose.yml up -d

cd ../../data;
if [ ! -f "oxford5k.zip" ]; then
    echo "========================= [Downloading $ unzip oxford5k dataset ...] ========================="
    gdown 1g3wiFb9fEv7Zt8KTyEJJnU0jcbzgvIX3;
fi

if [ ! -d "oxford5k/jpg" ]; then
    apt-get install unzip
    unzip oxford5k.zip
fi

echo "========================= [Finished.] ========================="