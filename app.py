#!/usr/bin/env python3

from flask import Flask, render_template, request, session, redirect, url_for, make_response
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
import subprocess

# instantiate the app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
import credentials
config = credentials.get()

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# make one persistent connection to the database
connection = pymongo.MongoClient(config['MONGO_HOST'], 27017, 
                                username=config['MONGO_USER'],
                                password=config['MONGO_PASSWORD'],
                                authSource=config['MONGO_DBNAME'])
db = connection[config['MONGO_DBNAME']] # store a reference to the database

# set up the routes

@app.route('/')
def home():
    """
    Route for the home page
    """ 
    return redirect(url_for('login')) # render the home template 

@app.route('/login')
def login():
    """
    Route for the home page
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def process_login():
    us = request.form['us']
    psw = request.form['psw']

    existing = db.listUsers.find_one({ "username": us, "password": psw})

    if (existing != None):
        session['username'] = us
        return redirect(url_for('index'))

    else:
        error = 1
        return render_template("login.html", error = error)

@app.route('/login/<error>')
def show_issue(error):
    error = error
    return redirect (url_for('home'))

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def process_signup():
    fn = request.form['firstName']
    ln = request.form['lastName']
    email = request.form['email']

    us = request.form['us']
    psw = request.form['psw']
    psw2 = request.form['psw-repeat']

    if (psw != psw2):
        error = 1
        return render_template("signup.html", error = error)
    
    else:
        existing = db.listUsers.find_one({ "username": us})
        if (existing != None):
            error = 2
            return render_template("signup.html", error = error)
        else:
            check_email = db.listUsers.find_one({ "email": email})
            if (check_email != None):
                error = 3
                return render_template("signup.html", error = error)
            else:
                db.listUsers.insert_one({ "username": us, "password": psw, "first": fn, "last": ln, "email": email})
                return redirect(url_for('login'))

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    title = request.form['title']
    notes = request.form['notes']
    listLabel = request.form['listLabel']
    dueDate = request.form['dueDate']
    dueTime = request.form['dueTime']

    # create a new document with the data the user entered
    todo = {
        "username": session['username'],
        "title": title,
        "notes": notes, 
        "listLabel": listLabel,
        "dueDate": dueDate,
        "dueTime": dueTime,
        "created_at": datetime.datetime.utcnow()
    }
    db.todos.insert_one(todo) # insert a new document

    return redirect(url_for('viewtodos')) # tell the browser to make a request for the /read route

@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    todo = db.todos.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, todo=todo) # render the edit template

@app.route('/edit/<mongoid>', methods=['POST'])
def edit_todo(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    title = request.form['title']
    notes = request.form['notes']
    listLabel = request.form['listLabel']
    dueDate = request.form['dueDate']
    dueTime = request.form['dueTime']

    todo = {
        "username": session['username'],
        "title": title,
        "notes": notes, 
        "listLabel": listLabel,
        "dueDate": dueDate,
        "dueTime": dueTime,
        "created_at": datetime.datetime.utcnow()
    }

    db.todos.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": todo }
    )

    return redirect(url_for('viewtodos')) # tell the browser to make a request for the /read route

@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    db.todos.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('viewtodos')) # tell the web browser to make a request for the /read route.ß

@app.route('/viewtodos')
def viewtodos():
    todos = db.todos.find({"username": session['username']}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('viewtodos.html', todos=todos)

# @app.errorhandler(Exception)
# def handle_error(e):
#     """
#     Output any errors - good for debugging.
#     """
#     return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')