# ----------------------------------------------------------------------
# This script contains URL mappings for auth routes of flask app
#
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#
#-----------------------------------------------------------------------

#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from pymongo import database
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from .create_sandbox import *
auth = Blueprint('auth', __name__)

#login route code
@auth.route('/login')
def login():
    return render_template('login.html')

#signup route code
@auth.route('/signup')
def signup():
    return render_template('signup.html')


#logout route code
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.logged_out'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first() 

    if user: 
        flash('User name is already taken, try other name')
        return redirect(url_for('auth.signup'))


    new_user = User(name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    user_name = name
    if(create_sandbox(user_name)):
        if(annotations_directory(user_name)):
            if(dirlist(user_name)[0]):
                from pymongo import MongoClient
                connection = MongoClient('localhost',27017)
                database = connection.get_database('anno_admin')
                collection = database["author_job"]
                job_list = ""
                for document in dirlist(user_name)[1]:
                    job_list += document+":pending,"
                job_list = job_list[:len(job_list)-1]
                collection.insert_one({"email":user_name, "jobs":job_list})
                database = connection.get_database('models')
                collection = database["user_models"]
                collection.insert_one({"email":user_name, "Pool_Closure":""})
                return redirect(url_for('auth.login'))
    flash('Some problem setting up your sandbox! Try again later')
    return redirect(url_for('auth.signup'))

@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    print(user)
    f2(name)
    return redirect(url_for('main.load_jobs'))

    
def f2(name):
    import os
    current_path = os.getcwd()
    app_name = __name__.replace(".auth","")
    app_path = current_path + '/' + app_name +  '/'
    print('\n********************************\n')
    print('python3 ' + app_path +  'set_first.py '+ app_path)
    print('\n********************************\n')
    mesgs = os.popen('python3 ' + app_path +  'set_first.py ' + name + ' ' + app_path).read()
    print(mesgs)