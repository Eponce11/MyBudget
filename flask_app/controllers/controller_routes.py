from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_users import User
from flask_app.models.model_categories import Category
from flask_app.models.model_expenses import Expense
from flask_app.models.model_incomes import Income

@app.route('/')
def index():

    if 'uuid' in session:
        return redirect('/main')

    return render_template('login_page.html')


@app.route('/create_account')
def create_account():

    if 'uuid' in session:
        return redirect('/main')

    return render_template('create_account_page.html')


@app.route('/main')
def main():

    if 'uuid' not in session:
        return redirect('/')

    user = User.get_user({'id': session['uuid']})

    categories = Category.get_all_users_categories({'id': session['uuid']})

    total = 0

    for category in categories:
        expenses = Expense.get_all_category_expenses({'id': category.id})
        for expense in expenses:
            total = total + int(expense.cost)
    
    incomes = Income.get_all_users_incomes({'id': session['uuid']})

    income_total = 0

    for income in incomes:
        income_total = income_total + int(income.amount)


    return render_template('main_page.html', user = user, categories = categories, total = total, income_total = income_total)


