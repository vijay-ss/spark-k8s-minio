start:
	@echo "Starting Minikube and Spark cluster..." 
	sh scripts/startup.sh
stop:
	@echo "Stopping Kubernetes pods..."
	sh scripts/delete.sh
delete:
	@echo "Deleting Minikube cluster and resources..."
	minikube delete
reset:
	@echo "Deleting and restarting cluster..."
	minikube delete
	sh scripts/startup.sh
build:
	@echo "Building docker image..."
	eval $(minikube docker-env)
	docker build -t spark-hadoop:3.2.0 .
debug:
	@echo "Debugging configuration..."
	kubectl get svc -A
	kubectl get pod -n minio-dev
spark:
	@echo "Running Spark job..."
	sh scripts/spark.sh