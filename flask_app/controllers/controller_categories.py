from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_categories import Category
from flask_app.models.model_expenses import Expense

@app.route('/category')
def category():

    if 'uuid' not in session:
        return redirect('/')

    categories = Category.get_all_users_categories({'id': session['uuid']})

    total = 0
    all_total = 0

    for category in categories:
        expenses = Expense.get_all_category_expenses({'id': category.id})
        for expense in expenses:
            total = total + int(expense.cost)
            all_total = all_total + int(expense.cost)
        Category.update_one_total({'total': total, 'id': category.id})
        total = 0

    updated_categories = Category.get_all_users_categories({'id': session['uuid']})
    
    

    return render_template('category_page.html', categories = updated_categories, total = all_total)



@app.route('/category/new')
def category_new():

    if 'uuid' not in session:
        return redirect('/')

    return render_template('category_new.html')


@app.route('/category/create', methods=['POST'])
def category_create():

    
    is_valid = Category.validator_create_category(request.form)

    if is_valid == False:
        return redirect('/category/new')

    data = {
        **request.form,
        'user_id': session['uuid']
    }


    category_id = Category.create_category(data)


    return redirect('/category')




@app.route('/category/delete/<int:id>')
def category_delete(id):

    if 'uuid' not in session:
        return redirect('/')
    
    # Category.delete_one({'id': id})

    return redirect('/category')



@app.route('/category/edit/<int:id>')
def category_edit(id):

    if 'uuid' not in session:
        return redirect('/')

    category = Category.select_one({'id': id})

    return render_template('category_edit_page.html', category = category)


@app.route('/category/update/<int:id>', methods=['POST'])
def category_update(id):

    is_valid = Category.validator_create_category(request.form)

    if is_valid == False:
        return redirect(f'/category/edit/{id}')
    
    data = {
        **request.form,
        'id': id
    }

    Category.update_one(data)

    return redirect('/category')





