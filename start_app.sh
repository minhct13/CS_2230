#!/bin/bash
cd backend/;
docker load --input docker/cs419.tar;
docker run backend-app:latest -p 8000;
