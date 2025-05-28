from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_session import Session
import sqlite3



app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

flowers = [
    {'id': 1, 'name': 'Букет "Весна"', 'price': 15000, 'image': 'images/vesna.jpg'},
    {'id': 2, 'name': '101 тюльпан', 'price': 25000, 'image': 'images/tulp.jpg'},
    {'id': 3, 'name': '1001 Роза', 'price': 40000, 'image': 'images/rosa.jpg'},
    {'id': 4, 'name': 'Корзина "Любовь"', 'price': 40000, 'image': 'images/lyubov.jpg'}
]

@app.route('/')
def index():
    return render_template('index.html', flowers=flowers)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/add_to_cart/<int:flower_id>')
def add_to_cart(flower_id):
    selected = next((f for f in flowers if f['id'] == flower_id), None)
    if selected:
        cart = session.get('cart', [])
        cart.append({
            'id': selected['id'],
            'name': selected['name'],
            'price': selected['price'],
            'image': selected['image']
        })
        session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
    return redirect(url_for('cart'))




@app.route('/submit_order', methods=['POST'])
def submit_order():
    bouquet_name = request.form['bouquet_name']
    delivery_time = request.form['delivery_time']
    address = request.form['address']
    sender_name = request.form['sender_name']
    recipient_name = request.form['recipient_name']
    card_message = request.form.get('card_message', '')

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (bouquet_name, delivery_time, address, sender_name, recipient_name, card_message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (bouquet_name, delivery_time, address, sender_name, recipient_name, card_message))
    conn.commit()
    conn.close()

    return render_template('index.html', flowers=flowers, success=True)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'tokareva':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Неверный логин или пароль')
    return render_template('admin_login.html')


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = cursor.fetchall()
    conn.close()

    return render_template('admin.html', orders=orders)


@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))




if __name__ == '__main__':
    app.run(debug=True)
