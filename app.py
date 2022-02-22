import hashlib
import secrets

from flask import  Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy.orm import sessionmaker
from models import Base, Selection, engine, User, StockItem

app = Flask(__name__)
app.secret_key = secrets.token_hex()


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DB = DBSession()

@app.route('/')
@app.route('/index/')
def index():
    title = 'Home'
    heading = 'Restaurant'
    user = session.get('USER')
    items = DB.query(StockItem).all()
    selection = DB.query(Selection).filter_by(user_id=user['id'], paid=False).all()
    return render_template('index.html', title=title, heading=heading, items=items, user=user, cart=selection)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    title = 'Signup'
    
    if request.method == 'GET':
        return render_template('signup.html', title=title, heading=title)
    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

# Perform Validation of User Inputs
    if not(email and password):
        flash('One or both fields empty')
        return redirect(url_for('signup'))

    password_hash = hashlib.md5(password.encode()).hexdigest()
    new_user = User(name=name, email=email, password=password_hash)
    DB.add(new_user)
    DB.commit()
    flash(f'New User {new_user.name} added successfullly with email, {new_user.email}.')
    
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    title = 'Login'
    
    if request.method == 'GET':
        return render_template('login.html', title=title, heading=title)
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not(email and password):
        flash('Email or Password Not Given')
        return redirect(url_for('login'))

    password_hash = hashlib.md5(password.encode()).hexdigest()

    USER = DB.query(User).filter_by(email=email, password=password_hash).one()

    session['USER'] = {'name': USER.name, 'id': USER.id}
    flash(f'Welcome {USER.name}.')
    return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    title = 'Logout'
    name = session['USER']
    session.pop("USER", None)
    flash(f'User {name} logged out.')
    return redirect(url_for('index'))



@app.route('/get/<int:item_no>/')
def get_item(item_no):
    
    user = session.get('USER')
    if user is None:
        return redirect(url_for('login'))
    
    selection = Selection(user_id=user.get('id'), item_no=item_no)
    DB.add(selection)
    DB.commit()

    item = DB.get(StockItem, item_no)
    item.stock_qty -= 1
    DB.add(item)
    DB.commit()
    
    flash(f'Item {item.name} added to your cart')
    return redirect(url_for('index'))


@app.route('/checkout')
def checkout():
    
    user = session.get('USER')
    if user is None:
        return redirect(url_for('login'))
    
    basket = DB.query(Selection).filter_by(user_id=user.get('id'), paid=False).all()
    for item in basket:
        item.paid = True
        DB.add(item)
        DB.commit()
    
    flash('Payment successful.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # app.secret_key = secrets.token_hex()
    app.run()