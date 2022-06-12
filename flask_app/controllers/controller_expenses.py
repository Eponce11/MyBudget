from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_expenses import Expense
from flask_app.models.model_categories import Category


@app.route('/expenses/<int:category_id>')
def expenses(category_id):

    if 'uuid' not in session:
        return redirect('/')


    expenses = Expense.get_all_category_expenses({'id': category_id})

    category = Category.select_one({'id': category_id})


    return render_template('expenses_category.html', category_id = category_id, expenses = expenses, category = category)


@app.route('/expenses/new/<int:category_id>')
def expense_new(category_id):

    if 'uuid' not in session:
        return redirect('/')

    return render_template('expense_new.html', category_id = category_id)


@app.route('/expense/create/<int:category_id>', methods=['POST'])
def expense_create(category_id):

    
    is_valid = Expense.validator_create_expense(request.form)

    if is_valid == False:
        return redirect(f'/expenses/new/{category_id}')

    data = {
        **request.form,
        'category_id': category_id
    }

    expense_id = Expense.create_expense(data)

    return redirect(f'/expenses/{category_id}')


@app.route('/expenses/delete/<int:category_id>/<int:id>')
def expense_delete(id, category_id):

    if 'uuid' not in session:
        return redirect('/')

    Expense.delete_one({'id': id})

    return redirect(f'/expenses/{category_id}')



@app.route('/expense/edit/<int:id>')
def expense_edit(id):

    if 'uuid' not in session:
        return redirect('/')

    expense = Expense.select_one({'id': id})


    return render_template('expense_edit_page.html', expense = expense)


@app.route('/expense/update/<int:id>', methods=['POST'])
def expense_update(id):

    
    is_valid = Expense.validator_create_expense(request.form)

    if is_valid == False:
        return redirect(f'/expense/edit/{id}')
    
    data = {
        **request.form,
        'id': id
    }

    Expense.update_one(data)

    return redirect('/category')


@app.route('/main/expense/create', methods=['POST'])
def expense_add_home():

    data = {
        **request.form
    }

    if 'category_id' not in data:
        data['category_id'] = ""


    is_valid = Expense.validator_create_expense(data)


    if is_valid == False:
        return redirect ('/main')

    Expense.create_expense(request.form)

    return redirect('/main')



