#!/bin/bash
echo "=== Debugging Route Issues ==="

echo "1. Checking Flask app routes in product-service:"
cat product-service/src/app.py | grep "@app.route"

echo ""
echo "2. Testing product service directly:"
kubectl port-forward -n ecommerce svc/product-service 8080:80 2>/dev/null &
sleep 2
echo "   /products: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/products)"
echo "   /health: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)"
pkill -f "kubectl port-forward"

echo ""
echo "3. Testing through Kong with verbose output:"
kubectl port-forward -n kong svc/kong-kong-proxy 9031:80 2>/dev/null &
sleep 2
echo "   Testing /products:"
curl -v http://localhost:9031/products 2>&1 | grep -E "(HTTP|< HTTP|> GET)"
echo ""
echo "   Testing /health:"
curl -v http://localhost:9031/health 2>&1 | grep -E "(HTTP|< HTTP|> GET)"
pkill -f "kubectl port-forward"

echo ""
echo "=== Debug Complete ==="
