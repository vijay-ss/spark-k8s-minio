#!/bin/bash

MINIO_POD=$(kubectl get pod -n minio-dev | awk '{print$1}' | grep -F -e 'minio-')
MINIO_POD_IP=$(kubectl get svc -A | grep -F -e 'minio-dev' | awk '{print $4}')
echo ${MINIO_POD_IP}

SPARK_MASTER=$(kubectl get pods | awk '{print $1}' | grep -F -e '-master-')
echo ${SPARK_MASTER}

kubectl logs -n minio-dev ${MINIO_POD}

kubectl exec ${SPARK_MASTER} -it -- \
    spark-submit spark_jobs/main.py minio.minio-dev.svc.cluster.local:9000 \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=spark-hadoop:3.2.0 \
    --deploy-mode cluster

# kubectl exec ${SPARK_MASTER} -it -- \
#     spark-submit \
#     --conf spark.executor.instances=1 \
#     --conf spark.kubernetes.container.image=spark-hadoop:3.2.0 \
#     local:///spark_jobs/main.py