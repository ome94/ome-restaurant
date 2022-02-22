import hashlib
import secrets

from flask import  Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy.orm import sessionmaker
from models import Base, engine, User, Item, Basket, Order

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
    USER = session.get('USER')
    items = DB.query(Item).all()
    return render_template('index.html', title=title, heading=heading, items=items, user=USER)


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

    session['USER'] = USER.name
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
    
    item = DB.get(Item, item_no)
    item.stock_qty -= 1
    DB.add(item)
    DB.commit()
    
    user = session['USER']
    basket = DB.query(Basket).filter_by(user_id=user.id, checked=False).all()
    flash(f'Item {item.name} added')
    redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = secrets.token_hex()
    app.run()