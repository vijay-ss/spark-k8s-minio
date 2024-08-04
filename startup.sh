#!/bin/bash

minikube start --memory 8192 --cpus 4

eval $(minikube docker-env)
docker build -t spark-hadoop:3.2.0 .

sh create.sh

SPARK_MASTER=$(kubectl get pods | awk '{print $1}' | grep -F -e '-master-')
echo ${SPARK_MASTER}

kubectl exec ${SPARK_MASTER} -it -- \
    spark-submit spark_jobs/main.py \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=spark-hadoop:3.2.0 \
    --deploy-mode cluster