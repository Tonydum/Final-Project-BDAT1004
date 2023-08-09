from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# ... (your existing routes)
# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prices')
def get_prices():
    # Connect to MongoDB and retrieve price data
    client = MongoClient('mongodb://tonydum126:Icenova22@ac-l1mncqa-shard-00-00.s8ode9n.mongodb.net:27017,ac-l1mncqa-shard-00-01.s8ode9n.mongodb.net:27017,ac-l1mncqa-shard-00-02.s8ode9n.mongodb.net:27017/?ssl=true&replicaSet=atlas-cioiiy-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['Cryptocurrency']
    collection = db['Cryptocurrency']
    price_data = list(collection.find({}, {'_id': 0}))

    return jsonify(price_data)

@app.route('/search', methods=['GET'])
def search():
    symbol = request.args.get('symbol')

    if not symbol:
        return redirect(url_for('index'))

    client = MongoClient('mongodb://tonydum126:Icenova22@ac-l1mncqa-shard-00-00.s8ode9n.mongodb.net:27017,ac-l1mncqa-shard-00-01.s8ode9n.mongodb.net:27017,ac-l1mncqa-shard-00-02.s8ode9n.mongodb.net:27017/?ssl=true&replicaSet=atlas-cioiiy-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['Cryptocurrency']
    collection = db['Cryptocurrency']
    
    price_data = list(collection.find({'symbol': symbol}, {'_id': 0}))
    return render_template('search_results.html', symbol=symbol, price_data=price_data)

if __name__ == '__main__':
    app.run(debug=True)
