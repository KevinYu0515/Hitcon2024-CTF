from flask import Flask, request, render_template, redirect, url_for
from utils.role import User
from flask_cors import CORS
import db.action as db
app = Flask(__name__)
CORS(app)

user = User(2000)
db.initial()

@app.route('/', methods=['GET', 'POST'])
def index():
    items = db.query_all()
    return render_template('commodity.html', items=items, user=user)

@app.route('/collection', methods=['GET'])
def collection():
    return render_template('collection.html', items=list(user.items.values()), user=user)

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    for name in data.get('item'):
        try:
            user.buy_item(db.query(name))
        except ValueError as e:
            break
    return redirect(url_for('index'))

@app.route('/sell', methods=['POST'])
def sell():
    data = request.json
    for name in data.get('item'):
        try:
            user.sell_item(name)
        except ValueError as e:
            break
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()