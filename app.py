import hashlib
import os
from flask import  Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy.orm import sessionmaker
from models import Base, engine, User, Item, Basket, Order

app = Flask(__name__)
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

@app.route('/signup/')
def signup():
    title = 'Signup'
    return render_template('signup.html', title=title, heading=title)

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

    USER = DB.get(User).filter_by(email=email, password=password_hash).one()
    # Assuming the user isn't malicious
    session['USER'] = USER
    return redirect(url_for('index'))

@app.route('/logout/')
def logout():
    title = 'Logout'
    return render_template('login.html', title=title, heading=title)

    del session["USER"]

@app.route('/get/<int:item_no>/', methods=['POST'])
def get_item(item_no):
    
    item = DB.get(Item, item_no)
    basket = DB.query(Basket).filter_by(user_id)
    flash(f'Item {item.name} added')
    redirect(url_for('index'))

def check_login(render, title, heading):
    USER = session.get("USER")
    if USER:
        return redirect(url_for('search'))

    return render_template(render, title=title, heading=heading, user=USER)


if __name__ == '__main__':
    app.secret_key = os.urandom(32).hex()
    app.run()