# spark-k8s-minio

Start the cluster:
```
minikube start --memory 8192 --cpus 4
minikube dashboard
```

Build Docker image:
```
eval $(minikube docker-env)
docker build -f docker/Dockerfile -t spark-hadoop:3.2.0 ./docker
```

Create the deployments and services:
```
kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml
kubectl create -f ./kubernetes/spark-worker-deployment.yaml
```

To configure ingress object, which is essential for accessing Spark web UI on port 8080 (or whichever is configured), first enable ingress addon and then create ingress object
```
minikube addons enable ingress
kubectl apply -f ./kubernetes/minikube-ingress.yaml
```