start:
	@echo "Starting Minikube and Spark cluster..." 
	sh startup.sh
stop:
	@echo "Stopping Kubernetes pods..."
	sh delete.sh