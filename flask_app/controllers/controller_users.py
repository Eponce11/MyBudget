from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_users import User

@app.route('/create', methods=['POST'])
def create_user():
    
    is_valid = User.validator_create_user(request.form)

    if is_valid == False:
        return redirect('/create_account')

    hash_pw = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        'password': hash_pw
    }

    id = User.create_user(data)

    session['uuid'] = id

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():

    is_valid = User.validator_login(request.form)

    if is_valid == False:
        return redirect('/')

    return redirect('/main')


@app.route('/logout')
def logout():
    if 'uuid' in session:
        session.pop('uuid')
    
    return redirect('/')

