#!/bin/sh

docker-compose up -d api web redis
docker run -d --gpus all --network antonovka_default --mount source=antonovka_storage,target=/app/storage antonovka_worker
