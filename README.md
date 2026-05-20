# Kubernetes Assignment - Flask + MySQL

## 1) Start Minikube (PowerShell)
```powershell
minikube start --driver=docker
```

## 2) Build Docker image in Minikube Docker environment
```powershell
minikube -p minikube docker-env --shell powershell | Invoke-Expression
docker build -t flask-mysql-app:1.0 .
```

## 3) Apply Kubernetes YAML files
```powershell
kubectl apply -f .\k8s\mysql-pvc.yaml
kubectl apply -f .\k8s\mysql-deployment.yaml
kubectl apply -f .\k8s\mysql-service.yaml
kubectl apply -f .\k8s\web-deployment.yaml
kubectl apply -f .\k8s\web-service.yaml
kubectl apply -f .\k8s\web-hpa.yaml
```

## 4) Check pods, services, PVC, and HPA
```powershell
kubectl get pods
kubectl get svc
kubectl get pvc
kubectl get hpa
```

## 5) Open app in browser
```powershell
minikube service web-service
```

> This opens the Flask web app in your default browser.
