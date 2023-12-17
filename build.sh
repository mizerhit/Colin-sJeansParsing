#! /bin/bash

cd bot
touch tokens.py
echo "tg_token = '$1'" >> tokens.py

docker-compose up --build