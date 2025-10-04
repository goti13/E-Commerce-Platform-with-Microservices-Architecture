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

