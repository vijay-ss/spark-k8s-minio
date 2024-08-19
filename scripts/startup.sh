#!/bin/bash

minikube start --memory 8192 --cpus 4

eval $(minikube docker-env)
docker build -t spark-hadoop:3.2.0 .

sh scripts/create.sh

sleep 30

sh scripts/spark.sh