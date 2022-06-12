from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_incomes import Income

@app.route('/incomes')
def incomes():

    if 'uuid' not in session:
        return redirect('/')
        

    incomes = Income.get_all_users_incomes({'id': session['uuid']})

    return render_template('incomes_page.html', incomes = incomes)

@app.route('/incomes/new')
def incomes_new():

    if 'uuid' not in session:
        return redirect('/') 

    return render_template('income_new.html')

@app.route('/incomes/create', methods=['POST'])
def incomes_create():

    is_valid = Income.validator_create_income(request.form)

    if is_valid == False:
        return redirect('/incomes/new')
        
    data = {
        **request.form,
        'user_id': session['uuid']
    }

    income_id = Income.create_income(data)

    return redirect('/incomes')

@app.route('/incomes/edit/<int:id>')
def income_edit(id):

    if 'uuid' not in session:
        return redirect('/') 

    income = Income.select_one({'id': id})

    return render_template('income_edit.html', income = income)


@app.route('/incomes/update/<int:id>', methods=['POST'])
def income_update(id):

    is_valid = Income.validator_create_income(request.form)

    if is_valid == False:
        return redirect(f'/incomes/edit/{id}')
    
    data = {
        **request.form,
        'id': id
    }

    Income.update_one(data)

    return redirect('/incomes')

@app.route('/incomes/delete/<int:id>')
def income_delete(id):

    if 'uuid' not in session:
        return redirect('/')

    Income.delete_one({'id': id})

    return redirect('/incomes')


@app.route('/main/income/create', methods=['POST'])
def income_add_home():

    is_valid = Income.validator_create_income(request.form)


    if is_valid == False:
        return redirect('/main')

    data = {
        **request.form,
        'user_id': session['uuid']
    }

    income_id = Income.create_income(data)

    return redirect('/main')




