# Capstone Project: E-Commerce Platform with Microservices Architecture


Hypothetical Use Case

You are tasked with developing an e-commerce platform using a microservices-based architecture. The platform consists of several microservices:

- Product Service: Manages product information.

- Cart Service: Handles user shopping carts.

- Order Service: Manages order processing.

The goal is to containerize these microservices using Docker, deploy them to a Kubernetes cluster managed by ArgoCD, and expose them through an API Gateway.


Tasks


Task 1: Project Setup:

- Create a new project directory named 'ecommerce-platform'.


- Inside, create subdirectories for each microservice: 'product-service', 'cart-service', 'order-service'.


Task 2: Initialize Git Repository:


- Initialize a Git repository in your 'ecommerce-platform' directory.


Task 3: Version Control:


- Add and commit your initial project structure to the Git repository.


Task 4: Dockerize Microservices:


- For each microservice, create a 'Dockerfile' specifying a base image (e.g., Python/Flask or Node.js/Express).


- Implement basic functionalities for each service:


	- 'product-service': API to list and view products.


	- "cart-service': API to add/remove items to/from a cart.

	- 'order-service': API to create and view orders..


Task 5: Push to Docker Hub:

- Log in to Docker Hub and create a repository for each microservice.

- Build Docker images and push them to Docker Hub.



Task 6: Set up ArgoCD with Kubernetes:


- Install ArgoCD in a Kubernetes cluster.

- Connect your Git repository to ArgoCD.


Task 7: Kubernetes Deployment:

- Create Kubernetes deployment YAML files for each microservice.

- Define the ArgoCD application YAMLs to manage these deployments.


Task 8: Create Kubernetes Services:

- Create Kubernetes service YAML files for each microservice, specifying the type as 'Cluster IP'.

- Use ArgoCD to apply these services to your cluster.

Task 9 (Advanced): API Gateway Integration:

- Set up an AP| Gateway (e.g., Kong or Ambassador) in Kubernetes as an Ingress controller.

- Define Ingress resources to route traffic to the appropriate microservice.


- Use ArgoCD to manage the Ingress resource deployment.


Task 10: Monitoring and Logging (Optional):

- Integrate a monitoring solution like Prometheus and Grafana.

- Set up logging using Elasticsearch, Fluentd, and Kibana (EFK stack).


--------------------------------------------------------------------------------------------------------------------------
                                                PROJECT IMPLEMENTATION
--------------------------------------------------------------------------------------------------------------------------

# Phase 1: Project Setup & Local Development




**Step 1:Create project structure**


```text

ecommerce-platform/
├── product-service/
│   ├── src/
│   │   └── app.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── cart-service/
│   ├── src/
│   │   └── app.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── order-service/
│   ├── src/
│   │   └── app.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── kubernetes/
│   ├── manifests/
│   │   ├── namespace.yaml
│   │   ├── product-service.yaml
│   │   ├── cart-service.yaml
│   │   ├── order-service.yaml
│   │   └── kong-ingress.yaml
│   └── argocd/
│       └── ecommerce-app.yaml
├── api-gateway/
│   └── kong-ingress.yaml
├── monitoring/
├── .gitignore
└── README.md

```


1. Create main project directory


```bash
mkdir ecommerce-platform
cd ecommerce-platform
```
2. Create microservices directories

```bash
mkdir product-service cart-service order-service kubernetes api-gateway monitoring

```
3. Create src directories for each service

```bash
mkdir product-service/src product-service/tests
mkdir cart-service/src cart-service/tests  
mkdir order-service/src order-service/tests

```

4. Create Kubernetes directories

```bash
mkdir kubernetes/manifests kubernetes/argocd

```

**Initialize Git**

```bash
git init
echo "# Capstone Project: E-Commerce Platform with Microservices Architecture" > README.md

```

**Step 2: Create Microservice Applications**

Product Service (product-service/src/app.py):

```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Sample product data
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics", "stock": 15},
    {"id": 2, "name": "Smartphone", "price": 699.99, "category": "Electronics", "stock": 30},
    {"id": 3, "name": "Headphones", "price": 149.99, "category": "Electronics", "stock": 50},
    {"id": 4, "name": "Desk Chair", "price": 199.99, "category": "Furniture", "stock": 10}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({
        "products": products,
        "count": len(products)
    })

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "product-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

```


Cart Service 

Cart Service (cart-service/src/app.py):


```python

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory cart storage (replace with Redis in production)
carts = {}

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {"user_id": user_id, "items": [], "total": 0})
    return jsonify(cart)

@app.route('/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if user_id not in carts:
        carts[user_id] = {"user_id": user_id, "items": [], "total": 0}
    
    # Check if item already in cart
    existing_item = next((item for item in carts[user_id]['items'] if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        carts[user_id]['items'].append({
            "product_id": product_id,
            "quantity": quantity
        })
    
    # Update total (simplified - in real app, fetch product price)
    carts[user_id]['total'] = sum(item['quantity'] * 100 for item in carts[user_id]['items'])
    
    return jsonify({"message": "Item added to cart", "cart": carts[user_id]})

@app.route('/cart/<user_id>/remove/<product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    if user_id in carts:
        carts[user_id]['items'] = [item for item in carts[user_id]['items'] if item['product_id'] != int(product_id)]
        carts[user_id]['total'] = sum(item['quantity'] * 100 for item in carts[user_id]['items'])
    
    return jsonify({"message": "Item removed from cart", "cart": carts.get(user_id, {"user_id": user_id, "items": [], "total": 0})})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "cart-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

```

Order Service (order-service/src/app.py):

```python
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

orders = []
order_id_counter = 1

@app.route('/orders', methods=['POST'])
def create_order():
    global order_id_counter
    data = request.json
    
    order = {
        "id": order_id_counter,
        "user_id": data['user_id'],
        "items": data['items'],
        "total": data['total'],
        "status": "confirmed",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    orders.append(order)
    order_id_counter += 1
    
    return jsonify({"message": "Order created successfully", "order": order})

@app.route('/orders/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    user_orders = [order for order in orders if order['user_id'] == user_id]
    return jsonify({
        "orders": user_orders,
        "count": len(user_orders)
    })

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "order-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

```

**Step 3: Create Requirements Files**


```text

# product-service/requirements.txt
Flask==2.3.3

# cart-service/requirements.txt  
Flask==2.3.3

# order-service/requirements.txt
Flask==2.3.3

```

**Step 4: Create Dockerfiles**

Product Service Dockerfile (product-service/Dockerfile):

```

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5000

CMD ["python", "app.py"]

```

Cart Service Dockerfile (cart-service/Dockerfile):


```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5001

CMD ["python", "app.py"]

```

Order Service Dockerfile (order-service/Dockerfile):

```

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5002

CMD ["python", "app.py"]

```

Step 5: Test Locally

```bash

# Test product service
cd product-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py

# In another terminal, test the API
curl http://localhost:5003/products

```


# Phase 2: Containerization & Docker Hub


**Step 6: Build and Push Docker Images**

```

# Replace 'yourusername' with your actual Docker Hub username
DOCKER_USERNAME="yourusername"

# Build images
docker build -t $DOCKER_USERNAME/product-service:latest ./product-service
docker build -t $DOCKER_USERNAME/cart-service:latest ./cart-service  
docker build -t $DOCKER_USERNAME/order-service:latest ./order-service

# Login to Docker Hub
docker login

# Push images
docker push $DOCKER_USERNAME/product-service:latest
docker push $DOCKER_USERNAME/cart-service:latest
docker push $DOCKER_USERNAME/order-service:latest

```

**Step 7: Commit to Git**

Step 7: Commit to Git

```

# Create .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.env
.DS_Store
EOF

# Add and commit everything
git add .
git commit -m "Initial commit: E-commerce microservices platform"

# Create GitHub repository and push (replace with your repo URL)
git remote add origin https://github.com/yourusername/ecommerce-platform.git
git branch -M main
git push -u origin main

```

# Phase 3: Kubernetes Setup

**Step 8: Start Kubernetes Cluster**

```bash
# Start minikube cluster
minikube start --memory=4096 --cpus=2

# Verify cluster is running
kubectl cluster-info
kubectl get nodes

```

# Step 9: Create Kubernetes Manifests

Namespace (kubernetes/manifests/namespace.yaml):

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce
  labels:
    name: ecommerce

```

Product Service (kubernetes/manifests/product-service.yaml):

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
    spec:
      containers:
      - name: product-service
        image: yourusername/product-service:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
spec:
  selector:
    app: product-service
  ports:
  - name: http
    port: 80
    targetPort: 5000
    protocol: TCP
  type: ClusterIP

```


Cart Service (kubernetes/manifests/cart-service.yaml):

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-service
  namespace: ecommerce
  labels:
    app: cart-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cart-service
  template:
    metadata:
      labels:
        app: cart-service
    spec:
      containers:
      - name: cart-service
        image: yourusername/cart-service:latest
        ports:
        - containerPort: 5001
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: cart-service
  namespace: ecommerce
  labels:
    app: cart-service
spec:
  selector:
    app: cart-service
  ports:
  - name: http
    port: 80
    targetPort: 5001
    protocol: TCP
  type: ClusterIP

```

Order Service (kubernetes/manifests/order-service.yaml):

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: yourusername/order-service:latest
        ports:
        - containerPort: 5002
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5002
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5002
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
spec:
  selector:
    app: order-service
  ports:
  - name: http
    port: 80
    targetPort: 5002
    protocol: TCP
  type: ClusterIP

```

# Phase 4: ArgoCD Setup

**Step 10: Install ArgoCD**

1. Create argocd namespace

```bash

kubectl create namespace argocd

```

2. Install ArgoCD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

```

3. Wait for pods to be ready

```bash

kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

```

4. Get ArgoCD admin password

```bash

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

```

5. Port forward to access ArgoCD UI

```bash

kubectl port-forward svc/argocd-server -n argocd 8080:443

```

Access ArgoCD UI at: https://localhost:8080 (username: admin, password from above)


**Step 11: Create ArgoCD Application**

ArgoCD Application (kubernetes/argocd/ecommerce-app.yaml):

```yaml

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-platform
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourusername/ecommerce-platform.git
    targetRevision: main
    path: kubernetes/manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
    - CreateNamespace=true

```


**Apply ArgoCD Application:**


```bash

kubectl apply -f kubernetes/argocd/ecommerce-app.yaml

```

# Phase 5: API Gateway Setup


**Step 12: Install Helm and Kong Ingress Controller**

Install Helm using Homebrew (recommended)

```bash
brew install helm

```

OR Install using the official script

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

chmod 700 get_helm.sh
./get_helm.sh

```

Verify Helm installation

```
helm version

```

Add Kong Helm Repository and Install

```bash
helm repo add kong https://charts.konghq.com
helm repo update

```
Verify the repo was added

```bash

helm repo list

```

Install Kong in the kong namespace

```bash

kubectl create namespace kong
helm install kong kong/kong -n kong \
  --set ingressController.installCRDs=false \
  --set service.type=NodePort \
  --set env.database=off \
  --set env.nginx_worker_processes=2

```

Wait for Kong to be ready

```bash

kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kong -n kong --timeout=300s

```


Verify Kong installation

```bash

kubectl get all -n kong

```


**Step 13: Create Ingress Resource**


Kong Ingress (api-gateway/kong-ingress.yaml):

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: kong
spec:
  rules:
  - http:
      paths:
      - path: /products
        pathType: Prefix
        backend:
          service:
            name: product-service
            port:
              number: 80
      - path: /cart
        pathType: Prefix
        backend:
          service:
            name: cart-service
            port:
              number: 80
      - path: /orders
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 80

```

Apply the ingress:

```bash

kubectl apply -f api-gateway/kong-ingress.yaml

```

# Phase 6: Testing & Verification



**Step 14: Test the Deployment**

Get all resources in ecommerce namespace

```bash

kubectl get all -n ecommerce

```

Check ArgoCD application status


```bash

kubectl get application -n argocd

```


Get Kong service details

```bash

kubectl get svc -n kong

```

Test services through Kong
First, get the Kong proxy URL

```bash

minikube service -n kong kong-kong-proxy --url

```


Use the URL to test (replace KONG_URL with actual URL)


```bash

KONG_URL=$(minikube service -n kong kong-kong-proxy --url)

```

Test product service


```bash

curl $KONG_URL/products

```

Test cart service


```bash
curl -X POST $KONG_URL/cart/user123/add \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

```


Test order service  


```bash

curl -X POST $KONG_URL/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "items": [{"product_id": 1, "quantity": 2}], "total": 199.98}'

```

# Phase 7: Optional Monitoring (Prometheus & Grafana)


**Step 15: Install Monitoring Stack**

Add Prometheus community helm charts

```bash

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

```

Install kube-prometheus stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

```


<img width="2418" height="1572" alt="image" src="https://github.com/user-attachments/assets/8d41e4b7-eae0-4009-bc90-1d5e4d0fec58" />




