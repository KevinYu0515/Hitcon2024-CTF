from flask import jsonify, render_template, redirect, url_for, flash, render_template_string, request
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import RegistrationForm, LoginForm, BoardForm
from app.models import User, Board
from app import app, db
from datetime import datetime, timezone

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
@login_required
def home():
    boards = Board.query.order_by(Board.timestamp.desc())
    return render_template('home.html', boards=boards)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/newboard', methods=['GET', 'POST'])
@login_required
def newboard():
    form = BoardForm()
    form.creator.data = current_user.username
    if form.validate_on_submit():
        board = Board(creator=form.creator.data, title=form.title.data, left_name=form.left.data, right_name=form.right.data)
        db.session.add(board)
        db.session.commit()
        flash('Success, you create a new board!')
        return redirect(url_for('index'))
    return render_template('newboard.html', form=form)

@app.route('/board', methods=['GET', 'POST'])
@login_required
def board():
    name = render_template_string(request.args.get('name'))
    print(name)
    board = Board.query.filter_by(title=name).first()
    if not board:
        return redirect(url_for('index'))
    return render_template('board.html', board=board)

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    data = request.json
    vote_result = data.get('vote_result')
    board_id = data.get('id')
    board = Board.query.filter_by(id=board_id).first()
    if board:
        board.left_vote += vote_result['left_vote']
        board.right_vote += vote_result['right_vote']
        if board.left_vote < 0:
            board.left_vote = 0
        if board.right_vote < 0:
            board.right_vote = 0
        db.session.commit()
        
    updated_data = {
        'left_vote': board.left_vote,
        'right_vote': board.right_vote
    }
    return jsonify(updated_data)