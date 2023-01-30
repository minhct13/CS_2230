#!/bin/bash
cd backend/;

echo "Downloading backend docker image ..."
cd ./docker;wget https://drive.google.com/file/d/1AacIr4gZh_Utq1R2Pro0OKK3Rh8XjWpB/;

echo "Loading docker image ..."
docker load -i docker/cs419.tar;
docker-compose -f docker/docker-compose.yml up -d

echo "Downloading oxford5k dataset ..."
cd ../../data;wget https://drive.google.com/file/d/1g3wiFb9fEv7Zt8KTyEJJnU0jcbzgvIX3/;

echo "Done, now you can start retrieve via index.html"