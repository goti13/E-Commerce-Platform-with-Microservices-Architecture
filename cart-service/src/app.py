
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

