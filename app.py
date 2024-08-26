from flask import Flask, render_template, session, redirect, url_for,request,jsonify,flash
import sqlite3,joblib
import pandas as pd

app = Flask(__name__)

users = {}

app.secret_key = 'lkfashfwakldsjfaefiwfw_kja_axfwancsdklsdnfslf_sl_csjnfslsjnefqowejowiejfweo;kawf'

def get_connection():
    conn = sqlite3.connect('cloth.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_connection()
    men = pd.read_sql('SELECT * FROM Men LIMIT 5', conn)
    women = pd.read_sql('SELECT * FROM Women LIMIT 5', conn)
    conn.close()
    return render_template('index.html', men=men.to_dict(orient='records'), women=women.to_dict(orient='records'))

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email] == password:
        session['email'] = email
        return redirect(url_for('index'))
    else:
        flash('Incorrect email or password. Please try again.', 'error')
        return render_template('auth.html')
    
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['signup-username']
    email = request.form['signup-email']
    password = request.form['signup-password']

    if username in users:
        return "User already exists. Please login."
    else:
        users[email] = password
        session['email'] = email
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    print(f"Session before logout: {session}")
    session.pop('email', None)
    print(f"Session after logout: {session}")
    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search():
    category = request.args.get('category', 'all').lower()
    min_price = request.args.get('min-price', 0, type=float)
    max_price = request.args.get('max-price', float('inf'), type=float)

    conn = get_connection()

    base_query = 'SELECT * FROM {} WHERE Prices BETWEEN ? AND ?'
    params = [min_price, max_price]

    men_products = []
    if category == 'men' or category == 'all':
        query = base_query.format('Men')
        men_products = conn.execute(query, params).fetchall()

    women_products = []
    if category == 'women' or category == 'all':
        query = base_query.format('Women')
        women_products = conn.execute(query, params).fetchall()

    conn.close()

    men_products = [dict(row) for row in men_products]
    women_products = [dict(row) for row in women_products]

    return render_template('index.html', men=men_products, women=women_products)

@app.route('/men')
def men():
    conn = get_connection()
    men = pd.read_sql('SELECT * FROM Men', conn)
    conn.close()
    return render_template('men.html', products=men.to_dict(orient='records'))

@app.route('/women')
def women():
    conn = get_connection()
    women = pd.read_sql('SELECT * FROM Women', conn)
    conn.close()
    return render_template('women.html', products=women.to_dict(orient='records'))

@app.route('/cart')
def cart():
    if 'email' not in session:
        flash('Please log in to view your cart.', 'error')
        return redirect(url_for('auth')) 

    cart_items = session.get('cart', [])
    total_price = sum(float(item['Prices']) * item['Quantity'] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/add_to_cart/<string:Product_Name>/<string:category>')
def add_to_cart(Product_Name, category):
    conn = get_connection()
    query = f'SELECT * FROM {category} WHERE "Product Name" = ?'
    product = conn.execute(query, (Product_Name,)).fetchone()
    conn.close()
    
    if product:
        if 'cart' not in session:
            session['cart'] = []
        
        product_dict = dict(product)
        product_dict['Category'] = category
        found = False
        
        for item in session['cart']:
            if item['Product Name'] == Product_Name and item['Category'] == category:
                item['Quantity'] += 1 
                found = True
                break
        
        if not found:
            product_dict['Quantity'] = 1
            session['cart'].append(product_dict)
        
        session.modified = True  
    else:
        return "Product Not Found", 404
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<string:Product_Name>/<string:category>')
def remove_from_cart(Product_Name, category):
    print(f"Removing product: {Product_Name} from category: {category}")
    cart_items = session.get('cart', [])
    
    for item in cart_items:
        if item['Product Name'] == Product_Name and item['Category'] == category:
            cart_items.remove(item)
            break
    
    session['cart'] = cart_items
    session.modified = True
    print(f"Cart after removal: {session['cart']}")
    
    return redirect(url_for('cart'))

@app.route('/predict_size', methods=['POST'])
def predict_size():
    data = request.json
    weight = data['weight']
    age = data['age']
    height = data['height']
    
    model = joblib.load('randomforest_Regression.lb')
    
    input_df = pd.DataFrame([[weight, age, height]], columns=['weight', 'age', 'height'])
    
    predicted_size = model.predict(input_df)
    
    size_mapping = {
        1: "XXS",
        2: "S",
        3: "M",
        4: "L",
        5: "XL",
        6: "XXL",
        7: "XXXL"
    }
    size_label = size_mapping.get(int(predicted_size[0]), "Unknown")
    
    return jsonify({'predicted_size': size_label})

@app.route('/save_size/<string:Product_Name>/<string:category>', methods=['POST'])
def save_size(Product_Name, category):
    size = request.json['size']
    cart_items = session.get('cart', [])
    for item in cart_items:
        if item['Product Name'] == Product_Name and item['Category'] == category:
            item['Size'] = size
            break
    session['cart'] = cart_items
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
