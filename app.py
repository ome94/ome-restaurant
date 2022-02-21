import os
from flask import  Flask, render_template, redirect, request, url_for, session
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
    items = DB.query(Item).all()
    return render_template('index.html', title=title, heading=heading, items=items)

@app.route('/signup/')
def signup():
    title = 'Signup'
    return render_template('signup.html', title=title, heading=title)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    title = 'Login'
    return render_template('login.html', title=title, heading=title)

@app.route('/logout/')
def logout():
    title = 'Logout'
    return render_template('login.html', title=title, heading=title)

    del session["USER"]

@app.route('/get/<int:item_no>/', methods=['POST'])
def get_item(item_no):
    pass

def check_login(render, title, heading):
    USER = session.get("USER")
    if USER:
        return redirect(url_for('search'))

    return render_template(render, title=title, heading=heading, user=USER)


if __name__ == '__main__':
    app.secret_key = os.urandom(32).hex()
    app.run()