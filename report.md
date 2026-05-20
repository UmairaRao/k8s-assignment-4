# Kubernetes Assignment Report: Flask and MySQL on Minikube

## Introduction
This project demonstrates a simple containerized Flask web application connected to a MySQL database and deployed on Kubernetes. The goal is to show core Kubernetes objects such as Deployments, Services, PersistentVolumeClaim, and HorizontalPodAutoscaler.

## Application Description
The Flask app allows users to submit text messages through a form and displays stored messages from a MySQL table. The app reads all database connection settings from environment variables.

## Tools Used
- Python 3.11
- Flask
- mysql-connector-python
- Docker
- Kubernetes
- Minikube
- kubectl

## Folder Structure
```text
k8s-assignment-4/
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── report.md
└── k8s/
    ├── mysql-pvc.yaml
    ├── mysql-deployment.yaml
    ├── mysql-service.yaml
    ├── web-deployment.yaml
    ├── web-service.yaml
    └── web-hpa.yaml
```

## Micro-Steps Followed
1. Created Flask application (`app.py`) with routes to add and list messages.
2. Added MySQL initialization logic to create `messages` table if missing.
3. Configured DB host, port, user, password, and database name using environment variables.
4. Created `requirements.txt` for Python dependencies.
5. Wrote Dockerfile for building image `flask-mysql-app:1.0`.
6. Created MySQL PVC for persistent data.
7. Created MySQL Deployment with 1 replica and mounted PVC at `/var/lib/mysql`.
8. Created MySQL ClusterIP Service for internal communication.
9. Created web Deployment using image `flask-mysql-app:1.0` and memory requests/limits.
10. Created web NodePort Service to expose the Flask app.
11. Created HPA (`autoscaling/v2`) scaling web deployment by memory utilization.
12. Wrote README with exact PowerShell commands for full execution.

## Explanation of YAML Files
- `mysql-pvc.yaml`: Requests 1Gi persistent storage for MySQL data.
- `mysql-deployment.yaml`: Runs MySQL with one replica, sets DB env vars, mounts PVC to `/var/lib/mysql`.
- `mysql-service.yaml`: Provides stable DNS (`mysql-service`) for web app to connect internally.
- `web-deployment.yaml`: Runs Flask app, passes DB env vars, sets memory requests/limits for scheduling and HPA.
- `web-service.yaml`: Exposes Flask deployment through NodePort to access from host browser.
- `web-hpa.yaml`: Automatically scales `web-deployment` from 1 to 7 replicas based on memory utilization.

## Screenshot Placeholders
- Screenshot 1: Running pods (`kubectl get pods`)
- Screenshot 2: Services (`kubectl get svc`)
- Screenshot 3: PVC status (`kubectl get pvc`)
- Screenshot 4: HPA status (`kubectl get hpa`)
- Screenshot 5: Browser view of Flask message app

## Full YAML Files

### mysql-pvc.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### mysql-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:8.0
          ports:
            - containerPort: 3306
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpass
            - name: MYSQL_DATABASE
              value: messagesdb
          volumeMounts:
            - name: mysql-storage
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-storage
          persistentVolumeClaim:
            claimName: mysql-pvc
```

### mysql-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  selector:
    app: mysql
  ports:
    - port: 3306
      targetPort: 3306
  type: ClusterIP
```

### web-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-web
  template:
    metadata:
      labels:
        app: flask-web
    spec:
      containers:
        - name: flask-web
          image: flask-mysql-app:1.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          env:
            - name: DB_HOST
              value: mysql-service
            - name: DB_PORT
              value: "3306"
            - name: DB_USER
              value: root
            - name: DB_PASSWORD
              value: rootpass
            - name: DB_NAME
              value: messagesdb
          resources:
            requests:
              memory: "128Mi"
            limits:
              memory: "256Mi"
```

### web-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: flask-web
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30080
  type: NodePort
```

### web-hpa.yaml
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 1
  maxReplicas: 7
  metrics:
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
```
