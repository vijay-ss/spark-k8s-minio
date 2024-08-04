# spark-k8s-minio

Start the cluster:
```
minikube start --memory 8192 --cpus 4
minikube dashboard
```

Build Docker image:
```
eval $(minikube docker-env)
docker build -t spark-hadoop:3.2.0 .
```

Create the deployments and services:
```
kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml
kubectl create -f ./kubernetes/spark-worker-deployment.yaml
```

In order to access the Spark web UI (port 8080) outside the cluster, configure an Ingress object
```
minikube addons enable ingress
kubectl apply -f ./kubernetes/minikube-ingress.yaml
```
On Linux:
```echo "$(minikube ip) spark-kubernetes" | sudo tee -a /etc/hosts```

On MacOs: 
Dont use minikube ip! You need to update /etc/hosts with a different ip address.

```echo "127.0.0.1 spark-kubernetes" | sudo tee -a /etc/hosts```

You can also do it manually in the terminal on either Linux or MacOs:
```
sudo vi /etc/hosts
127.0.0.1 spark-kubernetes
```

Then run ```minikube tunnel```

Now test it out in the browser: [http://spark-kubernetes/](http://spark-kubernetes/)

![](img/spark_webui.png)

Try running Spark in interactive mode:
```
kubectl exec spark-master-56465454b7-wrcb4 -it -- \
    pyspark --conf spark.driver.bindAddress=10.244.0.9 --conf spark.driver.host=10.244.0.9
```

Or submit the spark job to the master node directly:
```
kubectl exec spark-master-56465454b7-wrcb4  -it -- \
    spark-submit spark_jobs/main.py \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=spark-hadoop:3.2.0 \
    --deploy-mode cluster
```