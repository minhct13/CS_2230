#!/bin/bash
cd backend/;

pip install gdown

echo "========================= [Downloading backend docker image ...] ========================="
cd ./docker;gdown 1AacIr4gZh_Utq1R2Pro0OKK3Rh8XjWpB;

echo "========================= [Loading docker image ...] ========================="
docker load -i docker/cs419.tar;
docker-compose -f docker/docker-compose.yml up -d

echo "========================= [Downloading $ unzip oxford5k dataset ...] ========================="
cd ../../data;gdown 1g3wiFb9fEv7Zt8KTyEJJnU0jcbzgvIX3;
unzip oxford5k.zip
echo "========================= [Done, now you can start retrieve via index.html] ========================="