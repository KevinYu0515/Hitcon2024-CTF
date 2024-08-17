from flask import Flask, request, session, render_template, redirect, url_for, abort
from utils.role import User
from flask_cors import CORS
from dataclasses import asdict
import db.shop_action as shop_db
import db.user_action as user_db
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)
shop_db.initial()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'username' in session:
        user = user_db.query(session.get('username'))
        items = shop_db.query_all()
        return render_template('commodity.html', items=items, user=user)
    return redirect(url_for('index'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('shop')
    if request.method == 'POST':
        user = User(username=request.form.get('username'))
        session['username'] = user.username
        if not user_db.query(user.username):
            user_db.add_user(asdict(user))
        return redirect(url_for('shop'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

@app.route('/collection', methods=['GET'])
def collection():
    if 'username' in session:
        user = user_db.query(session.get('username'))
        return render_template('collection.html', items=list(user.items.values()), user=user)
    return redirect(url_for('index'))

@app.route('/buy', methods=['POST'])
def buy():
    if 'username' in session:
        user = user_db.query(session.get('username'))
        data = request.json
        for name in data.get('item'):
            try:
                user.buy_item(shop_db.query(name))
                user_db.update(user.username, asdict(user))
            except ValueError as e:
                break
        print('ok')
        return redirect(url_for('shop'))
    return abort(500)

@app.route('/sell', methods=['POST'])
def sell():
    if 'username' in session:
        user = user_db.query(session.get('username'))
        data = request.json
        for name in data.get('item'):
            try:
                user.sell_item(name)
                user_db.update(user.username, asdict(user))
            except ValueError as e:
                break
        return redirect(url_for('shop'))
    return abort(500)

@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('shop'))