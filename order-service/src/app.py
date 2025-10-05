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

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

